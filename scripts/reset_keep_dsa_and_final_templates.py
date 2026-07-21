import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from src.core.database import SessionLocal
from src.metadata.models import META_ImportTemplate
from src.metadata.services.fixed_template_bootstrap import FIXED_TEMPLATE_SPECS, seed_fixed_templates


DB_PATH = Path(__file__).resolve().parents[1] / "odos.db"
REPORT_PATH = Path(__file__).resolve().parents[1] / "docs" / "implementation" / "reset_keep_dsa_final_templates_report.json"


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def _list_tables(conn: sqlite3.Connection) -> list[str]:
    rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
    return [str(row[0]) for row in rows]


def _count_rows(conn: sqlite3.Connection, table_name: str) -> int:
    return int(conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0])


def _template_name_set() -> set[str]:
    return {spec["template_name"] for spec in FIXED_TEMPLATE_SPECS}


def _snapshot_counts(conn: sqlite3.Connection, tables: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for table in tables:
        if table.startswith("sqlite_"):
            continue
        counts[table] = _count_rows(conn, table)
    return counts


def _delete_non_final_templates(conn: sqlite3.Connection, final_names: set[str]) -> dict[str, int]:
    placeholders = ",".join(["?"] * len(final_names))
    non_final_ids = [
        row[0]
        for row in conn.execute(
            f"SELECT template_id FROM meta_import_template WHERE template_name NOT IN ({placeholders})",
            tuple(sorted(final_names)),
        ).fetchall()
    ]

    deleted_mapping_rows = 0
    deleted_template_rows = 0

    if non_final_ids:
        id_placeholders = ",".join(["?"] * len(non_final_ids))
        deleted_mapping_rows = int(
            conn.execute(
                f"SELECT COUNT(*) FROM meta_field_mapping WHERE template_id IN ({id_placeholders})",
                tuple(non_final_ids),
            ).fetchone()[0]
        )
        conn.execute(
            f"DELETE FROM meta_field_mapping WHERE template_id IN ({id_placeholders})",
            tuple(non_final_ids),
        )

        deleted_template_rows = int(
            conn.execute(
                f"SELECT COUNT(*) FROM meta_import_template WHERE template_id IN ({id_placeholders})",
                tuple(non_final_ids),
            ).fetchone()[0]
        )
        conn.execute(
            f"DELETE FROM meta_import_template WHERE template_id IN ({id_placeholders})",
            tuple(non_final_ids),
        )

    return {
        "deleted_non_final_template_rows": deleted_template_rows,
        "deleted_non_final_mapping_rows": deleted_mapping_rows,
    }


def _purge_all_except_preserved(conn: sqlite3.Connection, preserve_tables: set[str]) -> dict[str, int]:
    deleted_counts: dict[str, int] = {}
    tables = _list_tables(conn)
    for table in tables:
        if table.startswith("sqlite_"):
            continue
        if table in preserve_tables:
            continue

        before = _count_rows(conn, table)
        if before > 0:
            conn.execute(f"DELETE FROM {table}")
        deleted_counts[table] = before

    if "sqlite_sequence" in tables:
        for table in deleted_counts.keys():
            conn.execute("DELETE FROM sqlite_sequence WHERE name = ?", (table,))

    return deleted_counts


def _post_seed_template_audit(final_names: set[str]) -> dict:
    db = SessionLocal()
    try:
        seed_fixed_templates(db)

        rows = (
            db.query(META_ImportTemplate)
            .filter(META_ImportTemplate.status == "Active")
            .filter(META_ImportTemplate.is_active == True)
            .all()
        )
        active_names = sorted({row.template_name for row in rows})
        final_active = sorted([name for name in active_names if name in final_names])
        non_final_active = sorted([name for name in active_names if name not in final_names])

        return {
            "active_template_count": len(active_names),
            "final_active_template_count": len(final_active),
            "non_final_active_template_count": len(non_final_active),
            "final_active_templates": final_active,
            "non_final_active_templates": non_final_active,
        }
    finally:
        db.close()


def main() -> None:
    if not DB_PATH.exists():
        raise SystemExit(f"Database not found: {DB_PATH}")

    final_names = _template_name_set()
    conn = _connect()

    try:
        all_tables = _list_tables(conn)
        pre_counts = _snapshot_counts(conn, all_tables)
        pre_dsa_count = pre_counts.get("mst_dsa", 0)

        preserve_tables = {
            "mst_dsa",
            "meta_import_template",
            "meta_field_mapping",
            "alembic_version",
        }

        conn.execute("PRAGMA foreign_keys = OFF")
        try:
            template_cleanup = _delete_non_final_templates(conn, final_names)
            deleted_counts = _purge_all_except_preserved(conn, preserve_tables)
            conn.commit()
        finally:
            conn.execute("PRAGMA foreign_keys = ON")

        post_template = _post_seed_template_audit(final_names)
        post_counts = _snapshot_counts(conn, _list_tables(conn))
        post_dsa_count = post_counts.get("mst_dsa", 0)

        report = {
            "executed_at": datetime.now(timezone.utc).isoformat(),
            "db_path": str(DB_PATH),
            "mode": "direct_purge_keep_dsa_and_final_templates",
            "pre_counts": pre_counts,
            "post_counts": post_counts,
            "dsa_pre_count": pre_dsa_count,
            "dsa_post_count": post_dsa_count,
            "dsa_preserved": pre_dsa_count == post_dsa_count,
            "template_cleanup": template_cleanup,
            "deleted_counts": deleted_counts,
            "template_audit": post_template,
        }

        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")

        print(json.dumps(
            {
                "report_path": str(REPORT_PATH),
                "dsa_preserved": report["dsa_preserved"],
                "dsa_pre_count": pre_dsa_count,
                "dsa_post_count": post_dsa_count,
                "final_active_template_count": post_template["final_active_template_count"],
                "non_final_active_template_count": post_template["non_final_active_template_count"],
            },
            indent=2,
        ))

    finally:
        conn.close()


if __name__ == "__main__":
    main()
