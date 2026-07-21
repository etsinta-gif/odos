# FCPL Pilot Acceptance Results

Generated At: 2026-07-21T10:23:14.361531
Base URL: http://127.0.0.1:8000
Overall Verdict: FAIL

## Summary

- PASS: 1
- FAIL: 1
- BLOCKED: 16
- PENDING: 13

## Case Matrix

| Test ID | Result | Notes |
|---|---|---|
| RG-02 | FAIL | HTTPConnectionPool(host='127.0.0.1', port=8000): Max retries exceeded with url: /api/v1/health (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=8000): Failed to |
| CF-01 | BLOCKED | server_not_reachable |
| CF-02 | BLOCKED | server_not_reachable |
| CF-03 | BLOCKED | server_not_reachable |
| SC-03 | BLOCKED | server_not_reachable |
| RG-04 | BLOCKED | server_not_reachable |
| E2E-02 | BLOCKED | server_not_reachable |
| TR-01 | BLOCKED | server_not_reachable |
| TR-02 | BLOCKED | server_not_reachable |
| TR-03 | BLOCKED | server_not_reachable |
| TR-04 | BLOCKED | server_not_reachable |
| TR-05 | BLOCKED | server_not_reachable |
| TR-06 | BLOCKED | server_not_reachable |
| TR-07 | BLOCKED | server_not_reachable |
| TR-08 | BLOCKED | server_not_reachable |
| TR-09 | BLOCKED | server_not_reachable |
| TR-10 | BLOCKED | server_not_reachable |
| RG-03 | PASS | ................................                                         [100%] ============================== warnings summary =============================== ..\.venv\Lib\site-pa |
| SC-01 | PENDING | Requires direct DB schema introspection in target PostgreSQL environment. |
| SC-02 | PENDING | Requires DB-level field type verification in target PostgreSQL environment. |
| VG-01 | PENDING | Needs invalid PAN fixture row upload under matching template. |
| VG-02 | PENDING | Needs disbursement/application date consistency fixture. |
| VG-03 | PENDING | Needs non-existent FK fixture upload. |
| VG-05 | PENDING | Needs controlled UPDATE policy re-upload scenario. |
| VG-06 | PENDING | Needs controlled FAIL policy duplicate scenario. |
| NL-01 | PENDING | Needs pre/post migration snapshot evidence from target environment. |
| NL-02 | PENDING | Covered partially via duplicate upload behavior in TR cases. |
| NL-03 | PENDING | Needs reconciliation dataset old vs canonical fields. |
| NL-04 | PENDING | Needs 2 clean cycles and legacy synonym replay evidence. |
| E2E-01 | PENDING | Needs all 10 source files available and server execution window. |
| E2E-03 | PENDING | Needs deterministic tally export content assertion dataset. |