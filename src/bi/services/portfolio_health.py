from __future__ import annotations

from datetime import date
from collections import defaultdict
from sqlalchemy.orm import Session

from src.admin.api.pnl_policy import SIM_TEMPLATE_BY_COMPONENT
from src.bi.services.phase1_common import quality, ratio, rows_for_period, safe_number, scoped_rows, sim_date, sim_rows, sim_value
from src.masters.models import MST_Customer, MST_Lender
from src.transactions.models import TRN_Case, TRN_Revenue


def calculate(db: Session, company_id: int, period_from: date, period_to: date) -> dict:
    sim_revenue_rows = sim_rows(db, SIM_TEMPLATE_BY_COMPONENT["revenue"], company_id)
    if company_id == 0 or sim_revenue_rows:
        return _calculate_from_sim(db, sim_revenue_rows, period_from, period_to)

    all_revenue = scoped_rows(db, TRN_Revenue, company_id)
    revenue, missing = rows_for_period(all_revenue, "revenue_date", period_from, period_to)
    customers = {row.customer_id: row for row in scoped_rows(db, MST_Customer, company_id)}
    lenders = {row.lender_id: row for row in scoped_rows(db, MST_Lender, company_id)}
    cases = {row.case_id: row for row in scoped_rows(db, TRN_Case, company_id)}
    by_rating: dict[str, float] = defaultdict(float)
    by_lender: dict[str, float] = defaultdict(float)
    by_unrated_customer: dict[str, float] = defaultdict(float)
    for row in revenue:
        amount = safe_number(row.net_amount or row.gross_amount or row.amount)
        case = cases.get(getattr(row, "case_id", None))
        customer = customers.get(getattr(case, "customer_id", None) if case is not None else getattr(row, "party_id", None))
        lender = lenders.get(getattr(case, "lender_id", None) if case is not None else getattr(row, "party_id", None))
        rating = str(getattr(lender, "credit_rating", None) or getattr(customer, "credit_rating_universal_rating", None) or "UNRATED").strip() or "UNRATED"
        by_rating[rating] += amount
        dimension = getattr(lender, "lender_name", None) or getattr(customer, "full_name", None) or getattr(row, "party_id", None) or "UNASSIGNED"
        by_lender[str(dimension)] += amount
        if rating == "UNRATED":
            customer_name = getattr(customer, "full_name", None) or getattr(row, "party_id", None) or "UNASSIGNED"
            by_unrated_customer[str(customer_name)] += amount
    total = sum(by_rating.values())
    concentration = sorted(
        [{"dimension": key, "revenue": round(value, 2), "share_pct": ratio(value, total)} for key, value in by_lender.items()],
        key=lambda item: item["revenue"], reverse=True,
    )
    unrated_customers = sorted(
        [{"customer": key, "revenue": round(value, 2), "share_pct": ratio(value, total)} for key, value in by_unrated_customer.items()],
        key=lambda item: item["revenue"],
        reverse=True,
    )
    weighted_rating_score, rated_revenue, unrated_revenue = _weighted_rating_score(by_rating, total)
    rating_coverage = round((rated_revenue / total) * 100, 2) if total else 0
    return {
        "period_from": period_from,
        "period_to": period_to,
        "revenue_total": round(total, 2),
        "revenue_by_credit_rating": [{"rating": key, "revenue": round(value, 2), "share_pct": ratio(value, total)} for key, value in sorted(by_rating.items())],
        "concentration": concentration,
        "unrated_customers": unrated_customers,
        "weighted_average_risk_score": weighted_rating_score,
        "risk_score": weighted_rating_score,
        "associated_rating": _associated_rating(weighted_rating_score),
        "rating_scale": {"minimum": 1, "maximum": 20, "worst": "D", "best": "AAA"},
        "rating_coverage_pct": rating_coverage,
        "unrated_revenue": round(unrated_revenue, 2),
        "risk_band": "LOW" if weighted_rating_score is not None and weighted_rating_score >= 15 else "MODERATE" if weighted_rating_score is not None and weighted_rating_score >= 10 else "HIGH" if weighted_rating_score is not None else "UNRATED",
        "data_quality": quality(len(all_revenue), missing, missing),
    }


def _calculate_from_sim(db: Session, rows: list[dict], period_from: date, period_to: date) -> dict:
    selected = [row for row in rows if sim_date(row, ["Invoice_Date", "revenue_date"]) and period_from <= sim_date(row, ["Invoice_Date", "revenue_date"]) <= period_to]
    lenders = scoped_rows(db, MST_Lender, 0)
    customers = scoped_rows(db, MST_Customer, 0)
    lender_by_name = {_normalise_lookup(getattr(row, "lender_name", None)): row for row in lenders if getattr(row, "lender_name", None)}
    customer_by_name = {_normalise_lookup(getattr(row, "full_name", None)): row for row in customers if getattr(row, "full_name", None)}
    lender_by_id = {str(getattr(row, "lender_id", "")): row for row in lenders}
    customer_by_id = {str(getattr(row, "customer_id", "")): row for row in customers}
    by_rating: dict[str, float] = defaultdict(float)
    by_dimension: dict[str, float] = defaultdict(float)
    by_unrated_customer: dict[str, float] = defaultdict(float)
    for row in selected:
        amount = safe_number(sim_value(row, ["Gross_Amount", "Net_Amount", "amount"]))
        lender, customer = _sim_master_matches(row, lender_by_name, customer_by_name, lender_by_id, customer_by_id)
        rating = str(getattr(lender, "credit_rating", None) or getattr(customer, "credit_rating_universal_rating", None) or sim_value(row, ["Credit_Rating", "credit_rating", "Rating"]) or "UNRATED").strip() or "UNRATED"
        dimension = str(getattr(lender, "lender_name", None) or getattr(customer, "full_name", None) or sim_value(row, ["Lender_Name", "Lender", "Customers_Name", "P&L_Unit"]) or "UNASSIGNED").strip()
        by_rating[rating] += amount
        by_dimension[dimension] += amount
        if rating == "UNRATED":
            customer_name = str(getattr(customer, "full_name", None) or sim_value(row, ["Customers_Name", "Customer_Name", "customer_name", "Customer"]) or "UNASSIGNED").strip() or "UNASSIGNED"
            by_unrated_customer[customer_name] += amount
    total = sum(by_rating.values())
    concentration = sorted([{"dimension": key, "revenue": round(value, 2), "share_pct": ratio(value, total)} for key, value in by_dimension.items()], key=lambda item: item["revenue"], reverse=True)
    unrated_customers = sorted(
        [{"customer": key, "revenue": round(value, 2), "share_pct": ratio(value, total)} for key, value in by_unrated_customer.items()],
        key=lambda item: item["revenue"],
        reverse=True,
    )
    weighted_rating_score, rated_revenue, unrated_revenue = _weighted_rating_score(by_rating, total)
    rating_coverage = round((rated_revenue / total) * 100, 2) if total else 0
    return {
        "period_from": period_from,
        "period_to": period_to,
        "revenue_total": round(total, 2),
        "revenue_by_credit_rating": [{"rating": key, "revenue": round(value, 2), "share_pct": ratio(value, total)} for key, value in sorted(by_rating.items())],
        "concentration": concentration,
        "unrated_customers": unrated_customers,
        "weighted_average_risk_score": weighted_rating_score,
        "risk_score": weighted_rating_score,
        "associated_rating": _associated_rating(weighted_rating_score),
        "rating_scale": {"minimum": 1, "maximum": 20, "worst": "D", "best": "AAA"},
        "rating_coverage_pct": rating_coverage,
        "unrated_revenue": round(unrated_revenue, 2),
        "risk_band": "LOW" if weighted_rating_score is not None and weighted_rating_score >= 15 else "MODERATE" if weighted_rating_score is not None and weighted_rating_score >= 10 else "HIGH" if weighted_rating_score is not None else "UNRATED",
        "data_quality": {"source_rows": len(rows), "included_rows": len(selected), "excluded_rows": max(len(rows) - len(selected), 0), "missing_date_rows": 0},
    }


RATING_SCORE = {
    "D": 1, "C-": 2, "C": 3, "C+": 4, "B-": 5, "B": 6, "B+": 7,
    "BB-": 8, "BB": 9, "BB+": 10, "BBB-": 11, "BBB": 12, "BBB+": 13,
    "A-": 14, "A": 15, "A+": 16, "AA-": 17, "AA": 18, "AA+": 19, "AAA": 20,
}


def _weighted_rating_score(by_rating: dict[str, float], total_revenue: float) -> tuple[float | None, float, float]:
    rated_revenue = 0.0
    weighted_total = 0.0
    unrated_revenue = 0.0
    for rating, revenue in by_rating.items():
        score = RATING_SCORE.get(rating.upper().replace("−", "-"))
        if score is None:
            unrated_revenue += revenue
            continue
        rated_revenue += revenue
        weighted_total += score * revenue
    return (round(weighted_total / total_revenue, 2) if total_revenue else None, rated_revenue, unrated_revenue)


def _associated_rating(score: float | None) -> str:
    if score is None or score <= 0:
        return "UNRATED"
    return min(RATING_SCORE, key=lambda rating: (abs(RATING_SCORE[rating] - score), -RATING_SCORE[rating]))


def _normalise_lookup(value: object) -> str:
    return " ".join(str(value or "").strip().upper().split())


def _sim_master_matches(row: dict, lender_by_name: dict, customer_by_name: dict, lender_by_id: dict, customer_by_id: dict):
    lender_id = sim_value(row, ["Lender_ID", "lender_id", "Lender_Master_ID", "lender_master_id"])
    customer_id = sim_value(row, ["Customer_ID", "customer_id", "Customer_Master_ID", "customer_master_id"])
    lender = lender_by_id.get(str(lender_id)) if lender_id not in (None, "") else None
    customer = customer_by_id.get(str(customer_id)) if customer_id not in (None, "") else None
    if lender is None:
        lender_name = sim_value(row, ["Lender_Name", "Lender", "lender_name"])
        lender = lender_by_name.get(_normalise_lookup(lender_name))
    if customer is None:
        customer_name = sim_value(row, ["Customers_Name", "Customer_Name", "customer_name", "Customer"])
        customer = customer_by_name.get(_normalise_lookup(customer_name))
    return lender, customer
