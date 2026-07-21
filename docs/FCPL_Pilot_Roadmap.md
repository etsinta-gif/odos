# FCPL Pilot Test - Step-by-Step Execution Roadmap

Document ID: FCPL-PILOT-002
Version: 2.0
Status: Verified against root app entrypoint

## Preconditions

- Start server with: `uvicorn app.main:app --reload`
- Confirm `http://localhost:8000/docs` is reachable
- Keep the three FCPL Excel files ready

## Step 1 - Upload Files

1. Open `http://localhost:8000/masters/etl/upload`
2. Upload `FCPL_Connector_Master.xlsx` with entity type `Connector`
3. Upload `FCPL_Lender_Payout.xlsx` with entity type `Lender`
4. Upload `FCPL_Secured_Tracker.xlsx` with entity type `Case`

Expected: each upload creates a batch and stages rows.

## Step 2 - Verify Staging

Use Swagger endpoints:

- `GET /api/v1/etl/staging/connectors`
- `GET /api/v1/etl/staging/lenders`
- `GET /api/v1/etl/staging/cases`

Expected: row totals should match upload sizes.

## Step 3 - Validate Staging

Run:

`python scripts/validate_staging.py`

Optional batch-specific run:

`python scripts/validate_staging.py --batch-guid <batch_guid>`

Expected: no critical errors.

## Step 4 - Promote Records

Run:

`python scripts/promote_staging.py`

Optional batch-specific run:

`python scripts/promote_staging.py --batch-guid <batch_guid>`

Expected: promotion count is greater than zero.

## Step 5 - Verify Master Data

Check these endpoints in Swagger:

- `GET /api/masters/connectors`
- `GET /api/masters/lenders`
- `GET /api/masters/cases`
- `GET /api/masters/revenue`
- `GET /api/masters/commission`

Expected: records present and linked.

## Step 6 - Generate Pilot Report

Open:

`http://localhost:8000/masters/reports/pilot`

Expected: report shows counts and pass message when key tables are populated.