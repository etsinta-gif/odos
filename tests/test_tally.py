import os
import json
import gc
from datetime import date
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app
from src.core.database import Base, engine, SessionLocal
from src.transactions.models import TRN_TallyExportBatch

client = TestClient(app)


def _auth_headers() -> dict[str, str]:
    username = f"tally_{uuid4().hex[:8]}"
    password = "Admin@12345"
    register_payload = {
        "dsa_code": f"TD{uuid4().hex[:6].upper()}",
        "dsa_name": "Tally Test DSA",
        "username": username,
        "password": password,
    }
    register = client.post("/api/auth/register", json=register_payload)
    assert register.status_code == 200

    login = client.post("/api/auth/login", json={"username": username, "password": password})
    assert login.status_code == 200
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def setup_module(module):
    Base.metadata.create_all(bind=engine)


def teardown_module(module):
    client.close()
    gc.collect()
    engine.dispose()
    for _ in range(5):
        try:
            os.remove("odos.db")
            break
        except FileNotFoundError:
            break
        except PermissionError:
            continue


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in (response.headers.get("content-type") or "")
    assert "<html" in response.text.lower()


def test_create_export_batch():
    headers = _auth_headers()
    payload = {
        "batch_name": "Test Batch",
        "export_type": "ALL",
        "period_start": str(date.today()),
        "period_end": str(date.today()),
        "notes": "Integration test batch",
    }
    response = client.post("/api/masters/tally/exports", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["batch_name"] == "Test Batch"


def test_list_export_batches():
    headers = _auth_headers()
    response = client.get("/api/masters/tally/exports", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_export_batch():
    headers = _auth_headers()
    batch = SessionLocal().query(TRN_TallyExportBatch).first()
    response = client.get(f"/api/masters/tally/exports/{batch.batch_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["batch_id"] == batch.batch_id
