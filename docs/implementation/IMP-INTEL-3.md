# IMP-INTEL-3 - Automation, Alerts & Notifications Engine

## Scope
Implemented INTEL-3 automation and alerts capabilities on top of existing red-flag and BI layers.

## Backend Deliverables
- Added alert domain models:
  - `ALERT_Rule`
  - `ALERT_EscalationPolicy`
  - `ALERT_Notification`
  - `ALERT_AuditLog`
- Added services:
  - `src/alerts/services/alert_engine.py`
  - `src/alerts/services/notification.py`
  - `src/alerts/services/escalation.py`
  - `src/alerts/services/automation.py`
  - `src/alerts/services/scheduler.py`
- Extended Alerts API for:
  - Rule CRUD and rule testing
  - Escalation policy create/list
  - Notification read/list
  - Audit list
  - Automation triggers
  - Scheduler manual run endpoint
- Preserved existing INTEL-1 red-flag endpoints and legacy `/api/v1/alerts` compatibility.

## Database Deliverables
- Added migration `0009_imp_intel_3_alert_engine.py`.
- New tables:
  - `alert_rules`
  - `alert_escalation_policies`
  - `alert_notifications`
  - `alert_audit_logs`

## Scheduler Integration
- Wired scheduler lifecycle into app startup/shutdown, guarded by environment flag:
  - `ALERT_SCHEDULER_ENABLED=1` enables background periodic tasks.

## Frontend Deliverables
- Extended alerts API client with INTEL-3 methods.
- Added alert UI pages:
  - `frontend/src/pages/Alerts/RuleManagement.tsx`
  - `frontend/src/pages/Alerts/NotificationCenter.tsx`
  - `frontend/src/pages/Alerts/AuditLog.tsx`
- Added route wiring and sidebar entries:
  - `frontend/src/App.tsx`
  - `frontend/src/components/layout/Sidebar.tsx`

## Template Deliverables
- Added email template:
  - `src/templates/email/alert_email.html`

## Notes
- JSON columns are used for cross-database compatibility (SQLite + Postgres style).
- Email notification gracefully records failure when SMTP settings are missing, preventing hard failures in rule execution.
