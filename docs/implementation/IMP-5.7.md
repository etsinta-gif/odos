# IMP-5.7 - ETL Unblock & Pilot Integration

Date: 2026-07-19

## Objective
Implement and verify an ETL unblock path for FCPL pilot operations, including staging upload, validation, promotion, and pilot reporting visibility.

## 5.7 Changes Incorporated

### Application wiring
- Mounted ETL API router in [app/main.py](app/main.py).
- Mounted ETL UI router in [app/main.py](app/main.py).

### ETL API and UI
- Added ETL API endpoints in [src/masters/api/etl.py](src/masters/api/etl.py):
  - `POST /api/v1/etl/upload`
  - `GET /api/v1/etl/batches`
  - `GET /api/v1/etl/staging`
  - `GET /api/v1/etl/staging/connectors`
  - `GET /api/v1/etl/staging/lenders`
  - `GET /api/v1/etl/staging/cases`
  - `GET /api/v1/etl/errors`
  - `POST /api/v1/etl/promote`
- Added ETL UI routes in [src/masters/ui/routes_etl.py](src/masters/ui/routes_etl.py):
  - `GET /masters/etl/upload`
  - `POST /masters/etl/upload`
  - `GET /masters/reports/pilot`

### Data model additions
- Added ETL transaction-layer models in [src/transactions/models.py](src/transactions/models.py):
  - `ETL_ImportBatch`
  - `ETL_StagingRawData`
  - `ETL_ErrorLog`
  - `ETL_DataLineage`

### UI templates
- Added upload page template [src/templates/masters/etl_upload.html](src/templates/masters/etl_upload.html).
- Added pilot report template [src/templates/masters/pilot_report.html](src/templates/masters/pilot_report.html).

### Operational scripts
- Added staging validation script [scripts/validate_staging.py](scripts/validate_staging.py).
- Added promotion script [scripts/promote_staging.py](scripts/promote_staging.py).

### Dependency updates
- Added `pandas>=2.2.0` and `openpyxl>=3.1.0` to [requirements.txt](requirements.txt).
- Added `pandas>=2.2.0` and `openpyxl>=3.1.0` to [pyproject.toml](pyproject.toml).

### Supporting documentation
- Added rollout guidance [docs/FCPL_Pilot_Roadmap.md](docs/FCPL_Pilot_Roadmap.md).
- Added quick reference [docs/FCPL_Quick_Reference.md](docs/FCPL_Quick_Reference.md).

## Dry-Run Performed

### Dry-run scope
- End-to-end ETL flow executed in local workspace DB:
  1. Upload connector workbook (1 row)
  2. Upload lender workbook (1 row)
  3. Upload case workbook (1 row)
  4. Validate staged rows using [scripts/validate_staging.py](scripts/validate_staging.py)
  5. Promote validated rows using [scripts/promote_staging.py](scripts/promote_staging.py)
  6. Verify post-promotion API behavior on `POST /api/v1/etl/promote`
  7. Verify pilot report UI availability on `GET /masters/reports/pilot`

### Precondition encountered and handled
- Initial dry-run attempt failed because SQLite tables did not yet exist in the workspace-local DB file.
- Applied schema bootstrap (`Base.metadata.create_all(bind=engine)`) and re-ran successfully.

### Batch results
- Connector batch: `925269b8-1e0e-488c-95a8-a43a278f11a4` -> `PROMOTED` (1/1 success)
- Lender batch: `8e993aa7-1c1b-43c6-8125-337bdaa15654` -> `PROMOTED` (1/1 success)
- Case batch: `9c87acca-2ca6-40c0-bc11-23e794967b09` -> `PROMOTED` (1/1 success)

### Validation and promotion outputs
- Validation script exit code: `0` for all 3 batches.
- Validation summary:
  - Connector: `warnings=0, critical_errors=0`
  - Lender: `warnings=1, critical_errors=0`
  - Case: `warnings=0, critical_errors=0`
- Promotion script exit code: `0` for all 3 batches.
- Promotion summary: `Promoted 1 records.` for each batch.

### Functional verification
- Route presence check: all IMP-5.7 ETL API/UI endpoints present.
- Post-promotion API check:
  - `POST /api/v1/etl/promote` returned `400` with `No eligible staged records for this batch` for each processed batch.
  - This is expected after successful promotion and indicates idempotent-safe behavior.
- Pilot UI check:
  - `GET /masters/reports/pilot` returned `200`.

### Data delta (before -> after)
- Connectors: `0 -> 1` (`+1`)
- Lenders: `0 -> 1` (`+1`)
- Cases: `0 -> 1` (`+1`)
- Revenues: `0 -> 1` (`+1`)
- Commissions: `0 -> 1` (`+1`)
- ETL batches: `0 -> 3` (`+3`)
- ETL staging rows: `0 -> 3` (`+3`)
- ETL errors: `0 -> 0` (`+0`)

## Verdict
IMP-5.7 is implemented and dry-run verified in this workspace.

## Notes / Follow-ups
- `scripts/promote_staging.py` emits Python 3.14 deprecation warnings for `datetime.utcnow()`. Functional impact is none for this dry run, but code should migrate to timezone-aware `datetime.now(datetime.UTC)` in a follow-up hardening pass.
