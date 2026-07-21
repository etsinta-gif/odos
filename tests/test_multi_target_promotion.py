import json
from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import inspect

from app.main import app
from src.core.database import Base, SessionLocal, engine
from src.metadata.models import META_ImportTemplate
from src.transactions.models import ETL_DataLineage, ETL_ImportBatch, ETL_StagingRawData


def setup_module(module):
    Base.metadata.create_all(bind=engine)


def _auth_headers(client: TestClient) -> dict[str, str]:
    username = f"etl_{uuid4().hex[:8]}"
    password = "Admin@12345"
    register_payload = {
        "dsa_code": f"ET{uuid4().hex[:6].upper()}",
        "dsa_name": "ETL Test DSA",
        "username": username,
        "password": password,
    }
    register = client.post("/api/auth/register", json=register_payload)
    assert register.status_code == 200

    login = client.post("/api/auth/login", json={"username": username, "password": password})
    assert login.status_code == 200
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_multi_target_support_detector() -> None:
    from src.etl.services.promoter import supports_multi_target

    mappings = [
        {"target_table": "MST_Lender", "target_field": "lender_name", "source_column": "Lender / NBFC"},
        {"target_table": "MST_Product", "target_field": "sub_product", "source_column": "Sub-product"},
    ]
    assert supports_multi_target(mappings) is True


def test_promote_batch_returns_error_without_template_id() -> None:
    from src.etl.services.promoter import promote_batch

    db = SessionLocal()
    try:
        batch = ETL_ImportBatch(
            batch_guid="test-no-template-id",
            company_id=1,
            source_system="TEST",
            file_name="missing.xlsx",
            import_status="STAGED",
            is_complete=False,
            total_rows=0,
            successful_rows=0,
            failed_rows=0,
        )
        db.add(batch)
        db.commit()

        result = promote_batch(db, batch.batch_guid, "SKIP")
        assert result["error"] == "Batch template_id is not set"
    finally:
        db.query(ETL_ImportBatch).filter(ETL_ImportBatch.batch_guid == "test-no-template-id").delete()
        db.commit()
        db.close()


def test_fcpl_lender_file_upload_sets_template_id_when_template_matches() -> None:
    src = Path("samples/FCPL_Lender_Payout_N_Master.xlsx")
    if not src.exists():
        return

    db = SessionLocal()
    try:
        template = db.query(META_ImportTemplate).filter(META_ImportTemplate.template_id == 16).first()
        if template is None:
            return

        client = TestClient(app)
        headers = _auth_headers(client)
        upload = client.post(
            "/api/v1/etl/upload",
            files={"file": (src.name, src.read_bytes(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
            data={"entity_type": "MST_Lender"},
            headers=headers,
        )
        assert upload.status_code == 200
        payload = upload.json()
        assert payload["template_id"] == 16

        batch = db.query(ETL_ImportBatch).filter(ETL_ImportBatch.batch_guid == payload["batch_guid"]).first()
        assert batch is not None
        assert batch.template_id == 16

        rows = db.query(ETL_StagingRawData).filter(ETL_StagingRawData.batch_guid == payload["batch_guid"]).all()
        assert rows
        sample = json.loads(rows[0].source_value or rows[0].stored_value or "{}")
        assert "Lender / NBFC" in sample or "DSA Code" in sample
    finally:
        inspector = inspect(engine)
        if "etl_data_lineage" in inspector.get_table_names():
            db.query(ETL_DataLineage).filter(ETL_DataLineage.batch_guid.like("%")).delete()
        db.query(ETL_StagingRawData).filter(ETL_StagingRawData.batch_guid.like("%")).delete()
        db.query(ETL_ImportBatch).filter(ETL_ImportBatch.file_name == "FCPL_Lender_Payout_N_Master.xlsx").delete()
        db.commit()
        db.close()