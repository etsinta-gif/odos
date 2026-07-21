from sqlalchemy.orm import Session

from src.masters.models import MST_Lender, MST_Product
from src.rules.models import RUL_CommissionRule
from src.transactions.models import RUL_CommissionSlab


def _product_code(row_data: dict, lender_id: int) -> str:
    raw = str(row_data.get("product_code") or "").strip()
    if raw:
        return raw
    sub_product = str(row_data.get("sub_product") or row_data.get("product_name") or "UNKNOWN").strip().replace(" ", "_")
    roi = row_data.get("roi_percent")
    return f"{lender_id}:{sub_product}:{roi if roi not in (None, '') else 'NA'}"


def promote_commission_slab(session: Session, staging_rows: list[dict], template: object, conflict_resolution: str = "SKIP") -> dict:
    created = 0
    updated = 0
    skipped = 0
    failed = 0
    records: list[tuple[dict, int]] = []

    for item in staging_rows:
        row_data = dict(item.get("mapped_data", {}))
        lender_code = str(row_data.get("lender_code") or "").strip()
        tier_name = str(row_data.get("tier_name") or row_data.get("slab_label") or "").strip()
        slab_type = str(row_data.get("slab_type") or "FLAT").strip() or "FLAT"
        if not lender_code or not tier_name:
            failed += 1
            continue

        lender = session.query(MST_Lender).filter(MST_Lender.lender_code == lender_code).first()
        if lender is None:
            failed += 1
            continue

        product_code = _product_code(row_data, lender.lender_id)
        product = session.query(MST_Product).filter(MST_Product.product_code == product_code).first()
        if product is None:
            failed += 1
            continue

        rule = (
            session.query(RUL_CommissionRule)
            .filter(RUL_CommissionRule.lender_id == lender.lender_id)
            .filter(RUL_CommissionRule.product_id == product.product_id)
            .filter(RUL_CommissionRule.slab_type == slab_type)
            .first()
        )
        if rule is None:
            failed += 1
            continue

        scoped_slab_label = f"{rule.commission_rule_id}:{tier_name}"

        existing = (
            session.query(RUL_CommissionSlab)
            .filter(RUL_CommissionSlab.commission_rule_id == rule.commission_rule_id)
            .filter(RUL_CommissionSlab.tier_name == tier_name)
            .first()
        )

        if existing:
            if conflict_resolution == "SKIP":
                skipped += 1
                records.append((item, existing.slab_id))
                continue
            if conflict_resolution == "FAIL":
                failed += 1
                continue

            existing.slab_label = scoped_slab_label
            existing.tier_min = row_data.get("tier_min", existing.tier_min)
            existing.tier_max = row_data.get("tier_max", existing.tier_max)
            existing.rate = row_data.get("rate", existing.rate)
            existing.is_active = True
            session.add(existing)
            session.flush()
            updated += 1
            records.append((item, existing.slab_id))
            continue

        slab = RUL_CommissionSlab(
            commission_rule_id=rule.commission_rule_id,
            slab_label=scoped_slab_label,
            tier_name=tier_name,
            tier_min=row_data.get("tier_min"),
            tier_max=row_data.get("tier_max"),
            rate=row_data.get("rate") or 0.0,
            is_active=True,
        )
        session.add(slab)
        session.flush()
        created += 1
        records.append((item, slab.slab_id))

    return {
        "table": "RUL_CommissionSlab",
        "created": created,
        "updated": updated,
        "skipped": skipped,
        "failed": failed,
        "records": records,
    }