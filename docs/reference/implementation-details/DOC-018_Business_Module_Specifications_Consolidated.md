# DOC-018 Business Module Specifications Consolidated

\# DOC\-018 – Business Module Specifications Consolidated

\*\*Document ID:\*\* DOC\-018  

\*\*Version:\*\* 1\.0  

\*\*Status:\*\* Approved / Frozen  

\*\*Owner:\*\* CTO \(ChatGPT\)  

\*\*Classification:\*\* Module Specifications  

\*\*Purpose:\*\* Define the complete business module specifications for the ODOS Enterprise Platform, including all operational, sales, and business execution modules\.

\-\-\-

\#\# Table of Contents

1\. Executive Summary

2\. Lead Management Module

3\. Customer Management Module

4\. Connector Management Module

5\. Case Management Module

6\. Revenue Management Module

7\. Commission Management Module

8\. Incentive Management Module

9\. Expense Management Module

10\. Payment Management Module

11\. Invoice Management Module

12\. Profitability Analysis Module

13\. Working Capital Management Module

14\. Forecasting Engine Module

15\. Business Modules Gap Analysis & Resolution Register

16\. Document Status & Approval

\-\-\-

\#\# 1\. Executive Summary

\#\#\# 1\.1 Purpose of This Document

This document consolidates the complete business module specifications for the ODOS Enterprise Platform\. It defines \*\*how\*\* the operational and business execution modules are implemented and interact with the rest of the system\.

This document covers:

\- \*\*Lead Management Module\*\* – Lead capture, tracking, and conversion

\- \*\*Customer Management Module\*\* – Customer master data and KYC management

\- \*\*Connector Management Module\*\* – Channel partner management

\- \*\*Case Management Module\*\* – Complete loan lifecycle management

\- \*\*Revenue Management Module\*\* – Commission income from lenders

\- \*\*Commission Management Module\*\* – Payouts to connectors

\- \*\*Incentive Management Module\*\* – Employee success fees and incentives

\- \*\*Expense Management Module\*\* – Operational expense tracking

\- \*\*Payment Management Module\*\* – Outbound payments and BRS

\- \*\*Invoice Management Module\*\* – Invoice generation and tracking

\- \*\*Profitability Analysis Module\*\* – Case and portfolio profitability

\- \*\*Working Capital Management Module\*\* – Cash conversion cycle and liquidity

\- \*\*Forecasting Engine Module\*\* – Predictive analytics and forecasting

\#\#\# 1\.2 The Business Module Philosophy

ODOS business modules follow a \*\*Process\-First\*\* and \*\*Data\-Driven\*\* philosophy:

| Principle | Description |

|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \*\*Process\-First\*\* | Modules implement business processes, not just data management |

| \*\*Data\-Driven\*\* | All business decisions are supported by governed data |

| \*\*AI\-Assisted\*\* | Modules leverage AI where appropriate |

| \*\*Human\-Governed\*\* | Critical decisions remain human\-controlled |

| \*\*Auditable\*\* | All business actions are auditable |

| \*\*Configurable\*\* | Business behaviour is configurable via rules |

| \*\*Traceable\*\* | Every business transaction is traceable |

\#\#\# 1\.3 Module Dependency Overview

\`\`\`

Lead Management

        │

        ▼

Customer Management ─────┐

        │                 │

        ▼                 │

Case Management           │

        │                 │

        ├─────────────────┤

        │                 │

        ▼                 ▼

Revenue Management   Commission Management

        │                 │

        ▼                 ▼

Invoice Management   Payment Management

        │                 │

        └─────────────────┤

                          │

                          ▼

                   Profitability Analysis

                          │

                          ▼

                Working Capital Management

                          │

                          ▼

                   Forecasting Engine

\`\`\`

\#\#\# 1\.4 Relationship to Other Repository Documents

| Document | Relationship |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| DOC\-010 | Architecture & ADRs referencing module design |

| DOC\-011 | Data Model referencing module tables |

| DOC\-013 | Application Development Standards referencing module implementation |

| DOC\-014 | Finance & Operations Specifications referencing module logic |

| DOC\-015 | AI & Data Engineering referencing AI modules |

| DOC\-016 | Security & Governance referencing module security |

| DOC\-017 | Core Modules referencing shared services |

\#\#\# 1\.5 Document Status

| Status | Approved / Frozen |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \*\*Version\*\* | 1\.0 |

| \*\*Date\*\* | July 2026 |

| \*\*Next Review\*\* | Annual or before major architectural change |

| \*\*Owner\*\* | CTO |

\-\-\-

\#\# 2\. Lead Management Module

\#\#\# 2\.1 Module Overview

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Module ID\*\* | MOD\-013 |

| \*\*Module Name\*\* | Lead Management |

| \*\*Module Group\*\* | CRM & Sales |

| \*\*Business Owner\*\* | Sales |

| \*\*Data Steward\*\* | Sales Operations |

| \*\*Phase Classification\*\* | Phase 1 |

\#\#\# 2\.2 Objective & Business Purpose

\*\*Objective:\*\* Manage leads from source to conversion\.

\*\*Business Purpose:\*\* Tracks lead sources, conversion rates, and connector performance\.

\#\#\# 2\.3 Scope

| In Scope | Out of Scope |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Lead capture | Case management \(handled by Case Management\) |

| Lead assignment | |

| Lead status tracking | |

| Lead scoring \(future\) | |

| Source attribution | |

\#\#\# 2\.4 Major Business Processes

| Process | Description |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| 1\. Lead Capture | Capture lead from any source |

| 2\. Lead Assignment | Assign lead to sales representative |

| 3\. Lead Status Tracking | Track lead through sales funnel |

| 4\. Lead Scoring | AI\-assisted lead scoring \(future\) |

| 5\. Lead Conversion | Convert lead to case |

\#\#\# 2\.5 State Model

\`\`\`

New → Assigned → Contacted → Qualified → Converted → Lost → Archived

\`\`\`

\#\#\# 2\.6 Business Rules

| Rule ID | Description |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| BR\-LEAD\-001 | Duplicate leads must be flagged |

| BR\-LEAD\-002 | Leads older than 30 days without activity are auto\-closed |

| BR\-LEAD\-003 | Lead source must be tracked for attribution |

| BR\-LEAD\-004 | Connector leads require connector ID |

\#\#\# 2\.7 Data Ownership

\*\*Owned Tables:\*\*

\- \`TRN\_Lead\`

\- \`TRN\_LeadSource\`

\#\#\# 2\.8 CRUD Matrix

| Table | Create | Read | Update | Delete |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| TRN\_Lead | Sales | All | Sales | Admin |

| TRN\_LeadSource | System/Sales | All | Sales | Admin |

\#\#\# 2\.9 Events Published & Consumed

| Event | Type |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-|

| LeadCreated | Published |

| LeadAssigned | Published |

| LeadQualified | Published |

| LeadConverted | Published |

| LeadLost | Published |

\#\#\# 2\.10 Configuration Dependencies

\- \`REF\_Priority\`

\- \`REF\_Status\`

\- \`CFG\_CompanySettings\`

\#\#\# 2\.11 Security

| Aspect | Detail |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Classification\*\* | Operational Data |

| \*\*Sensitivity\*\* | Internal |

| \*\*Access Control\*\* | Sales role; all for read |

\#\#\# 2\.12 Performance Expectations

| Metric | Target |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Expected Volume\*\* | High |

| \*\*Read/Write Pattern\*\* | Mixed |

| \*\*Typical SLA\*\* | Real\-time |

\#\#\# 2\.13 Error Handling

| Failure | Action |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| Duplicate lead | Queue for review |

| Invalid connector | Flag, reject |

\#\#\# 2\.14 Audit

All lead activities logged via \`SEC\_AuditTrail\`\.

\#\#\# 2\.15 AI Participation

| AI Capability | Participation |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| AI Reads | Yes |

| AI Learns | Yes \(conversion patterns\) |

| AI Suggests | Future \(lead scoring\) |

| AI Validates | No |

| AI Scores | Future \(lead scoring\) |

| Human Approval Required | No |

\#\#\# 2\.16 Future Enhancements

\- AI\-based lead scoring

\- Automated lead assignment

\- Lead routing based on connector performance

\-\-\-

\#\# 3\. Customer Management Module

\#\#\# 3\.1 Module Overview

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Module ID\*\* | MOD\-014 |

| \*\*Module Name\*\* | Customer Management |

| \*\*Module Group\*\* | CRM & Sales |

| \*\*Business Owner\*\* | Sales / Operations |

| \*\*Data Steward\*\* | Data Operations |

| \*\*Phase Classification\*\* | Phase 1 |

\#\#\# 3\.2 Objective & Business Purpose

\*\*Objective:\*\* Manage customer master data and KYC lifecycle\.

\*\*Business Purpose:\*\* Maintains a single source of truth for all customer data\.

\#\#\# 3\.3 Scope

| In Scope | Out of Scope |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Customer master data | Lead management \(handled by Lead Management\) |

| KYC management | |

| Customer identification | |

| Duplicate detection | |

\#\#\# 3\.4 Major Business Processes

| Process | Description |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| 1\. Customer Creation | Create new customer records |

| 2\. KYC Verification | Verify customer identity and documents |

| 3\. Customer Update | Update customer information |

| 4\. Duplicate Detection | Detect and resolve duplicate customers |

\#\#\# 3\.5 State Model

\`\`\`

Created → KYC Pending → KYC Verified → Active → Inactive → Archived

\`\`\`

\#\#\# 3\.6 Business Rules

| Rule ID | Description |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| BR\-CUST\-001 | PAN is mandatory for all customers |

| BR\-CUST\-002 | KYC must be verified before case creation |

| BR\-CUST\-003 | Duplicate PANs must be prevented |

| BR\-CUST\-004 | Customer data changes require audit |

\#\#\# 3\.7 Data Ownership

\*\*Owned Tables:\*\*

\- \`MST\_Party\`

\- \`MST\_Customer\`

\- \`MST\_PartyAddress\`

\- \`MST\_PartyContact\`

\- \`MST\_PartyBankAccount\`

\#\#\# 3\.8 CRUD Matrix

| Table | Create | Read | Update | Delete |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| MST\_Party | Sales/Ops | All | Sales/Ops | Admin |

| MST\_Customer | Sales/Ops | All | Sales/Ops | Admin |

| MST\_PartyAddress | Sales/Ops | All | Sales/Ops | Admin |

| MST\_PartyContact | Sales/Ops | All | Sales/Ops | Admin |

| MST\_PartyBankAccount | Sales/Ops | All | Sales/Ops | Admin |

\#\#\# 3\.9 Events Published & Consumed

| Event | Type |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-|

| CustomerCreated | Published |

| CustomerKYCVerified | Published |

| CustomerUpdated | Published |

| CustomerMerged | Published |

\#\#\# 3\.10 Configuration Dependencies

\- \`REF\_\` tables \(Gender, Marital Status, Occupation, etc\.\)

\- \`AUD\_Document\` \(for KYC documents\)

\#\#\# 3\.11 Security

| Aspect | Detail |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Classification\*\* | Master Data |

| \*\*Sensitivity\*\* | Restricted \(PII\) |

| \*\*Access Control\*\* | Role\-based with masking |

\#\#\# 3\.12 Performance Expectations

| Metric | Target |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Expected Volume\*\* | Medium |

| \*\*Read/Write Pattern\*\* | Mixed |

| \*\*Typical SLA\*\* | Real\-time |

\#\#\# 3\.13 Error Handling

| Failure | Action |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| Duplicate PAN | Prevent creation, flag |

| Invalid KYC | Reject, notify user |

\#\#\# 3\.14 Audit

All customer changes logged via \`SEC\_AuditTrail\`\.

\#\#\# 3\.15 AI Participation

| AI Capability | Participation |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| AI Reads | Yes |

| AI Learns | Yes |

| AI Suggests | Yes \(duplicate detection\) |

| AI Validates | No |

| AI Scores | Yes \(Duplicate Confidence\) |

| Human Approval Required | Yes \(for merges\) |

\#\#\# 3\.16 Future Enhancements

\- AI\-assisted KYC verification

\- External PAN/GSTIN validation

\-\-\-

\#\# 4\. Connector Management Module

\#\#\# 4\.1 Module Overview

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Module ID\*\* | MOD\-015 |

| \*\*Module Name\*\* | Connector Management |

| \*\*Module Group\*\* | CRM & Sales |

| \*\*Business Owner\*\* | Partnerships |

| \*\*Data Steward\*\* | Channel Operations |

| \*\*Phase Classification\*\* | Phase 1 |

\#\#\# 4\.2 Objective & Business Purpose

\*\*Objective:\*\* Manage channel partner \(connector\) master data and performance\.

\*\*Business Purpose:\*\* Maintains connector relationships, commissions, and performance tracking\.

\#\#\# 4\.3 Scope

| In Scope | Out of Scope |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Connector master data | Commission calculation \(handled by Commission Management\) |

| Connector hierarchy | |

| Connector performance | |

| Connector bank details | |

\#\#\# 4\.4 Major Business Processes

| Process | Description |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| 1\. Connector Onboarding | Create new connector records |

| 2\. Connector Hierarchy | Manage multi\-level hierarchy |

| 3\. Connector Performance | Track connector performance metrics |

| 4\. Connector Settlement | Manage connector payouts |

\#\#\# 4\.5 State Model

\`\`\`

Created → Active → Inactive → Archived

\`\`\`

\#\#\# 4\.6 Business Rules

| Rule ID | Description |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| BR\-CON\-001 | Connector PAN must be unique |

| BR\-CON\-002 | Connector hierarchy must be valid |

| BR\-CON\-003 | Connector payouts require bank details |

\#\#\# 4\.7 Data Ownership

\*\*Owned Tables:\*\*

\- \`MST\_Connector\`

\- \`MST\_ConnectorBank\`

\- \`MST\_ConnectorHierarchy\`

\#\#\# 4\.8 CRUD Matrix

| Table | Create | Read | Update | Delete |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| MST\_Connector | Partnerships | All | Partnerships | Admin |

| MST\_ConnectorBank | Partnerships | All | Partnerships | Admin |

| MST\_ConnectorHierarchy | Partnerships | All | Partnerships | Admin |

\#\#\# 4\.9 Events Published & Consumed

| Event | Type |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-|

| ConnectorCreated | Published |

| ConnectorUpdated | Published |

\#\#\# 4\.10 Configuration Dependencies

\- \`REF\_\` tables

\- \`RUL\_CommissionRule\`

\#\#\# 4\.11 Security

| Aspect | Detail |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Classification\*\* | Master Data |

| \*\*Sensitivity\*\* | Internal |

| \*\*Access Control\*\* | Partnerships role |

\#\#\# 4\.12 Performance Expectations

| Metric | Target |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Expected Volume\*\* | Medium |

| \*\*Read/Write Pattern\*\* | Mixed |

| \*\*Typical SLA\*\* | Real\-time |

\#\#\# 4\.13 Future Enhancements

\- Connector performance dashboards

\- Automated tier upgrades

\-\-\-

\#\# 5\. Case Management Module

\#\#\# 5\.1 Module Overview

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Module ID\*\* | MOD\-016 |

| \*\*Module Name\*\* | Case Management |

| \*\*Module Group\*\* | Loan Operations |

| \*\*Business Owner\*\* | Operations |

| \*\*Data Steward\*\* | Operations Lead |

| \*\*Phase Classification\*\* | Phase 3 |

\#\#\# 5\.2 Objective & Business Purpose

\*\*Objective:\*\* Manage the complete lifecycle of a loan case from lead to closure\.

\*\*Business Purpose:\*\* Tracks all operational milestones, financials, and TAT\.

\#\#\# 5\.3 Scope

| In Scope | Out of Scope |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Case creation | Document management \(handled by Document Management\) |

| Case status tracking | |

| Document collection | |

| Verification | |

| Sanction | |

| Disbursement | |

| Closure | |

\#\#\# 5\.4 Major Business Processes

| Process | Description |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| 1\. Case Creation | Create case from lead |

| 2\. Document Collection | Collect KYC and loan documents |

| 3\. Verification | Verify documents and eligibility |

| 4\. Sanction | Lender sanction |

| 5\. Disbursement | Loan disbursement |

| 6\. Closure | Case closure |

\#\#\# 5\.5 State Model

\`\`\`

Lead → Application → Sanctioned → Disbursed → Closed → Archived

\`\`\`

\#\#\# 5\.6 Business Rules

| Rule ID | Description |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| BR\-CASE\-001 | Case must have a valid Customer, Lender, and Product |

| BR\-CASE\-002 | Disbursement requires complete KYC |

| BR\-CASE\-003 | TAT tracked from Lead to Disbursement |

| BR\-CASE\-004 | Sanction must precede disbursement |

| BR\-CASE\-005 | Disbursement amount cannot exceed sanction amount |

\#\#\# 5\.7 Data Ownership

\*\*Owned Tables:\*\*

\- \`TRN\_Case\`

\- \`TRN\_CaseStatusHistory\`

\- \`TRN\_Disbursement\`

\#\#\# 5\.8 CRUD Matrix

| Table | Create | Read | Update | Delete |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| TRN\_Case | Ops | All | Ops | Admin |

| TRN\_CaseStatusHistory | System | All | System | Admin |

| TRN\_Disbursement | Ops | All | Ops | Admin |

\#\#\# 5\.9 Events Published & Consumed

| Event | Type |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-|

| CaseCreated | Published |

| CaseSanctioned | Published |

| CaseDisbursed | Published |

| CaseClosed | Published |

| LeadConverted | Consumed \(from Lead Management\) |

\#\#\# 5\.10 Configuration Dependencies

\- \`RUL\_Workflow\`

\- \`RUL\_ValidationRule\`

\- \`MST\_Customer\`

\- \`MST\_Lender\`

\- \`MST\_Product\`

\- \`MST\_LenderAgreement\`

\#\#\# 5\.11 Security

| Aspect | Detail |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Classification\*\* | Operational Data |

| \*\*Sensitivity\*\* | Confidential |

| \*\*Access Control\*\* | Ops role; Finance for read |

\#\#\# 5\.12 Performance Expectations

| Metric | Target |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Expected Volume\*\* | High \(10,000\+ cases/year\) |

| \*\*Read/Write Pattern\*\* | Mixed |

| \*\*Typical SLA\*\* | Real\-time for updates, Batch for imports |

\#\#\# 5\.13 Error Handling

| Failure | Action |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| Validation failure | Case held for correction |

| Missing documents | Flag, notify |

| Incomplete KYC | Hold disbursement |

\#\#\# 5\.14 Audit

All case activities logged via \`SEC\_AuditTrail\` and \`TRN\_CaseStatusHistory\`\.

\#\#\# 5\.15 AI Participation

| AI Capability | Participation |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| AI Reads | Yes |

| AI Learns | Yes \(TAT patterns\) |

| AI Suggests | Yes \(TAT prediction\) |

| AI Validates | No |

| AI Scores | No |

| Human Approval Required | No |

\#\#\# 5\.16 Future Enhancements

\- AI\-based TAT prediction

\- Automated case routing

\- Document auto\-verification

\-\-\-

\#\# 6\. Revenue Management Module

\#\#\# 6\.1 Module Overview

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Module ID\*\* | MOD\-017 |

| \*\*Module Name\*\* | Revenue Management |

| \*\*Module Group\*\* | Finance |

| \*\*Business Owner\*\* | Finance |

| \*\*Data Steward\*\* | Finance Operations |

| \*\*Phase Classification\*\* | Phase 3 |

\#\#\# 6\.2 Objective & Business Purpose

\*\*Objective:\*\* Manage commission income from lenders \(Base Revenue \+ Campaign Incentives\)\.

\*\*Business Purpose:\*\* Tracks the DSA's primary revenue stream\.

\#\#\# 6\.3 Scope

| In Scope | Out of Scope |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Revenue calculation | Connector payouts \(handled by Commission Management\) |

| Revenue posting | |

| Revenue reconciliation | |

| Revenue adjustment | |

\#\#\# 6\.4 Major Business Processes

| Process | Description |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| 1\. Revenue Calculation | Calculate commission income |

| 2\. Revenue Posting | Post revenue to financial records |

| 3\. Revenue Reconciliation | Reconcile with lender payments |

| 4\. Revenue Adjustment | Adjust revenue with approval |

\#\#\# 6\.5 State Model

\`\`\`

Calculated → Validated → Approved → Posted → Reconciled → Adjusted

\`\`\`

\#\#\# 6\.6 Business Rules

| Rule ID | Description |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| BR\-REV\-001 | Revenue cannot be posted without a valid Case |

| BR\-REV\-002 | Approved revenue is immutable; corrections require adjustment entries |

| BR\-REV\-003 | Revenue must reconcile with lender reports |

| BR\-REV\-004 | Campaign incentives tracked separately |

\#\#\# 6\.7 Data Ownership

\*\*Owned Tables:\*\*

\- \`TRN\_Revenue\`

\- \`TRN\_CampaignIncentive\`

\#\#\# 6\.8 CRUD Matrix

| Table | Create | Read | Update | Delete |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| TRN\_Revenue | System | All | Finance \(adjustments\) | Admin |

| TRN\_CampaignIncentive | System | All | Finance | Admin |

\#\#\# 6\.9 Events Published & Consumed

| Event | Type |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-|

| RevenuePosted | Published |

| RevenueReconciled | Published |

| RevenueAdjusted | Published |

| CaseDisbursed | Consumed \(from Case Management\) |

\#\#\# 6\.10 Configuration Dependencies

\- \`RUL\_CommissionRule\`

\- \`RUL\_GSTRule\`

\- \`RUL\_TDSRule\`

\- \`MST\_LenderAgreement\`

\#\#\# 6\.11 Security

| Aspect | Detail |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Classification\*\* | Financial Data |

| \*\*Sensitivity\*\* | Restricted |

| \*\*Access Control\*\* | Finance for adjustments; all for read |

\#\#\# 6\.12 Performance Expectations

| Metric | Target |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Expected Volume\*\* | High |

| \*\*Read/Write Pattern\*\* | Mixed |

| \*\*Typical SLA\*\* | Batch window |

\#\#\# 6\.13 Error Handling

| Failure | Action |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| Calculation errors | Rollback, recalculate |

| Reconciliation errors | Flag for review |

\#\#\# 6\.14 Audit

All revenue activities logged via \`SEC\_AuditTrail\` and \`ETL\_DataLineage\`\.

\#\#\# 6\.15 AI Participation

| AI Capability | Participation |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| AI Reads | No |

| AI Learns | No |

| AI Suggests | No |

| AI Validates | Future \(anomaly detection\) |

| AI Scores | No |

| Human Approval Required | Yes \(for adjustments\) |

\#\#\# 6\.16 Future Enhancements

\- AI\-based revenue anomaly detection

\- Automated reconciliation

\-\-\-

\#\# 7\. Commission Management Module

\#\#\# 7\.1 Module Overview

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Module ID\*\* | MOD\-018 |

| \*\*Module Name\*\* | Commission Management |

| \*\*Module Group\*\* | Finance |

| \*\*Business Owner\*\* | Finance / Channel |

| \*\*Data Steward\*\* | Finance Operations |

| \*\*Phase Classification\*\* | Phase 3 |

\#\#\# 7\.2 Objective & Business Purpose

\*\*Objective:\*\* Manage payouts to connectors \(Sub\-DSAs\)\.

\*\*Business Purpose:\*\* Ensures timely and accurate payouts to channel partners\.

\#\#\# 7\.3 Scope

| In Scope | Out of Scope |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Connector commission calculation | Employee incentives \(handled by Incentive Management\) |

| Commission approval | |

| Commission payment | |

| Commission reconciliation | |

\#\#\# 7\.4 Major Business Processes

| Process | Description |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| 1\. Commission Calculation | Calculate connector payouts |

| 2\. Commission Approval | Approve payouts |

| 3\. Commission Payment | Process payments |

| 4\. Commission Reconciliation | Reconcile with payments |

\#\#\# 7\.5 State Model

\`\`\`

Calculated → Approved → Paid → Reconciled

\`\`\`

\#\#\# 7\.6 Business Rules

| Rule ID | Description |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| BR\-COMM\-001 | Commission cannot exceed available revenue |

| BR\-COMM\-002 | TDS applicable on connector payouts |

| BR\-COMM\-003 | Multiple connectors can split commission |

| BR\-COMM\-004 | Commission approval requires maker\-checker |

\#\#\# 7\.7 Data Ownership

\*\*Owned Tables:\*\*

\- \`TRN\_Commission\`

\- \`TRN\_CaseConnectorSplit\`

\#\#\# 7\.8 CRUD Matrix

| Table | Create | Read | Update | Delete |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| TRN\_Commission | System | All | Finance | Admin |

| TRN\_CaseConnectorSplit | Ops/System | All | Ops | Admin |

\#\#\# 7\.9 Events Published & Consumed

| Event | Type |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-|

| CommissionCalculated | Published |

| CommissionApproved | Published |

| CommissionPaid | Published |

| RevenuePosted | Consumed \(from Revenue Management\) |

\#\#\# 7\.10 Configuration Dependencies

\- \`RUL\_CommissionRule\`

\- \`RUL\_TDSRule\`

\- \`MST\_Connector\`

\- \`TRN\_CaseConnectorSplit\`

\#\#\# 7\.11 Security

| Aspect | Detail |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Classification\*\* | Financial Data |

| \*\*Sensitivity\*\* | Restricted |

| \*\*Access Control\*\* | Finance role |

\#\#\# 7\.12 Performance Expectations

| Metric | Target |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Expected Volume\*\* | High |

| \*\*Read/Write Pattern\*\* | Mixed |

| \*\*Typical SLA\*\* | Monthly/Weekly batch |

\#\#\# 7\.13 Error Handling

| Failure | Action |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| Calculation errors | Rollback, recalculate |

| Insufficient funds | Pending approval |

\#\#\# 7\.14 Audit

All commission activities logged via \`SEC\_AuditTrail\`\.

\#\#\# 7\.15 AI Participation

| AI Capability | Participation |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| AI Reads | No |

| AI Learns | No |

| AI Suggests | No |

| AI Validates | No |

| AI Scores | No |

| Human Approval Required | Yes |

\#\#\# 7\.16 Future Enhancements

\- AI\-based commission optimisation

\- Automated dispute resolution

\-\-\-

\#\# 8\. Incentive Management Module

\#\#\# 8\.1 Module Overview

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Module ID\*\* | MOD\-019 |

| \*\*Module Name\*\* | Incentive Management |

| \*\*Module Group\*\* | Finance / HR |

| \*\*Business Owner\*\* | Finance / HR |

| \*\*Data Steward\*\* | Finance Operations |

| \*\*Phase Classification\*\* | Phase 3 |

\#\#\# 8\.2 Objective & Business Purpose

\*\*Objective:\*\* Manage employee success fees and incentives\.

\*\*Business Purpose:\*\* Aligns employee behaviour with organisational goals\.

\#\#\# 8\.3 Scope

| In Scope | Out of Scope |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Employee incentive calculation | Salary payroll \(future\) |

| Incentive approval | |

| Incentive payment | |

| Incentive reconciliation | |

\#\#\# 8\.4 Major Business Processes

| Process | Description |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| 1\. Incentive Calculation | Calculate employee success fees |

| 2\. Incentive Approval | Approve incentives |

| 3\. Incentive Payment | Process payments |

| 4\. Incentive Reconciliation | Reconcile with payments |

\#\#\# 8\.5 State Model

\`\`\`

Calculated → Approved → Paid → Reconciled

\`\`\`

\#\#\# 8\.6 Business Rules

| Rule ID | Description |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| BR\-INC\-001 | Incentive rules must be configurable |

| BR\-INC\-002 | Multiple employees can split case incentives |

| BR\-INC\-003 | Incentive approval requires manager approval |

| BR\-INC\-004 | TDS applicable on employee incentives |

\#\#\# 8\.7 Data Ownership

\*\*Owned Tables:\*\*

\- \`TRN\_IncentiveEarned\`

\- \`TRN\_CaseEmployeeSplit\`

\#\#\# 8\.8 CRUD Matrix

| Table | Create | Read | Update | Delete |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| TRN\_IncentiveEarned | System | All | Finance/HR | Admin |

| TRN\_CaseEmployeeSplit | Ops/System | All | Ops | Admin |

\#\#\# 8\.9 Events Published & Consumed

| Event | Type |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-|

| IncentiveCalculated | Published |

| IncentivePaid | Published |

| RevenuePosted | Consumed \(from Revenue Management\) |

\#\#\# 8\.10 Configuration Dependencies

\- \`RUL\_InternalIncentiveScheme\`

\- \`RUL\_TDSRule\`

\- \`MST\_Employee\`

\- \`TRN\_CaseEmployeeSplit\`

\#\#\# 8\.11 Security

| Aspect | Detail |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Classification\*\* | Financial Data |

| \*\*Sensitivity\*\* | Restricted |

| \*\*Access Control\*\* | Finance/HR role |

\#\#\# 8\.12 Performance Expectations

| Metric | Target |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Expected Volume\*\* | High |

| \*\*Read/Write Pattern\*\* | Mixed |

| \*\*Typical SLA\*\* | Monthly batch |

\#\#\# 8\.13 Future Enhancements

\- AI\-based incentive optimisation

\- Gamification integration

\- Real\-time incentive tracking

\-\-\-

\#\# 9\. Expense Management Module

\#\#\# 9\.1 Module Overview

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Module ID\*\* | MOD\-020 |

| \*\*Module Name\*\* | Expense Management |

| \*\*Module Group\*\* | Finance |

| \*\*Business Owner\*\* | Finance / Operations |

| \*\*Data Steward\*\* | Finance Operations |

| \*\*Phase Classification\*\* | Phase 4 |

\#\#\# 9\.2 Objective & Business Purpose

\*\*Objective:\*\* Manage all operational expenses \(office, travel, vendors, recurring costs\)\.

\*\*Business Purpose:\*\* Tracks all outflows, enabling profitability analysis and budgeting\.

\#\#\# 9\.3 Scope

| In Scope | Out of Scope |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Operational expenses | Connector payouts \(handled by Commission Management\) |

| Recurring expenses | |

| Employee claims | |

| Vendor payments | |

| Cost allocation | |

\#\#\# 9\.4 Major Business Processes

| Process | Description |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| 1\. Expense Capture | Capture expense transactions |

| 2\. Expense Approval | Approve expenses |

| 3\. Expense Payment | Process payments |

| 4\. Expense Reconciliation | Reconcile with payments |

| 5\. Cost Allocation | Allocate costs to cost centres |

\#\#\# 9\.5 State Model

\`\`\`

Draft → Submitted → Approved → Paid → Reconciled

\`\`\`

\#\#\# 9\.6 Business Rules

| Rule ID | Description |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| BR\-EXP\-001 | Expense must have valid category and cost centre |

| BR\-EXP\-002 | Expenses above threshold require manager approval |

| BR\-EXP\-003 | GST/TDS applicable on vendor expenses |

| BR\-EXP\-004 | Recurring expenses auto\-generated |

\#\#\# 9\.7 Data Ownership

\*\*Owned Tables:\*\*

\- \`TRN\_Expense\`

\- \`TRN\_RecurringExpense\`

\- \`TRN\_ExpenseClaim\`

\- \`TRN\_CaseCost\`

\#\#\# 9\.8 CRUD Matrix

| Table | Create | Read | Update | Delete |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| TRN\_Expense | Ops/Finance | All | Finance | Admin |

| TRN\_RecurringExpense | Finance | All | Finance | Admin |

| TRN\_ExpenseClaim | Employee | All | Finance | Admin |

| TRN\_CaseCost | System | All | System | Admin |

\#\#\# 9\.9 Events Published & Consumed

| Event | Type |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-|

| ExpenseSubmitted | Published |

| ExpenseApproved | Published |

| ExpensePaid | Published |

\#\#\# 9\.10 Configuration Dependencies

\- \`MST\_Vendor\`

\- \`MST\_ExpenseCategory\`

\- \`MST\_CostCenter\`

\- \`RUL\_GSTRule\`

\- \`RUL\_TDSRule\`

\#\#\# 9\.11 Security

| Aspect | Detail |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Classification\*\* | Financial Data |

| \*\*Sensitivity\*\* | Internal |

| \*\*Access Control\*\* | Finance role |

\#\#\# 9\.12 Performance Expectations

| Metric | Target |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Expected Volume\*\* | High |

| \*\*Read/Write Pattern\*\* | Mixed |

| \*\*Typical SLA\*\* | Real\-time for claims, Batch for vendor bills |

\#\#\# 9\.13 Future Enhancements

\- AI\-based expense categorisation

\- OCR for vendor invoices

\- Budget vs actual monitoring

\-\-\-

\#\# 10\. Payment Management Module

\#\#\# 10\.1 Module Overview

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Module ID\*\* | MOD\-021 |

| \*\*Module Name\*\* | Payment Management |

| \*\*Module Group\*\* | Finance |

| \*\*Business Owner\*\* | Finance / Treasury |

| \*\*Data Steward\*\* | Treasury Operations |

| \*\*Phase Classification\*\* | Phase 4 |

\#\#\# 10\.2 Objective & Business Purpose

\*\*Objective:\*\* Manage all outbound payments and bank reconciliation\.

\*\*Business Purpose:\*\* Centralises all outflows and enables BRS\.

\#\#\# 10\.3 Scope

| In Scope | Out of Scope |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Payment initiation | Payment processing \(bank integration\) |

| UTR capture | |

| Bank reconciliation \(BRS\) | |

| Tally integration | |

\#\#\# 10\.4 Major Business Processes

| Process | Description |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| 1\. Payment Initiation | Initiate outbound payments |

| 2\. UTR Capture | Capture UTR numbers |

| 3\. Bank Reconciliation \(BRS\) | Match payments with bank statements |

| 4\. Tally Export | Export to Tally |

\#\#\# 10\.5 State Model

\`\`\`

Initiated → Pending UTR → UTR Captured → Reconciled → Exported to Tally

\`\`\`

\#\#\# 10\.6 Business Rules

| Rule ID | Description |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| BR\-PAY\-001 | UTR numbers must be unique \(DB constraint\) |

| BR\-PAY\-002 | Reconciliation requires UTR matching |

| BR\-PAY\-003 | Payment approval requires maker\-checker |

| BR\-PAY\-004 | High\-value payments require additional approval |

\#\#\# 10\.7 Data Ownership

\*\*Owned Tables:\*\*

\- \`TRN\_Payment\`

\- \`TRN\_UTRLock\`

\- \`TRN\_BankStatementLine\`

\- \`TRN\_TallyExportBatch\`

\- \`TRN\_TallyExportDetail\`

\#\#\# 10\.8 CRUD Matrix

| Table | Create | Read | Update | Delete |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| TRN\_Payment | Finance | All | Finance | Admin |

| TRN\_UTRLock | System | All | System | Admin |

| TRN\_BankStatementLine | Finance | All | Finance | Admin |

| TRN\_TallyExportBatch | System | All | System | Admin |

| TRN\_TallyExportDetail | System | All | System | Admin |

\#\#\# 10\.9 Events Published & Consumed

| Event | Type |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-|

| PaymentCreated | Published |

| PaymentReconciled | Published |

| TallyExportGenerated | Published |

\#\#\# 10\.10 Configuration Dependencies

\- \`MST\_CompanyBankAccount\`

\- \`MST\_TallyMapping\`

\#\#\# 10\.11 Security

| Aspect | Detail |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Classification\*\* | Financial Data |

| \*\*Sensitivity\*\* | Restricted |

| \*\*Access Control\*\* | Finance/Treasury role |

\#\#\# 10\.12 Performance Expectations

| Metric | Target |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Expected Volume\*\* | High |

| \*\*Read/Write Pattern\*\* | Mixed |

| \*\*Typical SLA\*\* | Real\-time for UTR entry, Batch for BRS |

\#\#\# 10\.13 Error Handling

| Failure | Action |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| UTR mismatch | Manual review |

| Duplicate UTR | Prevent, notify |

| Tally export failure | Retry, log |

\#\#\# 10\.14 Audit

All payment activities logged via \`SEC\_AuditTrail\`\.

\#\#\# 10\.15 AI Participation

| AI Capability | Participation |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| AI Reads | No |

| AI Learns | No |

| AI Suggests | No |

| AI Validates | Future \(fuzzy matching\) |

| AI Scores | No |

| Human Approval Required | Yes |

\#\#\# 10\.16 Future Enhancements

\- Automated BRS via OCR/direct bank API

\- Bulk payment processing

\- Real\-time bank integration

\-\-\-

\#\# 11\. Invoice Management Module

\#\#\# 11\.1 Module Overview

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Module ID\*\* | MOD\-022 |

| \*\*Module Name\*\* | Invoice Management |

| \*\*Module Group\*\* | Finance |

| \*\*Business Owner\*\* | Finance |

| \*\*Data Steward\*\* | Finance Operations |

| \*\*Phase Classification\*\* | Phase 3 |

\#\#\# 11\.2 Objective & Business Purpose

\*\*Objective:\*\* Manage invoice generation and tracking\.

\*\*Business Purpose:\*\* Enables timely and accurate invoicing to lenders\.

\#\#\# 11\.3 Scope

| In Scope | Out of Scope |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Invoice generation | Payment processing \(handled by Payment Management\) |

| Invoice tracking | |

| Invoice reconciliation | |

| GST/TDS calculation | |

\#\#\# 11\.4 Major Business Processes

| Process | Description |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| 1\. Invoice Generation | Generate invoices for revenue |

| 2\. Invoice Submission | Submit to lenders |

| 3\. Invoice Tracking | Track payment status |

| 4\. Invoice Reconciliation | Reconcile with payments |

\#\#\# 11\.5 State Model

\`\`\`

Generated → Sent → Due → Paid → Reconciled → Adjusted

\`\`\`

\#\#\# 11\.6 Business Rules

| Rule ID | Description |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| BR\-INV\-001 | Invoice must have a valid Case |

| BR\-INV\-002 | Invoice due date determined by agreement |

| BR\-INV\-003 | GST/TDS must be correctly calculated |

| BR\-INV\-004 | Approved invoices are immutable |

\#\#\# 11\.7 Data Ownership

\*\*Owned Tables:\*\*

\- \`TRN\_Invoice\`

\#\#\# 11\.8 CRUD Matrix

| Table | Create | Read | Update | Delete |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| TRN\_Invoice | System | All | Finance | Admin |

\#\#\# 11\.9 Events Published & Consumed

| Event | Type |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-|

| InvoiceGenerated | Published |

| InvoicePaid | Published |

| RevenuePosted | Consumed \(from Revenue Management\) |

\#\#\# 11\.10 Configuration Dependencies

\- \`MST\_LenderAgreement\`

\- \`RUL\_GSTRule\`

\- \`RUL\_TDSRule\`

\#\#\# 11\.11 Security

| Aspect | Detail |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Classification\*\* | Financial Data |

| \*\*Sensitivity\*\* | Confidential |

| \*\*Access Control\*\* | Finance role |

\#\#\# 11\.12 Performance Expectations

| Metric | Target |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Expected Volume\*\* | High |

| \*\*Read/Write Pattern\*\* | Mixed |

| \*\*Typical SLA\*\* | Batch window |

\#\#\# 11\.13 Future Enhancements

\- Automated invoice delivery

\- E\-invoicing integration

\-\-\-

\#\# 12\. Profitability Analysis Module

\#\#\# 12\.1 Module Overview

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Module ID\*\* | MOD\-023 |

| \*\*Module Name\*\* | Profitability Analysis |

| \*\*Module Group\*\* | Finance |

| \*\*Business Owner\*\* | Finance |

| \*\*Data Steward\*\* | Finance Operations |

| \*\*Phase Classification\*\* | Phase 4 |

\#\#\# 12\.2 Objective & Business Purpose

\*\*Objective:\*\* Calculate and report profitability at case, branch, product, lender, and company levels\.

\*\*Business Purpose:\*\* Enables management to understand and optimise profitability across all dimensions\.

\#\#\# 12\.3 Scope

| In Scope | Out of Scope |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Direct profitability | Tax calculations \(handled by Tax Management\) |

| Allocated overheads | |

| Contribution margin | |

| EBIDTA | |

| PAT | |

\#\#\# 12\.4 Major Business Processes

| Process | Description |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| 1\. Cost Allocation | Allocate overheads to cases |

| 2\. Profitability Calculation | Calculate all profitability metrics |

| 3\. Profitability Reporting | Generate profitability reports |

\#\#\# 12\.5 State Model

\`\`\`

Not Started → Calculating → Posted → Published

\`\`\`

\#\#\# 12\.6 Business Rules

| Rule ID | Description |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| BR\-PROF\-001 | Cost allocation rules must be configurable |

| BR\-PROF\-002 | Profitability must be calculable at all levels |

| BR\-PROF\-003 | Historical profitability must be preserved |

\#\#\# 12\.7 Data Ownership

\*\*Owned Tables:\*\*

\- \`BI\_CaseProfitability\_Detailed\`

\- \`BI\_PortfolioProfitability\`

\- \`TRN\_CostAllocation\`

\#\#\# 12\.8 CRUD Matrix

| Table | Create | Read | Update | Delete |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| BI\_CaseProfitability\_Detailed | System | All | System | Admin |

| BI\_PortfolioProfitability | System | All | System | Admin |

| TRN\_CostAllocation | System | All | System | Admin |

\#\#\# 12\.9 Configuration Dependencies

\- \`RUL\_CostAllocationRule\`

\- \`TRN\_Case\`

\- \`TRN\_Revenue\`

\- \`TRN\_Commission\`

\- \`TRN\_Expense\`

\- \`MST\_CostCenter\`

\#\#\# 12\.10 Security

| Aspect | Detail |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Classification\*\* | Financial Data |

| \*\*Sensitivity\*\* | Confidential |

| \*\*Access Control\*\* | Finance, Management |

\#\#\# 12\.11 Performance Expectations

| Metric | Target |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Expected Volume\*\* | Low \(per case\) |

| \*\*Read/Write Pattern\*\* | Mostly Read |

| \*\*Typical SLA\*\* | Monthly batch |

\#\#\# 12\.12 Future Enhancements

\- AI\-based profitability optimisation

\- Real\-time profitability

\-\-\-

\#\# 13\. Working Capital Management Module

\#\#\# 13\.1 Module Overview

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Module ID\*\* | MOD\-024 |

| \*\*Module Name\*\* | Working Capital Management |

| \*\*Module Group\*\* | Finance |

| \*\*Business Owner\*\* | Finance / Treasury |

| \*\*Data Steward\*\* | Treasury Operations |

| \*\*Phase Classification\*\* | Phase 4 |

\#\#\# 13\.2 Objective & Business Purpose

\*\*Objective:\*\* Monitor and manage the DSA's working capital requirement and cash conversion cycle\.

\*\*Business Purpose:\*\* Ensures liquidity and supports securitisation decisions\.

\#\#\# 13\.3 Scope

| In Scope | Out of Scope |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Cash conversion cycle | Cash management \(handled by Treasury\) |

| Receivables | |

| Overdue tracking | |

| Securitisation eligibility | |

\#\#\# 13\.4 Major Business Processes

| Process | Description |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| 1\. Track Receivables | Track outstanding receivables |

| 2\. Calculate CCC | Calculate cash conversion cycle |

| 3\. Monitor Overdue | Monitor overdue receivables |

| 4\. Securitisation Readiness | Assess securitisation eligibility |

\#\#\# 13\.5 State Model

\`\`\`

Not Started → Calculating → Published

\`\`\`

\#\#\# 13\.6 Business Rules

| Rule ID | Description |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| BR\-WC\-001 | CCC must be calculated for every case |

| BR\-WC\-002 | Overdue receivables must be flagged |

| BR\-WC\-003 | Securitisation eligibility must be configurable |

\#\#\# 13\.7 Data Ownership

\*\*Owned Tables:\*\*

\- \`BI\_PortfolioRiskSnapshot\`

\- \`TRN\_Case\` \(cash conversion cycle dates\)

\#\#\# 13\.8 CRUD Matrix

| Table | Create | Read | Update | Delete |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| BI\_PortfolioRiskSnapshot | System | All | System | Admin |

\#\#\# 13\.9 Configuration Dependencies

\- \`TRN\_Case\` \(disbursement/invoice dates\)

\- \`TRN\_Invoice\` \(outstanding\)

\- \`TRN\_Payment\` \(receipt dates\)

\#\#\# 13\.10 Security

| Aspect | Detail |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Classification\*\* | Financial Data |

| \*\*Sensitivity\*\* | Confidential |

| \*\*Access Control\*\* | Finance, Treasury, Management |

\#\#\# 13\.11 Performance Expectations

| Metric | Target |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Expected Volume\*\* | Low \(daily snapshot\) |

| \*\*Read/Write Pattern\*\* | Mostly Read |

| \*\*Typical SLA\*\* | Daily batch |

\#\#\# 13\.12 Future Enhancements

\- AI\-based cash flow prediction

\- Real\-time working capital dashboard

\-\-\-

\#\# 14\. Forecasting Engine Module

\#\#\# 14\.1 Module Overview

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Module ID\*\* | MOD\-025 |

| \*\*Module Name\*\* | Forecasting Engine |

| \*\*Module Group\*\* | Analytics |

| \*\*Business Owner\*\* | Finance / Strategy |

| \*\*Data Steward\*\* | Finance Operations |

| \*\*Phase Classification\*\* | Phase 5 |

\#\#\# 14\.2 Objective & Business Purpose

\*\*Objective:\*\* Generate forecasts for revenue, working capital, cash flow, and other key metrics\.

\*\*Business Purpose:\*\* Enables proactive planning and risk management\.

\#\#\# 14\.3 Scope

| In Scope | Out of Scope |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Statistical forecasting | Actual reporting |

| Trend analysis | |

| Scenario modelling | |

| Forecast validation | |

\#\#\# 14\.4 Major Business Processes

| Process | Description |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| 1\. Forecast Generation | Generate forecasts using statistical models |

| 2\. Scenario Analysis | Run scenario analysis |

| 3\. Forecast Validation | Validate forecast accuracy |

| 4\. Forecast Publication | Publish approved forecasts |

\#\#\# 14\.5 State Model

\`\`\`

Not Started → Generating → Validated → Published

\`\`\`

\#\#\# 14\.6 Business Rules

| Rule ID | Description |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| BR\-FCST\-001 | Forecasts must use at least 12 months of historical data |

| BR\-FCST\-002 | Forecasts require management approval for publication |

| BR\-FCST\-003 | Forecast accuracy must be continuously validated |

\#\#\# 14\.7 Data Ownership

\*\*Owned Tables:\*\*

\- \`BI\_ForecastModel\`

\- \`BI\_ForecastRun\`

\- \`BI\_ForecastPeriod\`

\- \`BI\_ForecastResult\`

\- \`BI\_ForecastAccuracy\`

\- \`BI\_ForecastDrivers\`

\#\#\# 14\.8 CRUD Matrix

| Table | Create | Read | Update | Delete |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| BI\_ForecastModel | Admin | All | Admin | Admin |

| BI\_ForecastRun | System | All | System | Admin |

| BI\_ForecastResult | System | All | System | Admin |

| BI\_ForecastAccuracy | System | All | System | Admin |

| BI\_ForecastDrivers | System | All | System | Admin |

\#\#\# 14\.9 Events Published & Consumed

| Event | Type |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-|

| ForecastGenerated | Published |

| ForecastPublished | Published |

| SnapshotUpdated | Consumed \(from Snapshot Generation\) |

\#\#\# 14\.10 Configuration Dependencies

\- \`BI\_ForecastModel\` \(statistical models\)

\- \`BI\_DailySnapshot\`

\- \`BI\_MonthlySnapshot\`

\- \`TRN\_Case\`

\#\#\# 14\.11 Security

| Aspect | Detail |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Classification\*\* | Analytical Data |

| \*\*Sensitivity\*\* | Internal |

| \*\*Access Control\*\* | Finance for publication; all for read |

\#\#\# 14\.12 Performance Expectations

| Metric | Target |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Expected Volume\*\* | Low \(per forecast run\) |

| \*\*Read/Write Pattern\*\* | Mostly Read |

| \*\*Typical SLA\*\* | Monthly batch |

\#\#\# 14\.13 AI Participation

| AI Capability | Participation |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| AI Reads | Yes |

| AI Learns | Yes \(from accuracy feedback\) |

| AI Suggests | Yes \(model selection\) |

| AI Validates | No |

| AI Scores | No |

| Human Approval Required | Yes \(for publishing\) |

\#\#\# 14\.14 Future Enhancements

\- AI\-based self\-optimising models

\- Real\-time forecasting

\- External data integration \(economic indicators\)

\-\-\-

\#\# 15\. Business Modules Gap Analysis & Resolution Register

\#\#\# 15\.1 Purpose

This section documents all identified gaps in the business module specifications and provides their resolution status\.

\#\#\# 15\.2 Gap Resolution Register

| ID | Area | Gap Description | Impact | Status | Resolution |

|\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|

| \*\*BM\-001\*\* | Lead Management | Lead scoring not defined | Medium | ✅ Resolved | Added to Future Enhancements |

| \*\*BM\-002\*\* | Customer Management | KYC workflow not fully defined | High | ✅ Resolved | Added to module specification |

| \*\*BM\-003\*\* | Case Management | Document collection workflow not defined | High | ✅ Resolved | Added to module specification |

| \*\*BM\-004\*\* | Revenue Management | Revenue adjustment process not defined | High | ✅ Resolved | Added to module specification |

| \*\*BM\-005\*\* | Commission Management | Split commission not fully defined | High | ✅ Resolved | Added to module specification |

| \*\*BM\-006\*\* | Incentive Management | Competition bonuses not defined | Medium | ✅ Resolved | Added to module specification |

| \*\*BM\-007\*\* | Expense Management | Recurring expense not fully defined | Medium | ✅ Resolved | Added to module specification |

| \*\*BM\-008\*\* | Payment Management | Bulk payment not supported | Medium | ✅ Resolved | Added to Future Enhancements |

| \*\*BM\-009\*\* | Invoice Management | Invoice adjustment not defined | Medium | ✅ Resolved | Added to module specification |

| \*\*BM\-010\*\* | Profitability | Cost allocation rules not fully defined | High | ✅ Resolved | Added to module specification |

| \*\*BM\-011\*\* | Working Capital | Securitisation readiness not defined | Medium | ✅ Resolved | Added to module specification |

| \*\*BM\-012\*\* | Forecasting | Forecast model selection not defined | Medium | ✅ Resolved | Added to module specification |

\#\#\# 15\.3 Deferred Gaps \(Future Versions\)

| ID | Area | Gap Description | Target Version | Rationale |

|\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|

| \*\*BM\-013\*\* | Collections | Collections & recovery module | V1\.1\+ | Outside initial DSA scope |

| \*\*BM\-014\*\* | Payroll | Payroll processing | V1\.1\+ | Outside initial scope |

| \*\*BM\-015\*\* | CRM | Full CRM capabilities | V2\.0 | Not required initially |

| \*\*BM\-016\*\* | AI | AI\-based lead scoring | V2\.0 | Requires AI maturity |

\-\-\-

\#\# 16\. Document Status & Approval

\#\#\# 16\.1 Document Status

| Status | Approved / Frozen |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \*\*Version\*\* | 1\.0 |

| \*\*Date\*\* | July 2026 |

| \*\*Next Review\*\* | Annual or before major architectural change |

| \*\*Owner\*\* | CTO |

\#\#\# 16\.2 Document Freeze Notice

\*\*This document is designated as an Architecture Baseline Artefact\.\*\*

\*\*Following approval:\*\*

\- Structural changes to business module specifications require a new Architecture Decision Record \(ADR\)\.

\- Changes to module interfaces require Architecture Review Board \(ARB\) approval\.

\- All business module implementation shall use this document as the governing baseline\.

\- All implementation teams shall treat this document as frozen unless superseded by a formally approved revision\.

\*\*Freeze Status:\*\* ✅ \*\*FROZEN\*\*

\#\#\# 16\.3 Approval Sign\-Off

| Role | Name | Signature | Date |

|\-\-\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-|

| Enterprise Architect | Architecture Review Board | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

| Business Lead | \_\[Name\]\_ | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

| Finance Lead | \_\[Name\]\_ | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

| Operations Lead | \_\[Name\]\_ | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

| CTO | \_\[ChatGPT\]\_ | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

| Technical Programme Manager | \_\[DeepSeek\]\_ | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

| Development Lead | \_\[Aniket\]\_ | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

\#\#\# 16\.4 Cross\-Reference to Repository Documents

| Document | Relationship |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| DOC\-000 | Repository structure referencing this document |

| DOC\-001 | Repository guide referencing this document |

| DOC\-002 | Dependency matrix including this document |

| DOC\-003 | Master index including this document |

| DOC\-010 | Architecture & ADRs referencing module design |

| DOC\-011 | Data Model referencing module tables |

| DOC\-013 | Application Development Standards referencing module implementation |

| DOC\-014 | Finance & Operations Specifications referencing module logic |

| DOC\-015 | AI & Data Engineering referencing AI modules |

| DOC\-016 | Security & Governance referencing module security |

| DOC\-017 | Core Modules referencing shared services |

\-\-\-

\#\# End of Document

\*\*Document ID:\*\* DOC\-018  

\*\*Document Name:\*\* \*Business Module Specifications Consolidated\*  

\*\*Version:\*\* 1\.0  

\*\*Status:\*\* Approved / Frozen  

\*\*Owner:\*\* CTO

