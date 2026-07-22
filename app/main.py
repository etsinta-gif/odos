from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
from pathlib import Path
import os

from src.core.database import Base, engine, SessionLocal
from src.admin.api import mapping as mapping_router
from src.ai.api import router as ai_feedback_router
from src.alerts.api import alerts as alerts_router
from src.alerts import models as alerts_models  # noqa: F401
from src.alerts.services.scheduler import scheduler as alert_scheduler
from src.bi.api import dashboards as bi_dashboards_router
from src.bi.api import reports as bi_reports_router
from src.bi.api import trends as bi_trends_router
from src.masters.api import case, commission, connector, customer, dashboard, document, dsa, employee, etl, expense, lender, payment, product, redflags, revenue
from src.masters.ui import routes as ui_routes
from src.masters.ui import routes_dsa
from src.masters.ui import routes_5_1, routes_5_2, routes_5_3, routes_5_4, routes_5_5, routes_data_ops, routes_etl, routes_rules
from src.masters.api.tally import router as tally_api_router
from src.metadata import models as metadata_models  # noqa: F401
from src.ai import models as ai_models  # noqa: F401
from src.bi import models as bi_models  # noqa: F401
from src.reference import models as reference_models  # noqa: F401
from src.rules.api import rules as rules_router
from src.rules import models as rules_models  # noqa: F401
from src.metadata.services.fixed_template_bootstrap import seed_fixed_templates
from src.security.api import auth as auth_router
from src.security import models as security_models  # noqa: F401

app = FastAPI()


def _is_truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "on"}

cors_origins = [origin.strip() for origin in os.getenv("CORS_ALLOW_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}

templates = Jinja2Templates(directory="src/templates")
app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(customer.router)
app.include_router(dsa.router)
app.include_router(lender.router)
app.include_router(product.router)
app.include_router(employee.router)
app.include_router(connector.router)
app.include_router(case.router)
app.include_router(document.router)
app.include_router(revenue.router)
app.include_router(commission.router)
app.include_router(dashboard.router)
app.include_router(redflags.router)
app.include_router(alerts_router.router)
app.include_router(alerts_router.legacy_router)
app.include_router(expense.router)
app.include_router(payment.router)
app.include_router(etl.router)
app.include_router(tally_api_router)
app.include_router(mapping_router.router)
app.include_router(ai_feedback_router)
app.include_router(rules_router.router)
app.include_router(bi_reports_router.router)
app.include_router(bi_dashboards_router.router)
app.include_router(bi_trends_router.router)
app.include_router(auth_router.router)
app.include_router(ui_routes.router)
app.include_router(routes_dsa.router)
app.include_router(routes_5_1.router)
app.include_router(routes_5_2.router)
app.include_router(routes_5_3.router)
app.include_router(routes_5_4.router)
app.include_router(routes_5_5.router)
app.include_router(routes_etl.router)
app.include_router(routes_rules.router)
app.include_router(routes_data_ops.router)


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    db_path = Path(__file__).resolve().parents[1] / "odos.db"
    conn = sqlite3.connect(str(db_path))
    try:
        altered = False

        def _table_columns(table_name: str) -> set[str]:
            return {row[1] for row in conn.execute(f"PRAGMA table_info({table_name})").fetchall()}

        def _ensure_column(table_name: str, column_name: str, ddl: str) -> None:
            nonlocal altered
            if column_name not in _table_columns(table_name):
                conn.execute(ddl)
                altered = True

        product_columns = {row[1] for row in conn.execute("PRAGMA table_info(mst_product)").fetchall()}
        if "borrower_salary_range" not in product_columns:
            conn.execute("ALTER TABLE mst_product ADD COLUMN borrower_salary_range VARCHAR(255)")
            altered = True
        if "is_employed" not in product_columns:
            conn.execute("ALTER TABLE mst_product ADD COLUMN is_employed BOOLEAN DEFAULT 0")
            altered = True
        if "category" not in product_columns:
            conn.execute("ALTER TABLE mst_product ADD COLUMN category VARCHAR(255)")
            altered = True

        case_columns = {row[1] for row in conn.execute("PRAGMA table_info(trn_case)").fetchall()}
        if "branch_code" not in case_columns:
            conn.execute("ALTER TABLE trn_case ADD COLUMN branch_code VARCHAR(100)")
            altered = True
        if "branch_name" not in case_columns:
            conn.execute("ALTER TABLE trn_case ADD COLUMN branch_name VARCHAR(255)")
            altered = True
        if "referral_source" not in case_columns:
            conn.execute("ALTER TABLE trn_case ADD COLUMN referral_source VARCHAR(255)")
            altered = True

        case_alter_statements = {
            "customer_name": "ALTER TABLE trn_case ADD COLUMN customer_name VARCHAR(255)",
            "company_name": "ALTER TABLE trn_case ADD COLUMN company_name VARCHAR(255)",
            "region_id": "ALTER TABLE trn_case ADD COLUMN region_id INTEGER",
            "unit_head_id": "ALTER TABLE trn_case ADD COLUMN unit_head_id INTEGER",
            "sales_manager_id": "ALTER TABLE trn_case ADD COLUMN sales_manager_id INTEGER",
            "confirmed_by_bank_date": "ALTER TABLE trn_case ADD COLUMN confirmed_by_bank_date DATE",
            "total_disbursement_amount": "ALTER TABLE trn_case ADD COLUMN total_disbursement_amount FLOAT",
            "remarks": "ALTER TABLE trn_case ADD COLUMN remarks TEXT",
            "is_cancelled": "ALTER TABLE trn_case ADD COLUMN is_cancelled BOOLEAN DEFAULT 0",
        }
        for col_name, alter_sql in case_alter_statements.items():
            if col_name not in case_columns:
                conn.execute(alter_sql)
                altered = True

        revenue_columns = _table_columns("trn_revenue")
        if "rate_percent" not in revenue_columns:
            conn.execute("ALTER TABLE trn_revenue ADD COLUMN rate_percent FLOAT")
            altered = True
        if "gross_amount" not in revenue_columns:
            conn.execute("ALTER TABLE trn_revenue ADD COLUMN gross_amount FLOAT")
            altered = True

        commission_columns = _table_columns("trn_commission")
        commission_alter_statements = {
            "rate_percent": "ALTER TABLE trn_commission ADD COLUMN rate_percent FLOAT",
            "gross_amount": "ALTER TABLE trn_commission ADD COLUMN gross_amount FLOAT",
            "payment_request_date": "ALTER TABLE trn_commission ADD COLUMN payment_request_date DATE",
            "payment_paid_date": "ALTER TABLE trn_commission ADD COLUMN payment_paid_date DATE",
            "utr_number": "ALTER TABLE trn_commission ADD COLUMN utr_number VARCHAR(255)",
            "advance_paid": "ALTER TABLE trn_commission ADD COLUMN advance_paid FLOAT",
            "advance_date": "ALTER TABLE trn_commission ADD COLUMN advance_date DATE",
            "recovery_made": "ALTER TABLE trn_commission ADD COLUMN recovery_made FLOAT",
            "recovery_date": "ALTER TABLE trn_commission ADD COLUMN recovery_date DATE",
        }
        for col_name, alter_sql in commission_alter_statements.items():
            if col_name not in commission_columns:
                conn.execute(alter_sql)
                altered = True

        expense_columns = _table_columns("trn_expense")
        expense_alter_statements = {
            "invoice_date": "ALTER TABLE trn_expense ADD COLUMN invoice_date DATE",
            "payment_date": "ALTER TABLE trn_expense ADD COLUMN payment_date DATE",
            "utr_number": "ALTER TABLE trn_expense ADD COLUMN utr_number VARCHAR(255)",
            "gross_amount": "ALTER TABLE trn_expense ADD COLUMN gross_amount FLOAT",
        }
        for col_name, alter_sql in expense_alter_statements.items():
            if col_name not in expense_columns:
                conn.execute(alter_sql)
                altered = True

        employee_columns = {row[1] for row in conn.execute("PRAGMA table_info(mst_employee)").fetchall()}
        employee_alter_statements = {
            "gender": "ALTER TABLE mst_employee ADD COLUMN gender VARCHAR(20)",
            "date_of_birth": "ALTER TABLE mst_employee ADD COLUMN date_of_birth DATE",
            "father_name": "ALTER TABLE mst_employee ADD COLUMN father_name VARCHAR(255)",
            "marital_status": "ALTER TABLE mst_employee ADD COLUMN marital_status VARCHAR(50)",
            "pan": "ALTER TABLE mst_employee ADD COLUMN pan VARCHAR(20)",
            "aadhar_number": "ALTER TABLE mst_employee ADD COLUMN aadhar_number VARCHAR(30)",
            "address": "ALTER TABLE mst_employee ADD COLUMN address TEXT",
            "date_of_joining": "ALTER TABLE mst_employee ADD COLUMN date_of_joining DATE",
            "team_name": "ALTER TABLE mst_employee ADD COLUMN team_name VARCHAR(100)",
            "pf_applicable": "ALTER TABLE mst_employee ADD COLUMN pf_applicable BOOLEAN DEFAULT 0",
            "esic_applicable": "ALTER TABLE mst_employee ADD COLUMN esic_applicable BOOLEAN DEFAULT 0",
            "bank_name": "ALTER TABLE mst_employee ADD COLUMN bank_name VARCHAR(100)",
            "bank_account_number": "ALTER TABLE mst_employee ADD COLUMN bank_account_number VARCHAR(50)",
            "bank_ifsc": "ALTER TABLE mst_employee ADD COLUMN bank_ifsc VARCHAR(20)",
            "uan_number": "ALTER TABLE mst_employee ADD COLUMN uan_number VARCHAR(30)",
        }
        for col_name, alter_sql in employee_alter_statements.items():
            if col_name not in employee_columns:
                conn.execute(alter_sql)
                altered = True

        connector_columns = _table_columns("mst_connector")
        if "connector_name" not in connector_columns:
            conn.execute("ALTER TABLE mst_connector ADD COLUMN connector_name VARCHAR(255)")
            altered = True

        # INTEL-1 compatibility columns for existing SQLite databases.
        _ensure_column("mst_lender", "default_gst_rate", "ALTER TABLE mst_lender ADD COLUMN default_gst_rate NUMERIC(5,2) DEFAULT 0")
        _ensure_column("mst_lender", "default_tds_rate", "ALTER TABLE mst_lender ADD COLUMN default_tds_rate NUMERIC(5,2) DEFAULT 0")
        _ensure_column("mst_lender", "max_commission", "ALTER TABLE mst_lender ADD COLUMN max_commission NUMERIC(15,2)")
        _ensure_column("mst_lender", "metadata", "ALTER TABLE mst_lender ADD COLUMN metadata JSON DEFAULT '{}' ")

        _ensure_column("mst_connector", "default_gst_rate", "ALTER TABLE mst_connector ADD COLUMN default_gst_rate NUMERIC(5,2) DEFAULT 0")
        _ensure_column("mst_connector", "default_tds_rate", "ALTER TABLE mst_connector ADD COLUMN default_tds_rate NUMERIC(5,2) DEFAULT 0")
        _ensure_column("mst_connector", "max_commission", "ALTER TABLE mst_connector ADD COLUMN max_commission NUMERIC(15,2)")
        _ensure_column("mst_connector", "metadata", "ALTER TABLE mst_connector ADD COLUMN metadata JSON DEFAULT '{}' ")

        _ensure_column("trn_revenue", "party_id", "ALTER TABLE trn_revenue ADD COLUMN party_id INTEGER")
        _ensure_column("trn_revenue", "reported_amount", "ALTER TABLE trn_revenue ADD COLUMN reported_amount NUMERIC(15,2)")
        _ensure_column("trn_revenue", "reported_gst", "ALTER TABLE trn_revenue ADD COLUMN reported_gst NUMERIC(15,2) DEFAULT 0")
        _ensure_column("trn_revenue", "reported_tds", "ALTER TABLE trn_revenue ADD COLUMN reported_tds NUMERIC(15,2) DEFAULT 0")
        _ensure_column("trn_revenue", "reported_net", "ALTER TABLE trn_revenue ADD COLUMN reported_net NUMERIC(15,2)")
        _ensure_column("trn_revenue", "system_gst", "ALTER TABLE trn_revenue ADD COLUMN system_gst NUMERIC(15,2) DEFAULT 0")
        _ensure_column("trn_revenue", "system_tds", "ALTER TABLE trn_revenue ADD COLUMN system_tds NUMERIC(15,2) DEFAULT 0")
        _ensure_column("trn_revenue", "gst_match", "ALTER TABLE trn_revenue ADD COLUMN gst_match BOOLEAN DEFAULT 0")
        _ensure_column("trn_revenue", "tds_match", "ALTER TABLE trn_revenue ADD COLUMN tds_match BOOLEAN DEFAULT 0")
        _ensure_column("trn_revenue", "data", "ALTER TABLE trn_revenue ADD COLUMN data JSON DEFAULT '{}' ")

        _ensure_column("trn_commission", "party_id", "ALTER TABLE trn_commission ADD COLUMN party_id INTEGER")
        _ensure_column("trn_commission", "reported_commission", "ALTER TABLE trn_commission ADD COLUMN reported_commission NUMERIC(15,2)")
        _ensure_column("trn_commission", "reported_gst", "ALTER TABLE trn_commission ADD COLUMN reported_gst NUMERIC(15,2) DEFAULT 0")
        _ensure_column("trn_commission", "reported_tds", "ALTER TABLE trn_commission ADD COLUMN reported_tds NUMERIC(15,2) DEFAULT 0")
        _ensure_column("trn_commission", "reported_net", "ALTER TABLE trn_commission ADD COLUMN reported_net NUMERIC(15,2)")
        _ensure_column("trn_commission", "exceeds_max", "ALTER TABLE trn_commission ADD COLUMN exceeds_max BOOLEAN DEFAULT 0")
        _ensure_column("trn_commission", "gst_match", "ALTER TABLE trn_commission ADD COLUMN gst_match BOOLEAN DEFAULT 0")
        _ensure_column("trn_commission", "tds_match", "ALTER TABLE trn_commission ADD COLUMN tds_match BOOLEAN DEFAULT 0")
        _ensure_column("trn_commission", "data", "ALTER TABLE trn_commission ADD COLUMN data JSON DEFAULT '{}' ")

        _ensure_column("trn_payment", "case_id", "ALTER TABLE trn_payment ADD COLUMN case_id INTEGER")
        _ensure_column("trn_payment", "party_id", "ALTER TABLE trn_payment ADD COLUMN party_id INTEGER")
        _ensure_column("trn_payment", "amount", "ALTER TABLE trn_payment ADD COLUMN amount NUMERIC(15,2)")
        _ensure_column("trn_payment", "mode", "ALTER TABLE trn_payment ADD COLUMN mode VARCHAR(50)")
        _ensure_column("trn_payment", "data", "ALTER TABLE trn_payment ADD COLUMN data JSON DEFAULT '{}' ")

        commission_rule_columns = _table_columns("rul_commission_rule")
        commission_rule_alter_statements = {
            "connector_share_percent": "ALTER TABLE rul_commission_rule ADD COLUMN connector_share_percent FLOAT",
            "clawback_period_months": "ALTER TABLE rul_commission_rule ADD COLUMN clawback_period_months INTEGER",
            "clawback_percent": "ALTER TABLE rul_commission_rule ADD COLUMN clawback_percent FLOAT",
        }
        for col_name, alter_sql in commission_rule_alter_statements.items():
            if col_name not in commission_rule_columns:
                conn.execute(alter_sql)
                altered = True

        commission_slab_columns = _table_columns("rul_commission_slab")
        if "connector_share" not in commission_slab_columns:
            conn.execute("ALTER TABLE rul_commission_slab ADD COLUMN connector_share FLOAT")
            altered = True

        columns = {row[1] for row in conn.execute("PRAGMA table_info(etl_import_batch)").fetchall()}
        if "file_hash" not in columns:
            conn.execute("ALTER TABLE etl_import_batch ADD COLUMN file_hash VARCHAR(64)")
            conn.execute("CREATE INDEX IF NOT EXISTS ix_etl_import_batch_file_hash ON etl_import_batch (file_hash)")
            altered = True

        if altered:
            conn.commit()
    finally:
        conn.close()

    if _is_truthy(os.getenv("ALERT_SCHEDULER_ENABLED", "0")):
        alert_scheduler.start()

    db = SessionLocal()
    try:
        seed_fixed_templates(db)
    finally:
        db.close()


@app.on_event("shutdown")
def shutdown_event():
    if _is_truthy(os.getenv("ALERT_SCHEDULER_ENABLED", "0")):
        alert_scheduler.stop()

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
