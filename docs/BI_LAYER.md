# ODOS BI Layer

## Overview

The ODOS BI Layer provides flexible analytics and reporting on top of the Intelligence Layer. It enables teams to create reusable reports, build dashboards, export outputs, and monitor trends.

## Key Capabilities

- Report definitions with dimensions, metrics, filters, ordering, and limits.
- JSON field support for dimensions and metrics (for example, data.lender_name).
- Export outputs in HTML, CSV, Excel, and PDF-compatible output.
- Trend APIs for GST mismatches, TDS mismatches, commission exceedances, and red-flag counts.
- Dashboard and widget APIs for chart, table, KPI, and custom query visualization.
- Scheduler for recurring report execution (daily, weekly, monthly).

## Workflow

1. Create report definition.
2. Execute report on demand.
3. Export report in desired format.
4. Add report (or custom query) as dashboard widget.
5. Configure schedule for recurring execution.

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| /api/bi/reports/ | GET | List active reports |
| /api/bi/reports/ | POST | Create report |
| /api/bi/reports/{id} | GET | Get report |
| /api/bi/reports/{id} | PUT | Update report |
| /api/bi/reports/{id} | DELETE | Soft delete report |
| /api/bi/reports/{id}/execute | POST | Execute report |
| /api/bi/reports/{id}/export/{format} | GET | Export report |
| /api/bi/reports/{id}/schedule | POST | Create or update schedule |
| /api/bi/reports/{id}/schedules | GET | List report schedules |
| /api/bi/reports/scheduler/run | POST | Trigger due scheduled executions |
| /api/bi/trends/summary | GET | 7-day summary for all trend metrics |
| /api/bi/trends/{metric} | GET | Trend series by metric type |
| /api/bi/dashboards/ | GET | List dashboards |
| /api/bi/dashboards/ | POST | Create dashboard |
| /api/bi/dashboards/{id} | GET | Get dashboard with widgets |
| /api/bi/dashboards/{id} | PUT | Update dashboard |
| /api/bi/dashboards/{id} | DELETE | Soft delete dashboard |
| /api/bi/dashboards/{id}/widgets | POST | Add widget |
| /api/bi/dashboards/{id}/widgets/{widget_id}/execute | POST | Execute widget data source |

## Notes

- BI routes are tenant-scoped by company_id.
- BI permission is role-based in this sprint implementation.
- Existing ETL and Intelligence Layer tables remain the source of truth.
