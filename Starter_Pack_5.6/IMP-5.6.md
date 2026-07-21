# IMP-5.6 – Tally Integration (UI & API)

**Document ID:** IMP-5.6
**Version:** 1.0
**Status:** Draft
**Owner:** Aniket
**Sprint:** 5.6
**Phase:** Phase 5 – Operational ERP
**Estimated Duration:** 2 days

---

## Sprint Overview

**Goal:** Build a system to export financial data (Revenue, Commission, Expenses, Payments) to Tally-compatible formats. This enables your Finance team to push data from ODOS into Tally for accounting and reporting.

---

## Prerequisites

- [ ] Sprint 5.5 completed (Expense & Payment Management UI)
- [ ] `TRN_TallyExportBatch` and `TRN_TallyExportDetail` tables exist
- [ ] `MST_TallyMapping` table exists (or create a simplified version)
- [ ] At least one Revenue, Commission, Expense, and Payment record exists

---

## Step 1: Create Tally API Endpoints

Create `src/masters/api/tally.py` with the following code:

```python
# src/masters/api/tally.py
from datetime import date, datetime
import json
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.transactions.models import (
    TRN_TallyExportBatch,
    TRN_TallyExportDetail,
    TRN_Revenue,
    TRN_Commission,
    TRN_Expense,
    TRN_Payment,
)
from src.masters.models import MST_TallyMapping

router = APIRouter(prefix="/api/masters/tally", tags=["Masters"])


class TallyExportBatchCreate(BaseModel):
    batch_name: str
    export_type: str  # REVENUE, COMMISSION, EXPENSE, PAYMENT, ALL
    period_start: date
    period_end: date
    notes: Optional[str] = None


class TallyExportBatchResponse(BaseModel):
    batch_id: int
    batch_name: str
    batch_number: Optional[str]
    export_type: str
    period_start: date
    period_end: date
    total_records: int
    exported_records: int
    export_status: str
    sync_status: str
    file_path: Optional[str]
    notes: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TallyExportDetailResponse(BaseModel):
    detail_id: int
    batch_id: int
    source_table: str
    source_id: int
    exported_data: Optional[str]
    export_status: str
    error_message: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


@router.get("/exports", response_model=List[TallyExportBatchResponse])
def list_export_batches(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    export_type: Optional[str] = None,
    export_status: Optional[str] = None,
    sync_status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(TRN_TallyExportBatch).filter(TRN_TallyExportBatch.is_active == True)
    if export_type:
        query = query.filter(TRN_TallyExportBatch.export_type == export_type)
    if export_status:
        query = query.filter(TRN_TallyExportBatch.export_status == export_status)
    if sync_status:
        query = query.filter(TRN_TallyExportBatch.sync_status == sync_status)
    batches = query.offset(skip).limit(limit).all()
    return batches


@router.get("/exports/{batch_id}", response_model=TallyExportBatchResponse)
def get_export_batch(batch_id: int, db: Session = Depends(get_db)):
    batch = db.query(TRN_TallyExportBatch).filter(TRN_TallyExportBatch.batch_id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Export batch not found")
    return batch


@router.post("/exports", response_model=TallyExportBatchResponse)
def create_export_batch(batch_data: TallyExportBatchCreate, db: Session = Depends(get_db)):
    batch_number = f"TALLY-{datetime.now().strftime('%Y%m%d')}-{datetime.now().strftime('%H%M%S')}"

    new_batch = TRN_TallyExportBatch(
        batch_name=batch_data.batch_name,
        batch_number=batch_number,
        export_type=batch_data.export_type,
        period_start=batch_data.period_start,
        period_end=batch_data.period_end,
        total_records=0,
        exported_records=0,
        export_status="PENDING",
        sync_status="PENDING",
        notes=batch_data.notes,
        is_active=True,
    )
    db.add(new_batch)
    db.commit()
    db.refresh(new_batch)
    return new_batch


@router.post("/exports/{batch_id}/generate")
def generate_export_file(batch_id: int, db: Session = Depends(get_db)):
    batch = db.query(TRN_TallyExportBatch).filter(TRN_TallyExportBatch.batch_id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Export batch not found")

    batch.export_status = "EXPORTING"
    db.commit()

    try:
        batch.exported_records = 0

        if batch.export_type in ["REVENUE", "ALL"]:
            records = db.query(TRN_Revenue).filter(
                TRN_Revenue.revenue_date >= batch.period_start,
                TRN_Revenue.revenue_date <= batch.period_end,
                TRN_Revenue.is_active == True,
            ).all()
            for record in records:
                detail = TRN_TallyExportDetail(
                    batch_id=batch.batch_id,
                    source_table="REVENUE",
                    source_id=record.revenue_id,
                    exported_data=json.dumps({
                        "date": str(record.revenue_date),
                        "amount": record.net_amount,
                        "case_id": record.case_id,
                        "gst": record.gst_amount,
                        "tds": record.tds_amount,
                    }),
                    export_status="COMPLETED",
                )
                db.add(detail)
                batch.exported_records += 1

        if batch.export_type in ["COMMISSION", "ALL"]:
            records = db.query(TRN_Commission).filter(
                TRN_Commission.commission_date >= batch.period_start,
                TRN_Commission.commission_date <= batch.period_end,
                TRN_Commission.is_active == True,
            ).all()
            for record in records:
                detail = TRN_TallyExportDetail(
                    batch_id=batch.batch_id,
                    source_table="COMMISSION",
                    source_id=record.commission_id,
                    exported_data=json.dumps({
                        "date": str(record.commission_date),
                        "amount": record.net_amount,
                        "case_id": record.case_id,
                        "connector_id": record.connector_id,
                    }),
                    export_status="COMPLETED",
                )
                db.add(detail)
                batch.exported_records += 1

        if batch.export_type in ["EXPENSE", "ALL"]:
            records = db.query(TRN_Expense).filter(
                TRN_Expense.expense_date >= batch.period_start,
                TRN_Expense.expense_date <= batch.period_end,
                TRN_Expense.is_active == True,
            ).all()
            for record in records:
                detail = TRN_TallyExportDetail(
                    batch_id=batch.batch_id,
                    source_table="EXPENSE",
                    source_id=record.expense_id,
                    exported_data=json.dumps({
                        "date": str(record.expense_date),
                        "amount": record.net_amount,
                        "category": record.expense_category_id,
                        "description": record.description,
                    }),
                    export_status="COMPLETED",
                )
                db.add(detail)
                batch.exported_records += 1

        if batch.export_type in ["PAYMENT", "ALL"]:
            records = db.query(TRN_Payment).filter(
                TRN_Payment.payment_date >= batch.period_start,
                TRN_Payment.payment_date <= batch.period_end,
                TRN_Payment.is_active == True,
            ).all()
            for record in records:
                detail = TRN_TallyExportDetail(
                    batch_id=batch.batch_id,
                    source_table="PAYMENT",
                    source_id=record.payment_id,
                    exported_data=json.dumps({
                        "date": str(record.payment_date),
                        "amount": record.payment_amount,
                        "mode": record.payment_mode,
                        "utr": record.utr_number,
                    }),
                    export_status="COMPLETED",
                )
                db.add(detail)
                batch.exported_records += 1

        batch.total_records = batch.exported_records
        batch.export_status = "COMPLETED"
        db.commit()

        return {
            "message": "Export file generated successfully",
            "batch_id": batch.batch_id,
            "records_exported": batch.exported_records,
        }

    except Exception as exc:
        batch.export_status = "FAILED"
        db.commit()
        raise HTTPException(status_code=500, detail=f"Export generation failed: {str(exc)}")


@router.post("/exports/{batch_id}/sync")
def sync_to_tally(batch_id: int, db: Session = Depends(get_db)):
    batch = db.query(TRN_TallyExportBatch).filter(TRN_TallyExportBatch.batch_id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Export batch not found")
    if batch.export_status != "COMPLETED":
        raise HTTPException(status_code=400, detail="Batch must be completed before syncing")

    batch.sync_status = "SYNCED"
    db.commit()
    return {"message": "Batch synced to Tally successfully"}


@router.get("/exports/{batch_id}/details", response_model=List[TallyExportDetailResponse])
def get_batch_details(batch_id: int, db: Session = Depends(get_db)):
    details = db.query(TRN_TallyExportDetail).filter(TRN_TallyExportDetail.batch_id == batch_id).all()
    return details


@router.delete("/exports/{batch_id}")
def delete_export_batch(batch_id: int, db: Session = Depends(get_db)):
    batch = db.query(TRN_TallyExportBatch).filter(TRN_TallyExportBatch.batch_id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Export batch not found")
    batch.is_active = False
    db.commit()
    return {"message": "Export batch deleted successfully"}
```

---

## Step 2: Extend UI Routes

Add the following imports in `src/masters/ui/routes.py`:

```python
from src.transactions.models import TRN_TallyExportBatch, TRN_TallyExportDetail
```

Then append these Tally export UI routes after existing routes:

```python
# --------------------------------------------
# Tally export UI routes
# --------------------------------------------

@router.get("/tally/exports")
async def tally_export_list(
    request: Request,
    export_type: Optional[str] = None,
    export_status: Optional[str] = None,
    sync_status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(TRN_TallyExportBatch).filter(TRN_TallyExportBatch.is_active == True)
    if export_type:
        query = query.filter(TRN_TallyExportBatch.export_type == export_type)
    if export_status:
        query = query.filter(TRN_TallyExportBatch.export_status == export_status)
    if sync_status:
        query = query.filter(TRN_TallyExportBatch.sync_status == sync_status)

    batches = query.order_by(TRN_TallyExportBatch.created_at.desc()).all()
    return TEMPLATES.TemplateResponse(
        "masters/tally_batch_list.html",
        {
            "request": request,
            "batches": batches,
            "export_types": ["REVENUE", "COMMISSION", "EXPENSE", "PAYMENT", "ALL"],
            "export_statuses": ["PENDING", "EXPORTING", "COMPLETED", "FAILED"],
            "sync_statuses": ["PENDING", "SYNCED", "FAILED"],
            "selected_export_type": export_type,
            "selected_export_status": export_status,
            "selected_sync_status": sync_status,
        },
    )


@router.get("/tally/exports/add")
async def tally_export_add_form(request: Request):
    return TEMPLATES.TemplateResponse(
        "masters/tally_batch_form.html",
        {
            "request": request,
            "batch": None,
            "action": "add",
            "export_types": ["REVENUE", "COMMISSION", "EXPENSE", "PAYMENT", "ALL"],
        },
    )


@router.post("/tally/exports")
async def tally_export_create(
    request: Request,
    batch_name: str = Form(...),
    export_type: str = Form(...),
    period_start: str = Form(...),
    period_end: str = Form(...),
    notes: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    from src.masters.api.tally import create_export_batch, TallyExportBatchCreate

    batch_data = TallyExportBatchCreate(
        batch_name=batch_name,
        export_type=export_type,
        period_start=date.fromisoformat(period_start),
        period_end=date.fromisoformat(period_end),
        notes=notes,
    )
    batch = create_export_batch(batch_data, db)
    return RedirectResponse(url=f"/masters/tally/exports/{batch.batch_id}", status_code=303)


@router.get("/tally/exports/{batch_id}")
async def tally_export_detail(request: Request, batch_id: int, db: Session = Depends(get_db)):
    from src.masters.api.tally import get_batch_details

    batch = db.query(TRN_TallyExportBatch).filter(TRN_TallyExportBatch.batch_id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Export batch not found")

    details = get_batch_details(batch_id, db)
    return TEMPLATES.TemplateResponse(
        "masters/tally_batch_detail.html",
        {"request": request, "batch": batch, "details": details},
    )


@router.post("/tally/exports/{batch_id}/generate")
async def tally_export_generate(batch_id: int, db: Session = Depends(get_db)):
    from src.masters.api.tally import generate_export_file

    generate_export_file(batch_id, db)
    return RedirectResponse(url=f"/masters/tally/exports/{batch_id}", status_code=303)


@router.post("/tally/exports/{batch_id}/sync")
async def tally_export_sync(batch_id: int, db: Session = Depends(get_db)):
    from src.masters.api.tally import sync_to_tally

    sync_to_tally(batch_id, db)
    return RedirectResponse(url=f"/masters/tally/exports/{batch_id}", status_code=303)


@router.get("/tally/exports/{batch_id}/delete")
async def tally_export_delete(batch_id: int, db: Session = Depends(get_db)):
    from src.masters.api.tally import delete_export_batch

    delete_export_batch(batch_id, db)
    return RedirectResponse(url="/masters/tally/exports", status_code=303)
```

---

## Step 3: Create HTML Templates

Create the following files in `src/templates/masters`.

### `tally_batch_list.html`

```html
{% extends "masters/base.html" %}

{% block title %}Tally Export Batches - ODOS Enterprise{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Tally Export Batches</h1>
    <a href="/masters/tally/exports/add" class="btn btn-primary">Create Export Batch</a>
</div>

<div class="filter-info">
    <form method="GET" action="/masters/tally/exports" class="filter-form">
        <div>
            <label for="export_type">Export Type:</label>
            <select id="export_type" name="export_type">
                <option value="">All</option>
                {% for et in export_types %}
                <option value="{{ et }}" {% if selected_export_type == et %}selected{% endif %}>{{ et }}</option>
                {% endfor %}
            </select>
        </div>
        <div>
            <label for="export_status">Export Status:</label>
            <select id="export_status" name="export_status">
                <option value="">All</option>
                {% for es in export_statuses %}
                <option value="{{ es }}" {% if selected_export_status == es %}selected{% endif %}>{{ es }}</option>
                {% endfor %}
            </select>
        </div>
        <div>
            <label for="sync_status">Sync Status:</label>
            <select id="sync_status" name="sync_status">
                <option value="">All</option>
                {% for ss in sync_statuses %}
                <option value="{{ ss }}" {% if selected_sync_status == ss %}selected{% endif %}>{{ ss }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="filter-actions">
            <button type="submit" class="btn btn-primary">Filter</button>
            <a href="/masters/tally/exports" class="btn btn-secondary">Clear</a>
        </div>
    </form>
</div>

<div class="table-container">
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Batch #</th>
                <th>Name</th>
                <th>Type</th>
                <th>Period</th>
                <th>Records</th>
                <th>Export Status</th>
                <th>Sync Status</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for batch in batches %}
            <tr>
                <td>{{ batch.batch_id }}</td>
                <td>{{ batch.batch_number }}</td>
                <td>{{ batch.batch_name }}</td>
                <td><span class="status-badge status-{{ batch.export_type.lower() }}">{{ batch.export_type }}</span></td>
                <td>{{ batch.period_start }} to {{ batch.period_end }}</td>
                <td>{{ batch.exported_records }}/{{ batch.total_records }}</td>
                <td><span class="status-badge status-{{ batch.export_status.lower() }}">{{ batch.export_status }}</span></td>
                <td><span class="status-badge status-{{ batch.sync_status.lower() }}">{{ batch.sync_status }}</span></td>
                <td>
                    <a href="/masters/tally/exports/{{ batch.batch_id }}" class="btn btn-sm btn-info">View</a>
                    <a href="/masters/tally/exports/{{ batch.batch_id }}/delete" class="btn btn-sm btn-danger" onclick="return confirm('Delete this export batch?')">Delete</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

{% if not batches %}
<div class="empty-state">
    <p>No export batches found.</p>
    <p><a href="/masters/tally/exports/add">Create your first export batch</a></p>
</div>
{% endif %}
{% endblock %}
```

### `tally_batch_form.html`

```html
{% extends "masters/base.html" %}

{% block title %}Create Tally Export Batch - ODOS Enterprise{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Create Export Batch</h1>
    <a href="/masters/tally/exports" class="btn btn-secondary">Back to List</a>
</div>

<form method="POST" action="/masters/tally/exports" class="form-card">
    <div class="form-row">
        <label for="batch_name">Batch Name</label>
        <input type="text" id="batch_name" name="batch_name" required value="{{ batch.batch_name if batch else '' }}">
    </div>
    <div class="form-row">
        <label for="export_type">Export Type</label>
        <select id="export_type" name="export_type" required>
            <option value="">Select type</option>
            {% for et in export_types %}
            <option value="{{ et }}" {% if batch and batch.export_type == et %}selected{% endif %}>{{ et }}</option>
            {% endfor %}
        </select>
    </div>
    <div class="form-row">
        <label for="period_start">Period Start</label>
        <input type="date" id="period_start" name="period_start" required value="{{ batch.period_start if batch else '' }}">
    </div>
    <div class="form-row">
        <label for="period_end">Period End</label>
        <input type="date" id="period_end" name="period_end" required value="{{ batch.period_end if batch else '' }}">
    </div>
    <div class="form-row">
        <label for="notes">Notes</label>
        <textarea id="notes" name="notes">{{ batch.notes if batch else '' }}</textarea>
    </div>
    <div class="form-actions">
        <button type="submit" class="btn btn-primary">Create Batch</button>
    </div>
</form>
{% endblock %}
```

### `tally_batch_detail.html`

```html
{% extends "masters/base.html" %}

{% block title %}Export Batch Detail - ODOS Enterprise{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Export Batch Detail</h1>
    <a href="/masters/tally/exports" class="btn btn-secondary">Back to List</a>
</div>

<div class="detail-card">
    <dl>
        <dt>Batch ID</dt><dd>{{ batch.batch_id }}</dd>
        <dt>Batch Number</dt><dd>{{ batch.batch_number }}</dd>
        <dt>Batch Name</dt><dd>{{ batch.batch_name }}</dd>
        <dt>Export Type</dt><dd>{{ batch.export_type }}</dd>
        <dt>Period</dt><dd>{{ batch.period_start }} to {{ batch.period_end }}</dd>
        <dt>Total Records</dt><dd>{{ batch.total_records }}</dd>
        <dt>Exported Records</dt><dd>{{ batch.exported_records }}</dd>
        <dt>Export Status</dt><dd><span class="status-badge status-{{ batch.export_status.lower() }}">{{ batch.export_status }}</span></dd>
        <dt>Sync Status</dt><dd><span class="status-badge status-{{ batch.sync_status.lower() }}">{{ batch.sync_status }}</span></dd>
        <dt>Notes</dt><dd>{{ batch.notes or '-' }}</dd>
        <dt>Created At</dt><dd>{{ batch.created_at }}</dd>
        <dt>Updated At</dt><dd>{{ batch.updated_at }}</dd>
    </dl>
</div>

<div class="form-actions" style="margin-top: 1rem; gap: 0.5rem; display: flex; flex-wrap: wrap;">
    {% if batch.export_status == 'PENDING' %}
    <form method="POST" action="/masters/tally/exports/{{ batch.batch_id }}/generate">
        <button type="submit" class="btn btn-primary">Generate Export File</button>
    </form>
    {% endif %}
    {% if batch.export_status == 'COMPLETED' and batch.sync_status == 'PENDING' %}
    <form method="POST" action="/masters/tally/exports/{{ batch.batch_id }}/sync">
        <button type="submit" class="btn btn-success">Mark as Synced to Tally</button>
    </form>
    {% endif %}
    <a href="/masters/tally/exports/{{ batch.batch_id }}/delete" class="btn btn-danger" onclick="return confirm('Delete this export batch?')">Delete Batch</a>
</div>

{% if details %}
<hr>
<h2>Exported Records</h2>
<div class="table-container">
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Source Table</th>
                <th>Source ID</th>
                <th>Status</th>
                <th>Preview</th>
                <th>Created At</th>
            </tr>
        </thead>
        <tbody>
            {% for detail in details %}
            <tr>
                <td>{{ detail.detail_id }}</td>
                <td>{{ detail.source_table }}</td>
                <td>{{ detail.source_id }}</td>
                <td><span class="status-badge status-{{ detail.export_status.lower() }}">{{ detail.export_status }}</span></td>
                <td>
                    <button type="button" class="btn btn-sm btn-info" onclick="togglePreview('preview-{{ detail.detail_id }}')">Preview</button>
                    <div id="preview-{{ detail.detail_id }}" style="display:none; margin-top: 0.5rem; background: #fbfbfb; padding: 0.75rem; border-radius: 5px; font-family: monospace; font-size: 0.85rem; white-space: pre-wrap; word-break: break-word;">
                        {{ detail.exported_data or 'No exported data' }}
                    </div>
                </td>
                <td>{{ detail.created_at }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endif %}

<script>
function togglePreview(id) {
  const elem = document.getElementById(id);
  elem.style.display = elem.style.display === 'none' ? 'block' : 'none';
}
</script>
{% endblock %}
```

### `tally_export_preview.html`

```html
{% extends "masters/base.html" %}

{% block title %}Tally Export Preview - ODOS Enterprise{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Export Preview</h1>
    <a href="/masters/tally/exports/{{ batch.batch_id }}" class="btn btn-secondary">Back to Batch</a>
</div>

<div class="detail-card">
    <dl>
        <dt>Batch Name</dt><dd>{{ batch.batch_name }}</dd>
        <dt>Batch Number</dt><dd>{{ batch.batch_number }}</dd>
        <dt>Export Type</dt><dd>{{ batch.export_type }}</dd>
        <dt>Period</dt><dd>{{ batch.period_start }} to {{ batch.period_end }}</dd>
        <dt>Records</dt><dd>{{ details|length }}</dd>
    </dl>
</div>

<div class="table-container" style="margin-top: 1rem;">
    <table>
        <thead>
            <tr>
                <th>#</th>
                <th>Source Table</th>
                <th>Source ID</th>
                <th>Exported Data</th>
            </tr>
        </thead>
        <tbody>
            {% for detail in details %}
            <tr>
                <td>{{ loop.index }}</td>
                <td>{{ detail.source_table }}</td>
                <td>{{ detail.source_id }}</td>
                <td style="font-family: monospace; font-size: 0.8rem; white-space: pre-wrap; word-break: break-word;">{{ detail.exported_data or '-' }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
```

---

## Step 4: Update Base Nav

In `src/templates/masters/base.html`, add:

```html
<li><a href="/masters/tally/exports">Tally Export</a></li>
```

---

## Step 5: Add CSS for Tally Status

Append the following to `src/static/css/style.css`:

```css
.status-revenue { background-color: #3498db; color: white; }
.status-commission { background-color: #9b59b6; color: white; }
.status-expense { background-color: #e74c3c; color: white; }
.status-payment { background-color: #2ecc71; color: white; }
.status-all { background-color: #f39c12; color: white; }

.status-exporting { background-color: #2980b9; color: white; }
.status-completed { background-color: #27ae60; color: white; }
.status-synced { background-color: #2ecc71; color: white; }
``` 

---

## Step 6: Seed Test Data

Create `scripts/seed_test_tally_data.py`:

```python
import json
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import SessionLocal
from src.transactions.models import TRN_TallyExportBatch, TRN_TallyExportDetail


def seed_tally_data(db):
    batches = [
        {
            "batch_name": "April 2026 Tally Export",
            "batch_number": "TALLY-20260430-001",
            "export_type": "ALL",
            "period_start": date(2026, 4, 1),
            "period_end": date(2026, 4, 30),
            "total_records": 4,
            "exported_records": 4,
            "export_status": "COMPLETED",
            "sync_status": "SYNCED",
            "notes": "Full April export",
            "is_active": True,
        },
        {
            "batch_name": "May 2026 Revenue Export",
            "batch_number": "TALLY-20260531-001",
            "export_type": "REVENUE",
            "period_start": date(2026, 5, 1),
            "period_end": date(2026, 5, 31),
            "total_records": 0,
            "exported_records": 0,
            "export_status": "PENDING",
            "sync_status": "PENDING",
            "notes": "Revenue only batch",
            "is_active": True,
        },
    ]

    for batch_data in batches:
        existing = db.query(TRN_TallyExportBatch).filter(
            TRN_TallyExportBatch.batch_number == batch_data["batch_number"]
        ).first()
        if not existing:
            batch = TRN_TallyExportBatch(**batch_data)
            db.add(batch)
            db.flush()

            if batch.export_status == "COMPLETED":
                details = [
                    {
                        "batch_id": batch.batch_id,
                        "source_table": "REVENUE",
                        "source_id": 1,
                        "exported_data": json.dumps({
                            "date": "2026-04-15",
                            "amount": 45000.0,
                            "case_id": 1,
                            "gst": 8100.0,
                            "tds": 4500.0,
                        }),
                        "export_status": "COMPLETED",
                    },
                    {
                        "batch_id": batch.batch_id,
                        "source_table": "COMMISSION",
                        "source_id": 1,
                        "exported_data": json.dumps({
                            "date": "2026-04-20",
                            "amount": 13500.0,
                            "case_id": 1,
                            "connector_id": 1,
                        }),
                        "export_status": "COMPLETED",
                    },
                    {
                        "batch_id": batch.batch_id,
                        "source_table": "EXPENSE",
                        "source_id": 1,
                        "exported_data": json.dumps({
                            "date": "2026-04-01",
                            "amount": 54000.0,
                            "category": 1,
                            "description": "Office rent April 2026",
                        }),
                        "export_status": "COMPLETED",
                    },
                    {
                        "batch_id": batch.batch_id,
                        "source_table": "PAYMENT",
                        "source_id": 1,
                        "exported_data": json.dumps({
                            "date": "2026-04-01",
                            "amount": 54000.0,
                            "mode": "NEFT",
                            "utr": "UTR-20260401001",
                        }),
                        "export_status": "COMPLETED",
                    },
                ]
                for detail_data in details:
                    detail = TRN_TallyExportDetail(**detail_data)
                    db.add(detail)

    db.commit()
    print("✅ Seeded tally export batches and details")


if __name__ == "__main__":
    db = SessionLocal()
    seed_tally_data(db)
    db.close()
```

---

## Step 7: Test Execution

1. Start server: `uvicorn src.main:app --reload`
2. Open `http://localhost:8000/masters/tally/exports`
3. Create a new export batch
4. Generate export file
5. Preview exported data
6. Sync the batch to Tally
7. Delete the batch

---

## Acceptance Criteria

- Tally Export UI and API are available.
- Export batches can be created, generated, previewed, synced, and soft deleted.
- Export statuses transition correctly.
- Export details are created for source records.
- `Tally Export` navigation appears in the master menu.
- Seed script adds sample Tally export batches.

---

**Note:** This implementation is designed as a starter pack. Adjust table names or record fields if your database schema differs.
