# DOC-024 DSA Reconciliation Specifications

\# DOC\-024: DSA Reconciliation Specifications

\*\*Document ID:\*\* DOC\-024  

\*\*Version:\*\* 1\.0  

\*\*Status:\*\* Approved / Frozen  

\*\*Owner:\*\* CTO \(ChatGPT\)  

\*\*Classification:\*\* Reconciliation Specifications  

\*\*Purpose:\*\* Define all reconciliation workflows for the DSA industry\. This document provides the authoritative reference for reconciling financial and operational data across bank statements, commission calculations, tax filings, and accounting systems\.

\-\-\-

\#\# Table of Contents

1\. Executive Summary

2\. Bank Reconciliation \(BRS\)

3\. Commission Reconciliation

4\. Tax Reconciliation

5\. Tally Reconciliation

6\. Reconciliation Dashboard

7\. Exception Management

8\. Reconciliation Schedule

9\. Document Status & Approval

\-\-\-

\#\# 1\. Executive Summary

\#\#\# 1\.1 Purpose

This document defines all reconciliation workflows required for the DSA/FCPL operations\. Reconciliation ensures that financial data across systems is consistent, accurate, and auditable\. It establishes the processes for matching platform records with external data sources and resolving discrepancies\.

\#\#\# 1\.2 Reconciliation Philosophy

| Principle | Description |

|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \*\*Automation First\*\* | Reconciliations shall be automated where possible |

| \*\*Traceability\*\* | Every reconciliation action is logged and traceable |

| \*\*Timely\*\* | Reconciliations are performed on schedule \(daily, weekly, monthly\) |

| \*\*Exception\-Driven\*\* | Only exceptions require human intervention |

| \*\*Auditable\*\* | Complete audit trail for all reconciliation activities |

| \*\*Threshold\-Based\*\* | Tolerance thresholds defined for acceptable variance |

\#\#\# 1\.3 Scope of Coverage

| Reconciliation Type | Frequency | Source | Target |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| Bank Reconciliation \(BRS\) | Daily | Bank Statement | TRN\_Payment |

| Commission Reconciliation | Weekly/Monthly | Platform Calculation | DSR/Input |

| Tax Reconciliation | Monthly | Platform Calculation | Tax Filing |

| Tally Reconciliation | Monthly | Platform Summary | Tally GL |

| Invoice Reconciliation | Daily | TRN\_Invoice | Bank Statement |

\#\#\# 1\.4 Relationship to Other Repository Documents

| Document | Relationship |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| DOC\-010 | Architecture foundation for reconciliation |

| DOC\-011 | Data Model for reconciliation tables |

| DOC\-012 | Platform Engineering referencing operational runbooks |

| DOC\-014 | Finance & Operations Specifications |

| DOC\-021 | FCPL Industry Configuration |

| DOC\-022 | Source\-to\-Canonical Mapping Guide |

| DOC\-023 | Rule Engine Translation Guide |

\-\-\-

\#\# 2\. Bank Reconciliation \(BRS\)

\#\#\# 2\.1 Purpose

Bank Reconciliation \(BRS\) matches platform payments against bank statements to ensure all outbound payments are properly recorded and no unauthorized transactions exist\.

\#\#\# 2\.2 Reconciliation Flow

\`\`\`

┌─────────────────────────────────────────────────────────────────┐

│                    BANK RECONCILIATION FLOW                     │

├─────────────────────────────────────────────────────────────────┤

│                                                                 │

│  ┌─────────────────┐       ┌─────────────────┐               │

│  │  TRN\_Payment    │       │ Bank Statement  │               │

│  │  \(Platform\)     │       │  \(External\)     │               │

│  └────────┬────────┘       └────────┬────────┘               │

│           │                         │                          │

│           └───────────┬─────────────┘                          │

│                       │                                        │

│                       ▼                                        │

│          ┌─────────────────────────┐                           │

│          │    UTR Number Match     │                           │

│          │                         │                           │

│          │  TRN\_Payment\.UTR =      │                           │

│          │  BankStatement\.UTR      │                           │

│          └────────────┬────────────┘                           │

│                       │                                        │

│        ┌──────────────┼────────────────┐                      │

│        │              │                │                       │

│        ▼              ▼                ▼                       │

│  ┌──────────┐  ┌──────────┐  ┌──────────────┐               │

│  │ Matched  │  │ Flagged  │  │ Flagged      │               │

│  │ \(Green\)  │  │ \(Red\)    │  │ \(Yellow\)     │               │

│  └──────────┘  └──────────┘  └──────────────┘               │

│                                                                 │

└─────────────────────────────────────────────────────────────────┘

\`\`\`

\#\#\# 2\.3 Matching Criteria

| Match Type | Criteria | Priority | Result |

|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Exact UTR Match\*\* | UTR number matches exactly | 1 | Automatically reconciled |

| \*\*Amount \+ Date Match\*\* | Amount and date match | 2 | Flag for review |

| \*\*Amount \+ Beneficiary Match\*\* | Amount and beneficiary match | 3 | Flag for review |

| \*\*No Match\*\* | No matching criteria | 4 | Exception: Manual review |

\#\#\# 2\.4 Reconciliation Matrix

| Source Data | Target Data | Matching Fields | Frequency |

|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|

| TRN\_Payment | Bank Statement | UTR, Amount, Date, Beneficiary | Daily |

| TRN\_Invoice | Bank Statement | Invoice No, Amount, Date | Daily |

| TRN\_Revenue | Bank Statement | Revenue ID, Amount, Date | Weekly |

| TRN\_Commission | Bank Statement | Commission ID, Amount, Date | Weekly |

\#\#\# 2\.5 BRS Workflow

| Step | Action | Owner | SLA |

|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-|\-\-\-\-\-|

| 1 | Import bank statement | Finance Team | Daily by 10:00 AM |

| 2 | Auto\-match UTRs | System | Within 15 minutes |

| 3 | Review flagged transactions | Finance Team | Within 4 hours |

| 4 | Resolve exceptions | Finance Team | Within 24 hours |

| 5 | Approve reconciliation | Finance Lead | Within 48 hours |

| 6 | Generate BRS report | System | End of each business day |

\#\#\# 2\.6 UTR Matching Rules

| Condition | Action |

|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| UTR found in bank statement | Mark as RECONCILED |

| UTR not found but amount/date match | Flag for review |

| UTR not found and no other match | Flag as UNMATCHED |

| Duplicate UTR detected | Flag for investigation |

\#\#\# 2\.7 Bank Statement Import Format

| Field | Format | Required |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|

| Transaction Date | YYYY\-MM\-DD | Yes |

| UTR Number | VARCHAR\(100\) | Yes |

| Amount | DECIMAL\(18,2\) | Yes |

| Beneficiary Name | VARCHAR\(255\) | Yes |

| Reference | VARCHAR\(255\) | No |

| Bank Name | VARCHAR\(100\) | Yes |

| Account Number | VARCHAR\(50\) | Yes |

| IFSC | VARCHAR\(20\) | No |

\#\#\# 2\.8 Reconciliation Status Codes

| Status Code | Status Name | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| RECONCILED | Reconciled | Successfully matched |

| PARTIAL | Partially Reconciled | Partial match found |

| PENDING | Pending | Waiting for bank statement |

| EXCEPTION | Exception | Requires manual review |

| UNMATCHED | Unmatched | No matching transaction found |

| INVESTIGATING | Investigating | Under investigation |

| RESOLVED | Resolved | Exception resolved |

\#\#\# 2\.9 BRS Report Structure

| Column | Description |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Payment ID | Platform payment identifier |

| UTR Number | Payment UTR |

| Payment Date | Date of payment |

| Amount | Payment amount |

| Bank Statement Date | Date on bank statement |

| Bank Statement UTR | UTR on bank statement |

| Match Status | RECONCILED / UNMATCHED / PARTIAL |

| Variance | Difference in amount |

| Resolution Status | OPEN / RESOLVED |

| Resolution Date | Date resolved |

| Resolved By | User who resolved |

\-\-\-

\#\# 3\. Commission Reconciliation

\#\#\# 3\.1 Purpose

Commission Reconciliation ensures that platform\-calculated commissions match the source data \(Excel/DSR\) and lender payout data\.

\#\#\# 3\.2 Reconciliation Types

| Type | Source | Target | Threshold |

|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|

| Connector Commission | Platform Calculation | DSR Input | ±2% |

| Lender Revenue | Platform Calculation | Lender Statement | ±1% |

| Employee Incentive | Platform Calculation | HR File | ±2% |

| Campaign Bonus | Platform Calculation | Campaign Data | ±1% |

\#\#\# 3\.3 Commission Reconciliation Flow

\`\`\`

┌─────────────────────────────────────────────────────────────────┐

│                  COMMISSION RECONCILIATION FLOW                 │

├─────────────────────────────────────────────────────────────────┤

│                                                                 │

│  ┌─────────────────┐       ┌─────────────────┐               │

│  │  Platform       │       │  Excel/DSR      │               │

│  │  Commission     │       │  Source Data    │               │

│  └────────┬────────┘       └────────┬────────┘               │

│           │                         │                          │

│           └───────────┬─────────────┘                          │

│                       │                                        │

│                       ▼                                        │

│          ┌─────────────────────────┐                           │

│          │    Commission Match     │                           │

│          │                         │                           │

│          │  Case ID \+ Amount \+ %  │                           │

│          └────────────┬────────────┘                           │

│                       │                                        │

│        ┌──────────────┼────────────────┐                      │

│        │              │                │                       │

│        ▼              ▼                ▼                       │

│  ┌──────────┐  ┌──────────┐  ┌──────────────┐               │

│  │  Within  │  │  >2%     │  │  Missing     │               │

│  │  Threshold│  │ Variance │  │  Records     │               │

│  │  \(Green\) │  │ \(Red\)    │  │  \(Yellow\)    │               │

│  └──────────┘  └──────────┘  └──────────────┘               │

│                                                                 │

└─────────────────────────────────────────────────────────────────┘

\`\`\`

\#\#\# 3\.4 Reconciliation Logic

| Step | Action | Logic | Owner |

|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-|

| 1 | Extract Platform Data | Query TRN\_Commission | System |

| 2 | Extract Source Data | Parse Excel/DSR | System |

| 3 | Match by Case ID | \`Platform\.CaseID = Source\.CaseID\` | System |

| 4 | Compare Amounts | \`ABS\(Platform\.Amount \- Source\.Amount\)\` | System |

| 5 | Apply Threshold | Variance > 2% → Flag | System |

| 6 | Generate Report | All matched \+ exceptions | System |

\#\#\# 3\.5 Variance Handling

| Variance | Action |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| ≤ 1% | Auto\-reconcile |

| 1% \- 2% | Flag for review \(low priority\) |

| 2% \- 5% | Flag for review \(medium priority\) |

| > 5% | Flag for review \(high priority\) |

| Missing record | Escalate to Operations |

\#\#\# 3\.6 Commission Reconciliation Report

| Column | Description |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Case ID | Loan case identifier |

| Connector | Connector name |

| Product | Product type |

| Lender | Lender name |

| Platform Commission | Platform\-calculated amount |

| Source Commission | Excel/DSR amount |

| Variance | Difference |

| Variance % | Percentage variance |

| Status | RECONCILED / FLAGGED / MISSING |

| Resolution | OPEN / RESOLVED |

\#\#\# 3\.7 Connector Payout Reconciliation

| Step | Action | Owner |

|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-|

| 1 | Generate Connector Payout Statement | System |

| 2 | Match against DSR | System |

| 3 | Flag discrepancies | System |

| 4 | Review and approve | Finance Team |

| 5 | Process payments | Finance Team |

\-\-\-

\#\# 4\. Tax Reconciliation

\#\#\# 4\.1 Purpose

Tax Reconciliation ensures that GST and TDS calculated by the platform match actual tax filings and statutory payments\.

\#\#\# 4\.2 GST Reconciliation

\#\#\#\# 4\.2\.1 Reconciliation Flow

\`\`\`

┌─────────────────────────────────────────────────────────────────┐

│                    GST RECONCILIATION FLOW                      │

├─────────────────────────────────────────────────────────────────┤

│                                                                 │

│  ┌─────────────────┐       ┌─────────────────┐               │

│  │  Platform GST   │       │  GST Filing     │               │

│  │  Calculation    │       │  \(GSTR\-1/3B\)    │               │

│  └────────┬────────┘       └────────┬────────┘               │

│           │                         │                          │

│           └───────────┬─────────────┘                          │

│                       │                                        │

│                       ▼                                        │

│          ┌─────────────────────────┐                           │

│          │    GST Match            │                           │

│          │                         │                           │

│          │  Period \+ GSTIN \+      │                           │

│          │  Amount                │                           │

│          └────────────┬────────────┘                           │

│                       │                                        │

│        ┌──────────────┼────────────────┐                      │

│        │              │                │                       │

│        ▼              ▼                ▼                       │

│  ┌──────────┐  ┌──────────┐  ┌──────────────┐               │

│  │  Matched │  │  Discre\- │  │  Missing     │               │

│  │  \(Green\) │  │  pancy   │  │  Records     │               │

│  │          │  │  \(Red\)   │  │  \(Yellow\)    │               │

│  └──────────┘  └──────────┘  └──────────────┘               │

│                                                                 │

└─────────────────────────────────────────────────────────────────┘

\`\`\`

\#\#\#\# 4\.2\.2 GST Reconciliation Logic

| Step | Action | Logic | Frequency |

|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|

| 1 | Calculate Platform GST | TRN\_Revenue\.GSTAmount | Monthly |

| 2 | Extract GST Filing | GSTR\-1 / GSTR\-3B | Monthly |

| 3 | Match by Period | \`Platform\.Period = Filing\.Period\` | Monthly |

| 4 | Compare GST Amount | \`ABS\(Platform\.GST \- Filing\.GST\)\` | Monthly |

| 5 | Check GSTIN | Validate GSTIN matches | Monthly |

\#\#\# 4\.3 TDS Reconciliation

\#\#\#\# 4\.3\.1 TDS Reconciliation Flow

\`\`\`

┌─────────────────────────────────────────────────────────────────┐

│                    TDS RECONCILIATION FLOW                      │

├─────────────────────────────────────────────────────────────────┤

│                                                                 │

│  ┌─────────────────┐       ┌─────────────────┐               │

│  │  Platform TDS   │       │  TDS Filing     │               │

│  │  Calculation    │       │  \(26Q/27Q\)      │               │

│  └────────┬────────┘       └────────┬────────┘               │

│           │                         │                          │

│           └───────────┬─────────────┘                          │

│                       │                                        │

│                       ▼                                        │

│          ┌─────────────────────────┐                           │

│          │    TDS Match            │                           │

│          │                         │                           │

│          │  PAN \+ Section \+        │                           │

│          │  Amount \+ Quarter       │                           │

│          └────────────┬────────────┘                           │

│                       │                                        │

│        ┌──────────────┼────────────────┐                      │

│        │              │                │                       │

│        ▼              ▼                ▼                       │

│  ┌──────────┐  ┌──────────┐  ┌──────────────┐               │

│  │  Matched │  │  Discre\- │  │  Missing     │               │

│  │  \(Green\) │  │  pancy   │  │  PAN         │               │

│  │          │  │  \(Red\)   │  │  \(Yellow\)    │               │

│  └──────────┘  └──────────┘  └──────────────┘               │

│                                                                 │

└─────────────────────────────────────────────────────────────────┘

\`\`\`

\#\#\#\# 4\.3\.2 TDS Reconciliation Logic

| Step | Action | Logic | Frequency |

|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|

| 1 | Calculate Platform TDS | TRN\_Payment\.TDSAmount | Quarterly |

| 2 | Extract TDS Filing | 26Q / 27Q | Quarterly |

| 3 | Match by PAN | \`Platform\.PAN = Filing\.PAN\` | Quarterly |

| 4 | Match by Section | \`Platform\.Section = Filing\.Section\` | Quarterly |

| 5 | Compare Amount | \`ABS\(Platform\.TDS \- Filing\.TDS\)\` | Quarterly |

\#\#\# 4\.4 Tax Reconciliation Schedule

| Activity | Frequency | Owner | Deadline |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|

| GST Calculation | Monthly | System | 5th of following month |

| GST Filing | Monthly | Finance | 20th of following month |

| GST Reconciliation | Monthly | Finance | 25th of following month |

| TDS Calculation | Quarterly | System | 15th of following quarter |

| TDS Filing | Quarterly | Finance | 30th of following quarter |

| TDS Reconciliation | Quarterly | Finance | 5th of next quarter |

\#\#\# 4\.5 Tax Reconciliation Report

| Column | Description |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Period | Tax period \(month/quarter\) |

| Tax Type | GST / TDS |

| Calculated Amount | Platform\-calculated tax |

| Filed Amount | Amount filed with government |

| Variance | Difference |

| Status | RECONCILED / DISCREPANCY |

| Action Required | None / Investigation |

| Resolution Date | Date resolved |

\-\-\-

\#\# 5\. Tally Reconciliation

\#\#\# 5\.1 Purpose

Tally Reconciliation ensures that platform financial data matches the Tally accounting system \(GL\) before automated posting\.

\#\#\# 5\.2 Reconciliation Flow

\`\`\`

┌─────────────────────────────────────────────────────────────────┐

│                    TALLY RECONCILIATION FLOW                    │

├─────────────────────────────────────────────────────────────────┤

│                                                                 │

│  ┌─────────────────┐       ┌─────────────────┐               │

│  │  Platform GL    │       │  Tally GL       │               │

│  │  Summary        │       │  Export         │               │

│  └────────┬────────┘       └────────┬────────┘               │

│           │                         │                          │

│           └───────────┬─────────────┘                          │

│                       │                                        │

│                       ▼                                        │

│          ┌─────────────────────────┐                           │

│          │    GL Match             │                           │

│          │                         │                           │

│          │  Account \+ Period \+    │                           │

│          │  Debit \+ Credit        │                           │

│          └────────────┬────────────┘                           │

│                       │                                        │

│        ┌──────────────┼────────────────┐                      │

│        │              │                │                       │

│        ▼              ▼                ▼                       │

│  ┌──────────┐  ┌──────────┐  ┌──────────────┐               │

│  │  Matched │  │  Variance│  │  Missing     │               │

│  │  \(Green\) │  │  \(Red\)   │  │  Accounts    │               │

│  │          │  │          │  │  \(Yellow\)    │               │

│  └──────────┘  └──────────┘  └──────────────┘               │

│                                                                 │

└─────────────────────────────────────────────────────────────────┘

\`\`\`

\#\#\# 5\.3 GL Account Mapping

| Platform Table | Source | Tally Account | Account Type |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| TRN\_Revenue | Revenue | Commission Income | Income |

| TRN\_Commission | Connector Payout | Commission Expense | Expense |

| TRN\_Expense | Operational Expense | Office Expense | Expense |

| TRN\_Payment | Payments | Bank Account | Asset |

| TRN\_Invoice | Receivables | Debtors | Asset |

| TRN\_TaxLiability | Tax Liability | GST/TDS Payable | Liability |

| TRN\_EmployeeSalary | Salary Expense | Salary Account | Expense |

| TRN\_StatutoryPayment | Statutory Payments | PF/ESIC Payable | Liability |

\#\#\# 5\.4 Tally Export Format

| Field | Format | Required |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|

| Date | YYYY\-MM\-DD | Yes |

| Voucher Type | Payment/Receipt/Sales | Yes |

| Account Name | VARCHAR\(100\) | Yes |

| Debit Amount | DECIMAL\(18,2\) | No |

| Credit Amount | DECIMAL\(18,2\) | No |

| Narration | TEXT | Yes |

| Reference | VARCHAR\(100\) | Yes |

| TDS Applicable | BOOLEAN | No |

| GST Applicable | BOOLEAN | No |

\#\#\# 5\.5 Tally Reconciliation Logic

| Step | Action | Logic | Frequency |

|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|

| 1 | Generate Platform GL | Query TRN\_\* tables | Monthly |

| 2 | Export Tally GL | Generate XML/JSON export | Monthly |

| 3 | Load Tally Data | Import Tally export | Monthly |

| 4 | Match Accounts | \`Platform\.Account = Tally\.Account\` | Monthly |

| 5 | Compare Totals | \`ABS\(Platform\.Balance \- Tally\.Balance\)\` | Monthly |

\#\#\# 5\.6 Tally Reconciliation Report

| Column | Description |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Account Name | GL Account |

| Platform Balance | Balance as per ODOS |

| Tally Balance | Balance as per Tally |

| Variance | Difference |

| Variance % | Percentage variance |

| Status | RECONCILED / DISCREPANCY |

| Resolution | OPEN / RESOLVED |

\-\-\-

\#\# 6\. Reconciliation Dashboard

\#\#\# 6\.1 Dashboard Metrics

| Metric | Description | Target |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| BRS Matching Rate | % of UTRs matched | >95% |

| Unmatched Transactions | Count of unmatched transactions | <5 |

| Aging of Unmatched | Average days unmatched | <3 days |

| Commission Variance | Average % variance | <2% |

| Tax Reconciliation Status | % of periods reconciled | 100% |

| Tally Reconciliation Status | % of accounts reconciled | 100% |

\#\#\# 6\.2 Dashboard Views

| View | Purpose | Key Metrics |

|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Executive View | High\-level status | Overall reconciliation health |

| Operations View | Daily reconciliation | BRS status, exceptions |

| Finance View | Monthly reconciliation | Tax, Tally status |

| Exception View | Outstanding issues | Unresolved exceptions by age |

\#\#\# 6\.3 Dashboard Widgets

| Widget Type | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| KPI Card | Key metric with trend |

| Table | List of exceptions |

| Chart | Reconciliation trend over time |

| Status Bar | Reconciliation status by type |

| Alert List | Pending action items |

\-\-\-

\#\# 7\. Exception Management

\#\#\# 7\.1 Exception Categories

| Category | Description | Severity |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|

| UTR Mismatch | UTR number not found in bank statement | Critical |

| Amount Mismatch | Payment amount differs from bank statement | High |

| Date Mismatch | Payment date differs from bank statement | Medium |

| Missing Payment | Payment not found in bank statement | Critical |

| Duplicate UTR | Same UTR used for multiple payments | High |

| Commission Variance | Commission calculation differs from source | Medium |

| Tax Discrepancy | Tax calculation differs from filing | High |

\#\#\# 7\.2 Exception Resolution Workflow

\`\`\`

┌─────────────────────────────────────────────────────────────────┐

│                 EXCEPTION RESOLUTION WORKFLOW                   │

├─────────────────────────────────────────────────────────────────┤

│                                                                 │

│  1\. Exception Detected                                         │

│     ↓                                                          │

│  2\. Auto\-Classify Exception                                     │

│     ↓                                                          │

│  3\. Assign to Team                                              │

│     ├── UTR Issues → Finance Team                              │

│     ├── Commission Issues → Operations Team                    │

│     └── Tax Issues → Finance Team                              │

│     ↓                                                          │

│  4\. Investigate                                                │

│     ↓                                                          │

│  5\. Resolve                                                     │

│     ├── Update System                                          │

│     ├── Manual Reconciliation                                   │

│     └── Escalate if needed                                     │

│     ↓                                                          │

│  6\. Verify Resolution                                          │

│     ↓                                                          │

│  7\. Close Exception                                            │

│                                                                 │

└─────────────────────────────────────────────────────────────────┘

\`\`\`

\#\#\# 7\.3 Escalation Matrix

| Exception Age | Action | Escalation |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|

| < 24 hours | Auto\-assign | Team Lead |

| 24\-48 hours | Follow\-up | Team Lead |

| 48\-72 hours | Escalate | Department Head |

| > 72 hours | Critical Escalation | CTO |

\#\#\# 7\.4 Exception Log

| Field | Description |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Exception ID | Unique identifier |

| Exception Type | From categories |

| Date Detected | Detection timestamp |

| Source System | Detecting system |

| Target System | Affected system |

| Severity | Critical/High/Medium/Low |

| Status | OPEN/IN\_PROGRESS/RESOLVED/CLOSED |

| Assigned To | Responsible user/team |

| Resolution | Resolution description |

| Resolved Date | Date resolved |

\-\-\-

\#\# 8\. Reconciliation Schedule

\#\#\# 8\.1 Daily Reconciliation

| Activity | Time | Owner |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-|

| Bank Statement Import | 9:30 AM | Finance Team |

| UTR Auto\-Reconciliation | 10:00 AM | System |

| Exception Review | 11:00 AM | Finance Team |

| BRS Report Generation | 5:00 PM | System |

\#\#\# 8\.2 Weekly Reconciliation

| Activity | Day | Owner |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-|\-\-\-\-\-\-\-|

| Commission Reconciliation | Monday | Operations Team |

| Connector Payout Review | Tuesday | Finance Team |

| Open Exception Review | Wednesday | Finance Team |

| Reconciliation Status Report | Friday | Finance Lead |

\#\#\# 8\.3 Monthly Reconciliation

| Activity | Timeline | Owner |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-|

| Tax Reconciliation | 1st week | Finance Team |

| Tally Reconciliation | 2nd week | Finance Team |

| Month\-End Reconciliation | 3rd week | Finance Lead |

| Reconciliation Report | 4th week | Finance Lead |

\#\#\# 8\.4 Quarterly Reconciliation

| Activity | Timeline | Owner |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-|

| TDS Reconciliation | After quarter\-end | Finance Team |

| GST Annual Reconciliation | After year\-end | Finance Team |

| Audit Preparation | Quarterly | Finance Lead |

\#\#\# 8\.5 Reconciliation SLAs

| Reconciliation Type | Frequency | SLA \(from period end\) | Owner |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-|

| BRS | Daily | 24 hours | Finance Team |

| Commission | Weekly | 7 days | Operations Team |

| Tax | Monthly | 15 days | Finance Team |

| Tally | Monthly | 15 days | Finance Team |

| GST Reconciliation | Monthly | 25 days | Finance Team |

| TDS Reconciliation | Quarterly | 20 days | Finance Team |

\-\-\-

\#\# 9\. Document Status & Approval

\#\#\# 9\.1 Document Status

| Status | Approved / Frozen |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \*\*Version\*\* | 1\.0 |

| \*\*Date\*\* | July 2026 |

| \*\*Next Review\*\* | Annual or before major architectural change |

| \*\*Owner\*\* | CTO |

\#\#\# 9\.2 Document Freeze Notice

\*\*This document is designated as a Reconciliation Baseline Artefact\.\*\*

\*\*Following approval:\*\*

\- Structural changes to reconciliation workflows require a new Architecture Decision Record \(ADR\)\.

\- Changes to reconciliation logic require Architecture Review Board \(ARB\) approval\.

\- All reconciliation implementation shall use this document as the governing baseline\.

\*\*Freeze Status:\*\* ✅ \*\*FROZEN\*\*

\#\#\# 9\.3 Approval Sign\-Off

| Role | Name | Signature | Date |

|\-\-\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-|

| Enterprise Architect | Architecture Review Board | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

| Finance Lead | \[Name\] | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

| Operations Lead | \[Name\] | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

| CTO | \[ChatGPT\] | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

| Technical Programme Manager | \[DeepSeek\] | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

| Development Lead | \[Aniket\] | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

\#\#\# 9\.4 Cross\-Reference to Repository Documents

| Document | Relationship |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| DOC\-000 | Repository structure referencing this document |

| DOC\-001 | Repository guide referencing this document |

| DOC\-002 | Dependency matrix including this document |

| DOC\-003 | Master index including this document |

| DOC\-010 | Architecture & ADRs referencing reconciliation |

| DOC\-011 | Data Model referencing reconciliation tables |

| DOC\-012 | Platform Engineering referencing reconciliation operations |

| DOC\-014 | Finance & Operations Specifications referencing reconciliation logic |

| DOC\-021 | FCPL Industry Configuration for reconciliation context |

| DOC\-022 | Source\-to\-Canonical Mapping for reconciliation sources |

| DOC\-023 | Rule Engine Translation Guide for rule\-based reconciliation |

\-\-\-

\#\# End of Document

\*\*Document ID:\*\* DOC\-024  

\*\*Document Name:\*\* \*DSA Reconciliation Specifications\*  

\*\*Version:\*\* 1\.0  

\*\*Status:\*\* Approved / Frozen  

\*\*Owner:\*\* CTO

