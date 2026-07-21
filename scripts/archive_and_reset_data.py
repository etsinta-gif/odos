import argparse
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).resolve().parents[1] / "odos.db"
ARCHIVE_DIR = Path(__file__).resolve().parents[1] / "archives"

TABLES_TO_RESET = [
    # Masters
    "mst_customer",
    "mst_dsa",
    "mst_lender",
    "mst_product",
    "mst_employee",
    "mst_connector",
    "mst_vendor",
    "mst_expense_category",
    "mst_cost_center",
    "mst_company_bank_account",
    # Transactions
    "trn_case",
    "trn_case_status_history",
    "trn_revenue",
    "trn_commission",
    "trn_expense",
    "trn_payment",
    "trn_recurring_expense",
    "trn_expense_claim",
    "trn_tally_export_batch",
    "trn_tally_export_detail",
    # Rules and slabs
    "rul_validation_rule",
    "rul_commission_rule",
    "rul_commission_slab",
    "rul_gst_rule",
    "rul_tds_rule",
    # ETL
    "etl_import_batch",
    "etl_staging_raw_data",
    "etl_error_log",
    "etl_data_lineage",
]


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def table_exists(conn: sqlite3.Connection, table: str) -> bool:
    q = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
    return conn.execute(q, (table,)).fetchone() is not None


def archive_tables(conn: sqlite3.Connection, output_path: Path) -> dict[str, int]:
    payload = {
        "archived_at": datetime.now(timezone.utc).isoformat(),
        "db_path": str(DB_PATH),
        "tables": {},
    }
    counts: dict[str, int] = {}

    for table in TABLES_TO_RESET:
        if not table_exists(conn, table):
            continue
        rows = [dict(r) for r in conn.execute(f"SELECT * FROM {table}").fetchall()]
        payload["tables"][table] = rows
        counts[table] = len(rows)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    return counts


def reset_tables(conn: sqlite3.Connection) -> dict[str, int]:
    deleted: dict[str, int] = {}
    conn.execute("PRAGMA foreign_keys = OFF")
    try:
        for table in TABLES_TO_RESET:
            if not table_exists(conn, table):
                continue
            before = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            conn.execute(f"DELETE FROM {table}")
            deleted[table] = before

        # Reset autoincrement counters for known tables.
        if table_exists(conn, "sqlite_sequence"):
            for table in TABLES_TO_RESET:
                conn.execute("DELETE FROM sqlite_sequence WHERE name = ?", (table,))

        conn.commit()
    finally:
        conn.execute("PRAGMA foreign_keys = ON")
    return deleted


def main() -> None:
    parser = argparse.ArgumentParser(description="Archive and reset ODOS data tables")
    parser.add_argument("--mode", choices=["archive", "reset", "archive-reset"], default="reset")
    parser.add_argument("--confirm", action="store_true", help="Required for reset operations")
    parser.add_argument("--backup", action="store_true", help="Create a backup before reset")
    parser.add_argument("--env", choices=["dev", "staging", "production"], default="dev")
    parser.add_argument("--dry-run", action="store_true", help="Preview reset impact without deleting data")
    parser.add_argument("--archive-file", default=None, help="Optional custom archive file path")
    args = parser.parse_args()

    if args.env == "production":
        raise SystemExit("Reset is blocked in production environment")

    if not DB_PATH.exists():
        raise SystemExit(f"Database not found: {DB_PATH}")

    conn = get_conn()
    try:
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        archive_file = Path(args.archive_file) if args.archive_file else ARCHIVE_DIR / f"odos_archive_{ts}.json"

        if args.mode in {"archive", "archive-reset"}:
            counts = archive_tables(conn, archive_file)
            print(f"Archive written: {archive_file}")
            print(json.dumps({"archived_counts": counts}, indent=2))

        if args.mode in {"reset", "archive-reset"}:
            if not args.confirm:
                raise SystemExit("Reset mode requires --confirm")

            if args.dry_run:
                preview = {}
                for table in TABLES_TO_RESET:
                    if not table_exists(conn, table):
                        continue
                    preview[table] = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                print(json.dumps({"dry_run": True, "candidate_delete_counts": preview}, indent=2))
                return

            if args.backup:
                ts_backup = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
                if shutil.which("pg_dump"):
                    backup_file = ARCHIVE_DIR / f"backup_{ts_backup}.sql"
                    backup_file.parent.mkdir(parents=True, exist_ok=True)
                    subprocess.run(["pg_dump", "-d", "odos_db", "-f", str(backup_file)], check=True)
                    print(f"PostgreSQL backup written: {backup_file}")
                else:
                    sqlite_backup = ARCHIVE_DIR / f"backup_{ts_backup}.db"
                    sqlite_backup.parent.mkdir(parents=True, exist_ok=True)
                    sqlite_backup.write_bytes(DB_PATH.read_bytes())
                    print(f"SQLite backup written: {sqlite_backup}")

            deleted = reset_tables(conn)
            print(json.dumps({"deleted_counts": deleted}, indent=2))
    finally:
        conn.close()


if __name__ == "__main__":
    main()
