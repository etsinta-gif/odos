# ODOS Frontend (UI-1)

This frontend is pre-wired for Hybrid ETL:
- Template found: upload returns success with strict-template auto processing.
- Template missing: upload returns mapping-required and routes to mapping approval view.

## Run

1. Install Node.js 18+ and npm.
2. In frontend folder run:
   npm install
   npm run dev
3. Ensure backend runs at http://localhost:8000.

## Key Routes

- /login
- /dashboard
- /dashboard/redflags
- /masters/etl/upload
- /etl/mapping/:batchGuid
