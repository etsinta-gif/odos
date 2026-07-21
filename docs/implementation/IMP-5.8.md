# IMP-5.8 - Generic Excel Mapping Engine

Date: 2026-07-20

## Objective
Enable first-time sheet onboarding with mapping inference and template approval, followed by routine mapped ingestion for subsequent uploads.

## Implemented Components

- Admin API: [src/admin/api/mapping.py](src/admin/api/mapping.py)
- File analyzer: [src/admin/services/file_analyzer.py](src/admin/services/file_analyzer.py)
- Mapping proposal engine: [src/admin/services/mapper.py](src/admin/services/mapper.py)
- Template persistence service: [src/admin/services/template_store.py](src/admin/services/template_store.py)
- ETL mapping resolver service: [src/metadata/services/field_mapper.py](src/metadata/services/field_mapper.py)
- Metadata models: [src/metadata/models.py](src/metadata/models.py)
- ETL integration update: [src/masters/api/etl.py](src/masters/api/etl.py)
- CLI analysis tool: [scripts/analyze_excel.py](scripts/analyze_excel.py)
- Unit tests: [tests/test_mapping_engine.py](tests/test_mapping_engine.py)
- User guide: [docs/MAPPING_ENGINE_GUIDE.md](docs/MAPPING_ENGINE_GUIDE.md)

## Process Clarification

### First-time upload
1. Analyze workbook and all sheets via `POST /api/admin/mapping/analyze`.
2. Review proposal and confirm template via `POST /api/admin/mapping/confirm`.
3. Store approved mapping in `meta_import_template` and `meta_field_mapping`.

### Repeat upload
1. ETL upload computes workbook fingerprint.
2. ETL tries template match by fingerprint, then file pattern.
3. If no template found: returns `202` with `mapping_required=true` and proposal payload.
4. If template found: reads configured sheet/header, maps source columns to canonical fields, scrubs values, deduplicates within batch, and stages rows.
5. Existing validation and promotion pipeline then runs into target schema.

## Notes
- Router wiring added in [app/main.py](app/main.py).
- Metadata models are imported in app startup path so tables are created by existing `Base.metadata.create_all(...)` strategy.
- Dependency `xlrd` added to [requirements.txt](requirements.txt) and [pyproject.toml](pyproject.toml).

## Verification Completed
- Static checks: no IDE errors in updated/new files.
- Unit tests: `tests/test_mapping_engine.py` passed (10 tests).
- Runtime smoke test passed:
  - analyze endpoint saw 2-sheet workbook,
  - template confirmed,
  - ETL upload used stored template and staged mapped row successfully.
