# TEST-INTEL-3 - Automation, Alerts & Notifications Validation

## Validation Checklist
- Alert migration upgrade
- Alert engine tests
- Existing alert API compatibility
- Full backend regression
- Frontend build

## Commands
- `python -m alembic upgrade head`
- `python -m pytest tests/test_alert_engine.py -q`
- `python -m pytest tests/test_alerts_api.py -q`
- `python -m pytest -q`
- `npm.cmd run build`

## Expected Outcomes
- Migration reaches `0009_imp_intel_3` successfully.
- Alert engine tests pass.
- Legacy and modern alert endpoints continue to function.
- No regressions in full test suite.
- Frontend build succeeds with new alerts pages.

## Coverage Highlights
- Rule create/list/get/update/delete
- Rule trigger and in-app notification generation
- Notification read flow
- Audit event persistence
- Auto-resolve flow
- Escalation flow
- Permission enforcement for alerts endpoints
