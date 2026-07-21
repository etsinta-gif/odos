import uuid

from sqlalchemy.orm import Session

from src.masters.models import MST_Lender, MST_Product
from src.rules.models import RUL_CommissionRule


def _product_code(row_data: dict, lender_id: int) -> str:
    raw = str(row_data.get("product_code") or "").strip()
    if raw:
        return raw
    sub_product = str(row_data.get("sub_product") or row_data.get("product_name") or "UNKNOWN").strip().replace(" ", "_")
    roi = row_data.get("roi_percent")
    return f"{lender_id}:{sub_product}:{roi if roi not in (None, '') else 'NA'}"


def promote_commission_rule(session: Session, staging_rows: list[dict], template: object, conflict_resolution: str = "SKIP") -> dict:
    created = 0
    updated = 0
    skipped = 0
    failed = 0
    records: list[tuple[dict, int]] = []

    for item in staging_rows:
        row_data = dict(item.get("mapped_data", {}))
        lender_code = str(row_data.get("lender_code") or "").strip()
        slab_type = str(row_data.get("slab_type") or "FLAT").strip() or "FLAT"
        if not lender_code:
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

        existing = (
            session.query(RUL_CommissionRule)
            .filter(RUL_CommissionRule.lender_id == lender.lender_id)
            .filter(RUL_CommissionRule.product_id == product.product_id)
            .filter(RUL_CommissionRule.slab_type == slab_type)
            .first()
        )

        if existing:
            if conflict_resolution == "SKIP":
                skipped += 1
                records.append((item, existing.commission_rule_id))
                continue
            if conflict_resolution == "FAIL":
                failed += 1
                continue

            existing.basis_type = row_data.get("basis_type") or existing.basis_type
            existing.calculation_type = str(row_data.get("calculation_type") or existing.calculation_type or "PERCENTAGE")
            existing.flat_rate = row_data.get("flat_rate", existing.flat_rate)
            existing.base_rate = row_data.get("base_rate", existing.base_rate)
            existing.base_percent = row_data.get("base_percent", existing.base_percent)
            existing.headline_percent = row_data.get("headline_percent", existing.headline_percent)
            existing.pf_percent = row_data.get("pf_percent", existing.pf_percent)
            existing.i_percent = row_data.get("i_percent", existing.i_percent)
            existing.qualifying_condition = row_data.get("qualifying_condition") or existing.qualifying_condition
            existing.qualifying_notes = row_data.get("qualifying_notes") or existing.qualifying_notes
            existing.commercial_terms = row_data.get("commercial_terms") or existing.commercial_terms
            existing.clawback_conditions = row_data.get("clawback_conditions") or existing.clawback_conditions
            existing.status = row_data.get("status") or existing.status
            existing.is_active = True
            session.add(existing)
            session.flush()
            updated += 1
            records.append((item, existing.commission_rule_id))
            continue

        rule = RUL_CommissionRule(
            rule_code=str(row_data.get("rule_code") or f"RULE-{uuid.uuid4().hex[:10]}"),
            rule_name=str(row_data.get("rule_name") or f"{lender_code}-{product_code}-{slab_type}"),
            lender_id=lender.lender_id,
            product_id=product.product_id,
            slab_type=slab_type,
            basis_type=row_data.get("basis_type"),
            calculation_type=str(row_data.get("calculation_type") or "PERCENTAGE"),
            flat_rate=row_data.get("flat_rate"),
            base_rate=row_data.get("base_rate"),
            base_percent=row_data.get("base_percent"),
            headline_percent=row_data.get("headline_percent"),
            pf_percent=row_data.get("pf_percent"),
            i_percent=row_data.get("i_percent"),
            qualifying_condition=row_data.get("qualifying_condition"),
            qualifying_notes=row_data.get("qualifying_notes"),
            commercial_terms=row_data.get("commercial_terms"),
            clawback_conditions=row_data.get("clawback_conditions"),
            status=row_data.get("status"),
            is_active=True,
        )
        session.add(rule)
        session.flush()
        created += 1
        records.append((item, rule.commission_rule_id))

    return {
        "table": "RUL_CommissionRule",
        "created": created,
        "updated": updated,
        "skipped": skipped,
        "failed": failed,
        "records": records,
    }