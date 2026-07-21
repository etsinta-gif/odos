## 1. The External Workflow (End-to-End DSA Operating Model)

Based on your description, here is the formalized workflow that will become the foundation for DOC-021 (FCPL Industry Configuration Specification).

### 1.1 High-Level Process Flow

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                         DSA OPERATING WORKFLOW                                      │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐      │
│  │  1. Data │    │  2. ETL  │    │  3. Data │    │  4. Recon│    │  5. Recon│      │
│  │  Upload  │───▶│ Staging  │───▶│Validation│───▶│  with    │───▶│  with   │      │
│  │  (Daily) │    │  & Map   │    │  & Calc  │    │  Bank    │    │  Tally  │      │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘      │
│       │               │               │               │               │             │
│       ▼               ▼               ▼               ▼               ▼             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐      │
│  │ Excel/CSV│    │ Staging  │    │ MST & TRN│    │ UTR Matc│    │ GL      │      │
│  │ Google   │    │ Tables   │    │ Updates  │    │ Due Date│    │ Journals│      │
│  │ Sheets   │    │ (Raw)    │    │ Red Flags│    │ Alerts  │    │ Export  │      │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘      │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Detailed Process Steps

| Step | Trigger | Action | System Responsibility | User Responsibility | Output |
|------|---------|--------|----------------------|-------------------|--------|
| **1. Data Upload** | Daily/Monthly | Upload Excel/CSV/Google Sheets | Provide upload UI, detect duplicate files | Upload files | Files in Landing Zone |
| **2. ETL Staging & Mapping** | File Arrival | Stage raw data, suggest mappings | Parse files, AI mapping recommendations, store in ETL_StagingRawData | Review/confirm mappings | Staged data + AI_Mapping recommendations |
| **3. Data Validation & Calculation** | Staging Complete | Validate, dedupe, calculate | Apply validation rules, duplicate detection, calculate commissions/TDS/GST | Review exceptions, approve/merge duplicates | Validated & enriched data |
| **4. Master Data Update** | Validation Pass | Update MST_ tables | Add only new masters (Lenders, Connectors, Products, Employees) | Confirm new masters | Updated master records |
| **5. Disbursement Confirmation** | Connector Upload | Confirm loan disbursement | Write to Bank interface, get confirmation | Upload DSR/connector report | Confirmed disbursement record |
| **6. Reconciliation with Bank** | Daily | Match UTRs, due dates | Match payments against bank statements, flag overdue | Investigate flags | Reconciled payments + exceptions |
| **7. Reconciliation with Tally** | Monthly | Export GL journals | Generate Tally-compatible export | Import to Tally, confirm | Tally export file |
| **8. Tax Reconciliation** | Quarterly | GST/TDS vs returns | Calculate tax liability, compare with returns | Confirm filing | Tax reconciliation report |

### 1.3 Reconciliation Matrix

| Reconciliation Type | Source Data | Target Data | Frequency | Action on Mismatch |
|---------------------|-------------|-------------|-----------|-------------------|
| **Commission vs Bank** | TRN_Commission | Bank Statement (UTR) | Daily | Flag, require manual verification |
| **Disbursement vs DSR** | TRN_Case | Connector DSR | Daily | Flag if >2% variance |
| **GST vs Returns** | RUL_GSTRule + TRN_Revenue | GST Filing | Monthly | Alert, require explanation |
| **TDS vs Returns** | RUL_TDSRule + TRN_Payment | TDS Filing | Monthly | Alert, require explanation |
| **Invoice vs Bank** | TRN_Invoice | Bank Statement | Daily | Overdue alerts |
| **Tally vs Platform** | TRN_* Summary | Tally GL | Monthly | Manual review before push |

