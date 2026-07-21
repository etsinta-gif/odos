# UI Audit Report - UI-1

## Current State

- Legacy server-rendered UI exists under /masters.
- New React UI scaffold added under frontend.
- Backend hybrid ETL APIs are available.

## Priority Fix List

- P0
  - Auth lifecycle wiring complete (login, refresh, logout, me, companies).
  - Hybrid ETL upload path wired in frontend and backend.
  - Dashboard stats/activity and red-flag feed endpoints wired.
- P1
  - Mapping governance actions (save draft, submit, admin activate) UI endpoint finalization.
  - Additional role-route restrictions and route-level UX messaging.
- P2
  - UI polish, richer interactions, and deeper test automation.

## Route Audit Notes

- /masters/etl/upload: available in legacy UI and new React UI.
- /dashboard and /dashboard/redflags: available in new React UI.
- Remaining legacy masters pages are still served via Jinja and can be migrated incrementally.
