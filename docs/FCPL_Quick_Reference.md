# FCPL Pilot - Quick Reference

## URLs

- Upload page: `http://localhost:8000/masters/etl/upload`
- Pilot report: `http://localhost:8000/masters/reports/pilot`
- Swagger: `http://localhost:8000/docs`

## Commands

- Validate staging: `python scripts/validate_staging.py`
- Promote staging: `python scripts/promote_staging.py`

## Expected Input Files

- `FCPL_Connector_Master.xlsx`
- `FCPL_Lender_Payout.xlsx`
- `FCPL_Secured_Tracker.xlsx`

## ETL API Endpoints

- `GET /api/v1/etl/batches`
- `GET /api/v1/etl/staging`
- `GET /api/v1/etl/staging/connectors`
- `GET /api/v1/etl/staging/lenders`
- `GET /api/v1/etl/staging/cases`
- `GET /api/v1/etl/errors`
- `POST /api/v1/etl/promote`