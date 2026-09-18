from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.core.templates import Jinja2Templates
import sqlite3
from pathlib import Path
import os

from src.core.database import Base, engine, SessionLocal
from src.core.contract import contract_version
from src.core.ai_feedback_guards import set_ai_feedback_guards_framework_enabled
from src.core.bi_configuration_guards import set_bi_configuration_guards_framework_enabled
from src.core.bi_consumption_guards import set_bi_consumption_guards_framework_enabled
from src.core.command_governance_guards import set_command_governance_guards_framework_enabled
from src.core.decision_governance_guards import set_decision_governance_guards_framework_enabled
from src.core.etl_pipeline_guards import set_etl_pipeline_guards_framework_enabled
from src.core.financial_config_guards import set_financial_config_guards_framework_enabled
from src.core.integration_connectors_guards import set_integration_connectors_guards_framework_enabled
from src.core.rule_governance_guards import set_rule_governance_guards_framework_enabled
from src.core.scope import set_scope_framework_enabled
from src.core.system_database_guards import set_system_database_guards_framework_enabled
from src.core.system_ops_guards import set_system_ops_guards_framework_enabled
from src.core.template_catalog_guards import set_template_catalog_guards_framework_enabled
from src.core.template_governance_guards import set_template_governance_guards_framework_enabled
from src.core.universal_data_guards import set_universal_data_guards_framework_enabled
from src.admin.api import mapping as mapping_router
from src.admin.api import dashboards as admin_dashboards_router
from src.admin.api import pnl_policy as admin_pnl_policy_router
from src.admin.api import reconciliation_policy as admin_reconciliation_policy_router
from src.admin.api import rules as admin_rules_router
from src.admin.api import templates as admin_templates_router
from src.ai.api import router as ai_feedback_router
from src.alerts.api import alerts as alerts_router
from src.alerts import models as alerts_models  # noqa: F401
from src.budget.api import budget as budget_router
from src.budget import models as budget_models  # noqa: F401
from src.command.api import compliance as command_compliance_router
from src.command.api import dashboard as command_dashboard_router
from src.command.api import governance as command_governance_router
from src.command.api import preferences as command_preferences_router
from src.command import models as command_models  # noqa: F401
from src.decision.api import ml as decision_ml_router
from src.decision.api import pipeline as decision_pipeline_router
from src.decision.api import rules as decision_rules_router
from src.decision.api import workflows as decision_workflows_router
from src.decision import models as decision_models  # noqa: F401
from src.alerts.services.scheduler import scheduler as alert_scheduler
from src.bi.api import dashboards as bi_dashboards_router
from src.bi.api import pnl_phase1 as bi_pnl_phase1_router
from src.bi.api import portfolio_health as bi_portfolio_health_router
from src.bi.api import phase1_exports as bi_phase1_exports_router
from src.bi.api import reports as bi_reports_router
from src.bi.api import trends as bi_trends_router
from src.bi.api import working_capital as bi_working_capital_router
from src.confidence.api import scores as confidence_scores_router
from src.confidence import models as confidence_models  # noqa: F401
from src.integration.api import connectors as integration_connectors_router
from src.integration import models as integration_models  # noqa: F401
from src.gateway.middleware import rate_limit_middleware
from src.masters.api import case, commission, connector as agent, customer, dashboard, document, dsa, employee, etl, expense, lender, payment, product, redflags, revenue, tenant as tenant_api
from src.masters.ui import routes as ui_routes
from src.masters.ui import routes_dsa
from src.masters.ui import routes_5_1, routes_5_2, routes_5_3, routes_5_4, routes_5_5, routes_data_ops, routes_etl, routes_tenant
from src.masters.api.tally import router as tally_api_router
from src.metadata import models as metadata_models  # noqa: F401
from src.ai import models as ai_models  # noqa: F401
from src.bi import models as bi_models  # noqa: F401
from src.reference import models as reference_models  # noqa: F401
from src.reconciliation.api import reconciliation as reconciliation_router
from src.reconciliation.api import reports as reconciliation_reports_router
from src.reconciliation import models as reconciliation_models  # noqa: F401
from src.rules.api import test_sandbox as validation_sandbox_router
from src.rules.api import validation as validation_router
from src.rules import models as rules_models  # noqa: F401
from src.security.api import auth as auth_router
from src.security import models as security_models  # noqa: F401
from scripts.seed_validation_rules import seed_rules as _seed_validation_rules
from src.system.api import backup as system_backup_router
from src.system.api import config as system_config_router
from src.system.api import database as system_database_router
from src.system.api import health as system_health_router
from src.system.api import tenant as system_tenant_router
from src.system import models as system_models  # noqa: F401
from src.system.services.artifact_cleanup import cleanup_artifact_scope
from src.system.services.database_registry import bootstrap_database_registry
from src.system.services.hierarchy import ensure_owner_industry_tenant_structure

app = FastAPI()
app.middleware("http")(rate_limit_middleware)

APP_CONTRACT_VERSION = contract_version()
LEGACY_RULE_ROUTES_FLAG = "ODOS_ENABLE_LEGACY_RULE_ROUTES"


def _is_truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "on"}


def _is_test_runtime() -> bool:
    if _is_truthy(os.getenv("ODOS_TEST_MODE", "0")):
        return True
    if os.getenv("PYTEST_CURRENT_TEST"):
        return True
    return False


def _sqlite_database_path(db_url: str) -> Path | None:
    if not db_url.startswith("sqlite:///"):
        return None
    raw_path = db_url.split("sqlite:///", 1)[-1].strip()
    if not raw_path or raw_path == ":memory:":
        return None
    return Path(raw_path).resolve()


def _sqlite_table_exists(db_path: Path | None, table_name: str) -> bool:
    if db_path is None or not db_path.exists():
        return False

    conn = sqlite3.connect(str(db_path))
    try:
        row = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name = ?",
            (table_name,),
        ).fetchone()
        return row is not None
    finally:
        conn.close()


def _is_business_schema_guard_enabled() -> bool:
    return _is_truthy(os.getenv("ODOS_ENABLE_BUSINESS_SCHEMA_FAILFAST", "1"))


def _business_schema_guard(path: str, db_path: Path | None) -> dict[str, str] | None:
    guard_rules = (
        ("/api/v1/etl", "etl_import_batch", "ETL runtime schema is disabled in this environment"),
        ("/api/masters/cases", "trn_case", "Case transaction schema is disabled in this environment"),
        ("/api/masters/revenue", "trn_revenue", "Revenue transaction schema is disabled in this environment"),
        ("/api/masters/commission", "trn_commission", "Commission transaction schema is disabled in this environment"),
        ("/api/masters/expenses", "trn_expense", "Expense transaction schema is disabled in this environment"),
        ("/api/masters/payments", "trn_payment", "Payment transaction schema is disabled in this environment"),
        ("/api/masters/tally", "trn_tally_export_batch", "Tally export transaction schema is disabled in this environment"),
        ("/api/masters/customers", "mst_customer", "Customer master schema is disabled in this environment"),
        ("/api/masters/lenders", "mst_lender", "Lender master schema is disabled in this environment"),
        ("/api/masters/products", "mst_product", "Product master schema is disabled in this environment"),
        ("/api/masters/employees", "mst_employee", "Employee master schema is disabled in this environment"),
        ("/api/masters/agents", "mst_agent", "Agent master schema is disabled in this environment"),
    )

    for prefix, required_table, message in guard_rules:
        if path.startswith(prefix) and not _sqlite_table_exists(db_path, required_table):
            return {
                "status": "error",
                "error_code": "BUSINESS_SCHEMA_DISABLED",
                "message": message,
                "missing_table": required_table,
                "path_prefix": prefix,
            }

    return None

cors_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ALLOW_ORIGINS",
        "http://localhost:3000,http://localhost:3001,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:3001,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def attach_contract_header(request: Request, call_next):
    if request.method.upper() == "OPTIONS":
        response = await call_next(request)
        if request.url.path.startswith("/api/"):
            response.headers["X-ODOS-Contract-Version"] = APP_CONTRACT_VERSION
        return response

    db_path = _sqlite_database_path(str(engine.url))
    if _is_business_schema_guard_enabled() and request.url.path.startswith("/api/"):
        payload = _business_schema_guard(request.url.path, db_path)
        if payload is not None:
            response = JSONResponse(status_code=409, content=payload)
            response.headers["X-ODOS-Contract-Version"] = APP_CONTRACT_VERSION
            return response

    response = await call_next(request)
    if request.url.path.startswith("/api/"):
        response.headers["X-ODOS-Contract-Version"] = APP_CONTRACT_VERSION
    return response


@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}

templates = Jinja2Templates(directory="src/templates")
app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(customer.router)
app.include_router(dsa.router)
app.include_router(tenant_api.router)
app.include_router(lender.router)
app.include_router(product.router)
app.include_router(employee.router)
app.include_router(agent.router)
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
app.include_router(admin_templates_router.router)
app.include_router(admin_reconciliation_policy_router.router)
app.include_router(admin_pnl_policy_router.router)
app.include_router(admin_rules_router.router)
app.include_router(admin_dashboards_router.router)
app.include_router(ai_feedback_router)
app.include_router(validation_router.router)
app.include_router(validation_sandbox_router.router)
app.include_router(reconciliation_router.router)
app.include_router(reconciliation_reports_router.router)
app.include_router(budget_router.router)
app.include_router(confidence_scores_router.router)
app.include_router(bi_reports_router.router)
app.include_router(bi_dashboards_router.router)
app.include_router(bi_pnl_phase1_router.router)
app.include_router(bi_working_capital_router.router)
app.include_router(bi_portfolio_health_router.router)
app.include_router(bi_phase1_exports_router.router)
app.include_router(bi_trends_router.router)
app.include_router(command_dashboard_router.router)
app.include_router(command_preferences_router.router)
app.include_router(command_governance_router.router)
app.include_router(command_compliance_router.router)
app.include_router(decision_rules_router.router)
app.include_router(decision_ml_router.router)
app.include_router(decision_workflows_router.router)
app.include_router(decision_pipeline_router.router)
app.include_router(integration_connectors_router.router)
app.include_router(system_health_router.router)
app.include_router(system_backup_router.router)
app.include_router(system_tenant_router.router)
app.include_router(system_config_router.router)
app.include_router(system_database_router.router)
app.include_router(auth_router.router)
app.include_router(ui_routes.router)
app.include_router(routes_dsa.router)
app.include_router(routes_tenant.router)
app.include_router(routes_5_1.router)
app.include_router(routes_5_2.router)
app.include_router(routes_5_3.router)
app.include_router(routes_5_4.router)
app.include_router(routes_5_5.router)
app.include_router(routes_etl.router)
app.include_router(routes_data_ops.router)

if _is_truthy(os.getenv(LEGACY_RULE_ROUTES_FLAG, "0")):
    from src.rules.api import rules as legacy_rules_router
    from src.masters.ui import routes_rules as legacy_routes_rules

    app.include_router(legacy_rules_router.router)
    app.include_router(legacy_routes_rules.router)


@app.on_event("startup")
def startup_event():
    legacy_rules_enabled = _is_truthy(os.getenv(LEGACY_RULE_ROUTES_FLAG, "0"))
    print(f"[startup] legacy_rule_routes={'ENABLED' if legacy_rules_enabled else 'DISABLED'} ({LEGACY_RULE_ROUTES_FLAG})")

    # NEW FRAMEWORK: Pillar 1 scope contract remains disabled by default.
    set_scope_framework_enabled(_is_truthy(os.getenv("ODOS_ENABLE_CORE_SCOPE_FRAMEWORK", "0")))

    # NEW FRAMEWORK: Pillar 3 universal validation/reconciliation guards remain disabled by default.
    set_universal_data_guards_framework_enabled(_is_truthy(os.getenv("ODOS_ENABLE_UNIVERSAL_DATA_GUARDS", "0")))

    # NEW FRAMEWORK: Pillar 4 ETL validate/promote/reconcile guards remain disabled by default.
    set_etl_pipeline_guards_framework_enabled(_is_truthy(os.getenv("ODOS_ENABLE_ETL_PIPELINE_GUARDS", "0")))

    # NEW FRAMEWORK: Pillar 5 BI consumption guards remain disabled by default.
    set_bi_consumption_guards_framework_enabled(_is_truthy(os.getenv("ODOS_ENABLE_BI_CONSUMPTION_GUARDS", "0")))

    # NEW FRAMEWORK: Pillar 12 BI configuration guards remain disabled by default.
    set_bi_configuration_guards_framework_enabled(_is_truthy(os.getenv("ODOS_ENABLE_BI_CONFIGURATION_GUARDS", "0")))

    # NEW FRAMEWORK: Pillar 6 AI feedback guards remain disabled by default.
    set_ai_feedback_guards_framework_enabled(_is_truthy(os.getenv("ODOS_ENABLE_AI_FEEDBACK_GUARDS", "0")))

    # NEW FRAMEWORK: Pillar 7 system operations guards remain disabled by default.
    set_system_ops_guards_framework_enabled(_is_truthy(os.getenv("ODOS_ENABLE_SYSTEM_OPS_GUARDS", "0")))

    # NEW FRAMEWORK: Pillar 8 system database guards remain disabled by default.
    set_system_database_guards_framework_enabled(_is_truthy(os.getenv("ODOS_ENABLE_SYSTEM_DATABASE_GUARDS", "0")))

    # NEW FRAMEWORK: Pillar 9 rule governance guards remain disabled by default.
    set_rule_governance_guards_framework_enabled(_is_truthy(os.getenv("ODOS_ENABLE_RULE_GOVERNANCE_GUARDS", "0")))

    # NEW FRAMEWORK: Pillar 10 template governance guards remain disabled by default.
    set_template_governance_guards_framework_enabled(_is_truthy(os.getenv("ODOS_ENABLE_TEMPLATE_GOVERNANCE_GUARDS", "0")))

    # NEW FRAMEWORK: Pillar 11 template catalog guards remain disabled by default.
    set_template_catalog_guards_framework_enabled(_is_truthy(os.getenv("ODOS_ENABLE_TEMPLATE_CATALOG_GUARDS", "0")))

    # NEW FRAMEWORK: Pillar 13 decision governance guards remain disabled by default.
    set_decision_governance_guards_framework_enabled(_is_truthy(os.getenv("ODOS_ENABLE_DECISION_GOVERNANCE_GUARDS", "0")))

    # NEW FRAMEWORK: Pillar 14 integration connector guards remain disabled by default.
    set_integration_connectors_guards_framework_enabled(_is_truthy(os.getenv("ODOS_ENABLE_INTEGRATION_CONNECTORS_GUARDS", "0")))

    # NEW FRAMEWORK: Pillar 15 command governance guards remain disabled by default.
    set_command_governance_guards_framework_enabled(_is_truthy(os.getenv("ODOS_ENABLE_COMMAND_GOVERNANCE_GUARDS", "0")))

    # NEW FRAMEWORK: Pillar 16 financial configuration guards remain disabled by default.
    set_financial_config_guards_framework_enabled(_is_truthy(os.getenv("ODOS_ENABLE_FINANCIAL_CONFIG_GUARDS", "0")))

    startup_create_all_enabled = _is_truthy(os.getenv("ODOS_ENABLE_STARTUP_CREATE_ALL", "0"))
    if startup_create_all_enabled:
        Base.metadata.create_all(bind=engine)

    db_path = _sqlite_database_path(str(engine.url))
    is_test_runtime = _is_test_runtime()
    skip_bootstrap = is_test_runtime or _is_truthy(os.getenv("ODOS_SKIP_STARTUP_BOOTSTRAP", "0"))

    if db_path is not None and not skip_bootstrap:
        ensure_owner_industry_tenant_structure(db_path)

    if not skip_bootstrap and _is_truthy(os.getenv("ALERT_SCHEDULER_ENABLED", "0")):
        alert_scheduler.start()

    if not skip_bootstrap:
        db = SessionLocal()
        try:
            if _is_truthy(os.getenv("ODOS_AUTO_ARTIFACT_CLEANUP", "1")):
                cleanup_artifact_scope(db, requested_by=None)
            else:
                bootstrap_database_registry(db)
            admin_templates_router.ensure_canonical_metadata_templates(db, updated_by="startup")
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

        try:
            _seed_validation_rules()
        except Exception:
            pass  # Never block startup if validation rules seed fails


@app.on_event("shutdown")
def shutdown_event():
    if _is_truthy(os.getenv("ALERT_SCHEDULER_ENABLED", "0")):
        alert_scheduler.stop()

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
