from datetime import date

from src.bi.services.pnl_phase1 import calculate as calculate_pnl
from src.bi.services.pnl_phase1 import variable_expense_distribution
from src.bi.services.portfolio_health import calculate as calculate_portfolio
from src.bi.services.working_capital import calculate as calculate_working_capital
from src.bi.services import portfolio_health as portfolio_health_service
from src.bi.services import working_capital as working_capital_service
from src.masters.models import MST_Customer, MST_Lender
from src.transactions.models import TRN_Case, TRN_Commission, TRN_Expense, TRN_Revenue


def test_phase1_pnl_returns_additive_metrics_and_growth(test_db) -> None:
    test_db.add_all(
        [
            TRN_Revenue(company_id=88001, revenue_date=date(2026, 8, 10), net_amount=1000, gross_amount=1000, is_active=True),
            TRN_Commission(company_id=88001, commission_date=date(2026, 8, 10), net_amount=100, gross_amount=100, is_active=True),
            TRN_Expense(company_id=88001, expense_date=date(2026, 8, 10), amount=50, net_amount=50, is_active=True),
            TRN_Revenue(company_id=88001, revenue_date=date(2026, 7, 10), net_amount=500, gross_amount=500, is_active=True),
            TRN_Revenue(company_id=88002, revenue_date=date(2026, 8, 10), net_amount=9999, gross_amount=9999, is_active=True),
        ]
    )
    test_db.commit()

    result = calculate_pnl(test_db, 88001, date(2026, 8, 1), date(2026, 8, 31))

    assert result["revenue"] == 1000
    assert result["variable_expenses"] == 100
    assert result["fixed_costs"] == 50
    assert result["ebitda"] == 850
    assert result["revenue_growth"] == 100.0
    assert result["data_quality"]["included_rows"] == 4


def test_variable_expense_distribution_returns_unit_and_revenue_bands() -> None:
    distribution = variable_expense_distribution(
        [
            {"revenue": 1000, "variable_expenses": 50},
            {"revenue": 2000, "variable_expenses": 1000},
            {"revenue": 500, "variable_expenses": 0},
        ]
    )

    by_label = {row["label"]: row for row in distribution}
    assert by_label["0-10%"]["unit_count"] == 1
    assert by_label["0-10%"]["revenue_amount"] == 1500
    assert by_label["50-60%"]["unit_count"] == 1
    assert by_label["50-60%"]["revenue_amount"] == 2000


def test_phase1_working_capital_empty_dataset_is_explicit(test_db) -> None:
    result = calculate_working_capital(test_db, 88003, date(2026, 8, 1), date(2026, 8, 31))

    assert result["dso"] is None
    assert result["dpo"] is None
    assert result["ccc"] is None
    assert result["working_capital_requirement"] is None
    assert result["data_quality"]["source_rows"] == 0


def test_working_capital_dpo_uses_invoice_payment_date_for_expense_mis(test_db, monkeypatch) -> None:
    def staged_rows(_db, template_name, _company_id):
        if template_name == "REVENUE_SALES":
            return [
                {"P&L_Unit": "UNIT-1", "Invoice_Date": "2026-01-01", "Gross_Amount": 1000},
                {"P&L_Unit": "UNIT-1", "Invoice_Date": "2026-01-01", "Invoice_Payment_Date": "2026-01-11", "Gross_Amount": 50},
                {"P&L_Unit": "UNIT-1", "Invoice_Date": "2026-01-01", "Invoice_Payment_Date": "2999-01-01", "Gross_Amount": 75},
            ]
        if template_name in {"EXPENSES_VARIABLE_AGENTS", "EXPENSES_VARIABLE_EMPLOYEE"}:
            return [{"P&L_Unit": "UNIT-1", "Invoice_Date": "2026-01-01", "Invoice_Payment_Date": "2026-01-11", "Gross_Amount": 100}]
        return []

    monkeypatch.setattr(working_capital_service, "sim_rows", staged_rows)
    result = calculate_working_capital(test_db, 0, date(2026, 1, 1), date(2026, 1, 31))

    assert result["dpo"] == 10.0
    assert result["dpo_by_payable_type"][0]["dpo_days"] == 10.0
    assert result["outstanding_receivables"] == 1075.0
    assert result["outstanding_payables"] == 0.0
    assert result["total_revenue"] == 1125.0
    assert result["total_expenses"] == 200.0
    assert result["gross_working_capital"] == 925.0
    assert result["monthly_cash_flow"] == [{"month": "2026-01", "amount_received": 50.0, "amount_paid": 200.0, "shortfall_excess": -150.0, "cumulative_amount_received": 50.0, "cumulative_amount_paid": 200.0, "cumulative_shortfall_excess": -150.0}]
    assert sum(row["amount"] for row in result["receivables_aging"]) == 1075.0
    assert sum(row["amount"] for row in result["payables_aging"]) == 0.0
    assert result["receivables_aging"][0]["amount"] == 1075.0


def test_phase1_portfolio_health_preserves_unrated_bucket_and_tenant_scope(test_db) -> None:
    test_db.add_all(
        [
            MST_Customer(company_id=88004, customer_id=94001, full_name="Rated", pan="PAN-RATED", credit_rating_universal_rating="A", is_active=True),
            MST_Customer(company_id=88004, customer_id=94002, full_name="Unrated", pan="PAN-UNRATED", credit_rating_universal_rating=None, is_active=True),
            TRN_Case(company_id=88004, case_id=95001, case_number="CASE-95001", customer_id=94001, lender_id=1, product_id=1, is_active=True),
            TRN_Case(company_id=88004, case_id=95002, case_number="CASE-95002", customer_id=94002, lender_id=1, product_id=1, is_active=True),
            TRN_Revenue(company_id=88004, case_id=95001, revenue_date=date(2026, 8, 10), net_amount=700, gross_amount=700, is_active=True),
            TRN_Revenue(company_id=88004, case_id=95002, revenue_date=date(2026, 8, 10), net_amount=300, gross_amount=300, is_active=True),
            TRN_Revenue(company_id=88005, party_id=94001, revenue_date=date(2026, 8, 10), net_amount=9999, gross_amount=9999, is_active=True),
        ]
    )
    test_db.commit()

    result = calculate_portfolio(test_db, 88004, date(2026, 8, 1), date(2026, 8, 31))

    ratings = {row["rating"]: row["revenue"] for row in result["revenue_by_credit_rating"]}
    assert ratings == {"A": 700.0, "UNRATED": 300.0}
    assert result["revenue_total"] == 1000
    assert result["weighted_average_risk_score"] == 10.5
    assert result["risk_score"] == 10.5
    assert result["associated_rating"] == "BBB-"
    assert result["rating_coverage_pct"] == 70.0
    assert result["risk_band"] == "MODERATE"


def test_phase1_portfolio_health_uses_linked_lender_rating_for_hdfc(test_db) -> None:
    test_db.add_all(
        [
            MST_Lender(company_id=88006, lender_id=96001, lender_name="HDFC", credit_rating="AAA", is_active=True),
            MST_Customer(company_id=88006, customer_id=96002, full_name="Unrated Customer", pan="PAN-HDFC", credit_rating_universal_rating=None, is_active=True),
            TRN_Case(company_id=88006, case_id=96003, case_number="CASE-HDFC", customer_id=96002, lender_id=96001, product_id=1, is_active=True),
            TRN_Revenue(company_id=88006, case_id=96003, revenue_date=date(2026, 8, 10), net_amount=1_400_000, gross_amount=1_400_000, is_active=True),
        ]
    )
    test_db.commit()

    result = calculate_portfolio(test_db, 88006, date(2026, 8, 1), date(2026, 8, 31))

    assert result["revenue_by_credit_rating"] == [{"rating": "AAA", "revenue": 1_400_000.0, "share_pct": 100.0}]
    assert result["weighted_average_risk_score"] == 20.0
    assert result["associated_rating"] == "AAA"
    assert result["unrated_revenue"] == 0.0
    assert result["concentration"][0]["dimension"] == "HDFC"


def test_phase1_portfolio_health_lists_unrated_customers_and_revenue(test_db) -> None:
    test_db.add_all(
        [
            MST_Customer(company_id=88008, customer_id=98001, full_name="Unrated A", pan="PAN-A", credit_rating_universal_rating=None, is_active=True),
            MST_Customer(company_id=88008, customer_id=98002, full_name="Unrated B", pan="PAN-B", credit_rating_universal_rating=None, is_active=True),
            MST_Customer(company_id=88008, customer_id=98003, full_name="Rated C", pan="PAN-C", credit_rating_universal_rating="AA", is_active=True),
            TRN_Case(company_id=88008, case_id=98010, case_number="CASE-A", customer_id=98001, lender_id=1, product_id=1, is_active=True),
            TRN_Case(company_id=88008, case_id=98011, case_number="CASE-B", customer_id=98002, lender_id=1, product_id=1, is_active=True),
            TRN_Case(company_id=88008, case_id=98012, case_number="CASE-C", customer_id=98003, lender_id=1, product_id=1, is_active=True),
            TRN_Revenue(company_id=88008, case_id=98010, revenue_date=date(2026, 8, 10), net_amount=600, gross_amount=600, is_active=True),
            TRN_Revenue(company_id=88008, case_id=98011, revenue_date=date(2026, 8, 10), net_amount=400, gross_amount=400, is_active=True),
            TRN_Revenue(company_id=88008, case_id=98012, revenue_date=date(2026, 8, 10), net_amount=200, gross_amount=200, is_active=True),
        ]
    )
    test_db.commit()

    result = calculate_portfolio(test_db, 88008, date(2026, 8, 1), date(2026, 8, 31))

    assert result["unrated_revenue"] == 1000.0
    assert result["unrated_customers"] == [
        {"customer": "Unrated A", "revenue": 600.0, "share_pct": 60.0},
        {"customer": "Unrated B", "revenue": 400.0, "share_pct": 40.0},
    ]


def test_phase1_portfolio_health_links_sim_lender_name_to_master_rating(test_db, monkeypatch) -> None:
    test_db.add(MST_Lender(company_id=88007, lender_id=97001, lender_name="HDFC", credit_rating="AAA", is_active=True))
    test_db.commit()

    def staged_rows(_db, template_name, _company_id):
        if template_name == "REVENUE_SALES":
            return [{"Lender_Name": "HDFC", "Invoice_Date": "2026-08-10", "Gross_Amount": 1_400_000}]
        return []

    monkeypatch.setattr(portfolio_health_service, "sim_rows", staged_rows)
    result = calculate_portfolio(test_db, 0, date(2026, 8, 1), date(2026, 8, 31))

    assert result["weighted_average_risk_score"] == 20.0
    assert result["associated_rating"] == "AAA"
    assert result["unrated_revenue"] == 0.0
