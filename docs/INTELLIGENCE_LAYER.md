# ODOS Intelligence Layer

## Overview

ODOS operates as an AI-enabled intelligence layer on top of source systems. CRM, accounting, MIS, lender reports, and bank statements are inputs. ODOS ingests, maps, verifies, reconciles, and surfaces insight.

ODOS does not own CRM operations, accounting posting, invoice generation, or payment execution.

## Processing Flow

1. Ingest source files or API payloads.
2. Stage and map into canonical structures.
3. Promote to transaction entities.
4. Cross-verify reported values against defaults and expected policies.
5. Generate red flags for mismatches or anomalies.
6. Provide dashboards, exports, and reconciliation outcomes.

## Core Concepts

### Party Defaults
Each party profile can carry expected defaults such as:
- default_gst_rate
- default_tds_rate
- max_commission

These defaults are references for verification, not invoice computation ownership.

### Cross-Verification
Primary checks include:
- GST consistency between reported and expected values.
- TDS consistency between reported and expected values.
- Commission amount threshold checks against max defaults.

### Red Flags
Red flags are generated automatically with:
- severity (CRITICAL, WARNING, INFO)
- category (gst, tds, commission, duplicate, missing)
- clear mismatch context (reported vs expected)
- lifecycle status (OPEN, RESOLVED, IGNORED)

## Operator Workflow

1. Upload data through ETL.
2. Confirm or refine mapping.
3. Promote data and run verification.
4. Review red flags.
5. Resolve or ignore with notes.
6. Tune party defaults when reference baselines change.

## BI and Reconciliation

Flexible JSON fields and canonical entities support:
- ad-hoc dimensional slicing
- dashboard KPI drill-downs
- invoice/payment/UTR reconciliation investigation
- audit-friendly lineage from source to insight

## Governance Principles

- Tenant isolation is mandatory.
- Every mismatch should be explainable and traceable.
- Verification is deterministic and auditable.
- Legacy calculation-centric modules can remain in compatibility mode during transition, then be retired by telemetry.
