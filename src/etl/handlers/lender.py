import uuid

from sqlalchemy.orm import Session

from src.masters.models import MST_Lender


def promote_lender(session: Session, staging_rows: list[dict], template: object, conflict_resolution: str = "SKIP") -> dict:
    created = 0
    updated = 0
    skipped = 0
    failed = 0
    records: list[tuple[dict, int]] = []

    for item in staging_rows:
        row_data = dict(item.get("mapped_data", {}))
        lender_code = str(row_data.get("lender_code") or "").strip()
        pan = str(row_data.get("pan") or "").strip()
        lender_name = str(row_data.get("lender_name") or "").strip()
        if not lender_name:
            failed += 1
            continue

        existing = None
        if lender_code:
            existing = session.query(MST_Lender).filter(MST_Lender.lender_code == lender_code).first()
        if existing is None and pan:
            existing = session.query(MST_Lender).filter(MST_Lender.pan == pan).first()

        if existing:
            if conflict_resolution == "SKIP":
                skipped += 1
                records.append((item, existing.lender_id))
                continue
            if conflict_resolution == "FAIL":
                failed += 1
                continue

            existing.lender_name = lender_name
            existing.gstin = row_data.get("gstin") or existing.gstin
            existing.lender_code = lender_code or existing.lender_code or f"L-{uuid.uuid4().hex[:8]}"
            existing.pan = pan or existing.pan or f"PAN-{uuid.uuid4().hex[:8]}"
            existing.dsa_code = row_data.get("dsa_code") or existing.dsa_code
            existing.is_nbfc = bool(row_data.get("is_nbfc", existing.is_nbfc))
            existing.is_active = True
            session.add(existing)
            session.flush()
            updated += 1
            records.append((item, existing.lender_id))
            continue

        lender = MST_Lender(
            lender_name=lender_name,
            pan=pan or f"PAN-{uuid.uuid4().hex[:8]}",
            gstin=row_data.get("gstin"),
            lender_code=lender_code or f"L-{uuid.uuid4().hex[:8]}",
            dsa_code=row_data.get("dsa_code"),
            is_nbfc=bool(row_data.get("is_nbfc", False)),
            is_active=True,
        )
        session.add(lender)
        session.flush()
        created += 1
        records.append((item, lender.lender_id))

    return {
        "table": "MST_Lender",
        "created": created,
        "updated": updated,
        "skipped": skipped,
        "failed": failed,
        "records": records,
    }