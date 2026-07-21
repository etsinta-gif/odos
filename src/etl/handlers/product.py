from sqlalchemy.orm import Session

from src.masters.models import MST_Lender, MST_Product


def _product_code(row_data: dict, lender_id: int) -> str:
    raw = str(row_data.get("product_code") or "").strip()
    if raw:
        return raw
    sub_product = str(row_data.get("sub_product") or row_data.get("product_name") or "UNKNOWN").strip().replace(" ", "_")
    roi = row_data.get("roi_percent")
    return f"{lender_id}:{sub_product}:{roi if roi not in (None, '') else 'NA'}"


def promote_product(session: Session, staging_rows: list[dict], template: object, conflict_resolution: str = "SKIP") -> dict:
    created = 0
    updated = 0
    skipped = 0
    failed = 0
    records: list[tuple[dict, int]] = []

    for item in staging_rows:
        row_data = dict(item.get("mapped_data", {}))
        lender_code = str(row_data.get("lender_code") or "").strip()
        if not lender_code:
            failed += 1
            continue

        lender = session.query(MST_Lender).filter(MST_Lender.lender_code == lender_code).first()
        if lender is None:
            failed += 1
            continue

        product_code = _product_code(row_data, lender.lender_id)
        product_name = str(row_data.get("product_name") or row_data.get("sub_product") or "Unknown Product").strip()
        existing = session.query(MST_Product).filter(MST_Product.product_code == product_code).first()

        if existing:
            if conflict_resolution == "SKIP":
                skipped += 1
                records.append((item, existing.product_id))
                continue
            if conflict_resolution == "FAIL":
                failed += 1
                continue

            existing.product_name = product_name
            existing.sub_product = str(row_data.get("sub_product") or existing.sub_product or product_name)
            existing.roi_percent = row_data.get("roi_percent", existing.roi_percent)
            existing.interest_rate = row_data.get("roi_percent", existing.interest_rate)
            existing.lender_id = lender.lender_id
            existing.is_active = True
            session.add(existing)
            session.flush()
            updated += 1
            records.append((item, existing.product_id))
            continue

        product = MST_Product(
            product_name=product_name,
            product_code=product_code,
            lender_id=lender.lender_id,
            sub_product=str(row_data.get("sub_product") or product_name),
            roi_percent=row_data.get("roi_percent"),
            interest_rate=row_data.get("roi_percent"),
            min_loan_amount=row_data.get("min_loan_amount"),
            max_loan_amount=row_data.get("max_loan_amount"),
            is_active=True,
        )
        session.add(product)
        session.flush()
        created += 1
        records.append((item, product.product_id))

    return {
        "table": "MST_Product",
        "created": created,
        "updated": updated,
        "skipped": skipped,
        "failed": failed,
        "records": records,
    }