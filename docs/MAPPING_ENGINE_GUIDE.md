# ODOS Mapping Engine - Admin Guide

## Workflow

1. First-time file upload:
- Analyze workbook and all sheets.
- Generate mapping proposal.
- Confirm and store template.

2. Repeat upload:
- Match template by fingerprint or filename pattern.
- Load mapped sheet/header.
- Stage normalized rows.
- Validate, deduplicate, scrub.
- Promote to master schema.

## Endpoints

- POST /api/admin/mapping/analyze
- POST /api/admin/mapping/confirm
- GET /api/admin/mapping/templates
- GET /api/admin/mapping/templates/{id}
- PUT /api/admin/mapping/templates/{id}
- DELETE /api/admin/mapping/templates/{id}

## Quick Start

1. Analyze a file:

```bash
python scripts/analyze_excel.py --file samples/Lender_Master.xlsx --generate-mapping
```

2. Confirm mapping:
- Use POST /api/admin/mapping/confirm with template payload.
- Set status to Active after review.

3. Upload through ETL:
- POST /api/v1/etl/upload.
- First-time uploads return mapping-required response.
- Repeat uploads stage rows using stored mapping.
