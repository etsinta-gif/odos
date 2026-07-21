# DOC-021 – FCPL Industry Configuration Specification

\# DOC\-021: FCPL Industry Configuration Specification

\*\*Document ID:\*\* DOC\-021  

\*\*Version:\*\* 1\.0  

\*\*Status:\*\* Approved / Frozen  

\*\*Owner:\*\* CTO \(ChatGPT\)  

\*\*Classification:\*\* Industry Configuration Specification  

\*\*Purpose:\*\* Define all industry\-specific \(DSA/FCPL\) configuration data that maps to the Canonical Model \(DOC\-011\)\. This document serves as the authoritative reference for configuring the ODOS platform for the Fineoteric Consulting Pvt Ltd \(FCPL\) DSA pilot\.

\-\-\-

\#\# Table of Contents

1\. Executive Summary

2\. Organizational Structure

3\. Product Taxonomy

4\. Lender/Bank Master

5\. Connector Master

6\. Reference Data

7\. Profile Types

8\. Configuration Cross\-Reference

9\. Document Status & Approval

\-\-\-

\#\# 1\. Executive Summary

\#\#\# 1\.1 Purpose

This document defines all industry\-specific configuration data required to operationalise the ODOS platform for the FCPL DSA pilot\. It maps FCPL's business entities, products, lenders, connectors, and reference data to the canonical enterprise data model defined in DOC\-011\.

\#\#\# 1\.2 Scope

| Area | Coverage |

|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|

| Organizational Structure | FCPL hierarchy: regions, branches, teams |

| Product Taxonomy | BL, PL, HL, LAP, SBL\-TL, SBL\-OD, BL\-TL, BL\-OD |

| Lender Master | 25\+ banks/NBFCs with classification |

| Connector Master | 700\+ connectors with hierarchy and bank details |

| Reference Data | Statuses, priorities, document types, payment statuses |

| Profile Types | SENP, SALARIED, N/A |

\#\#\# 1\.3 FCPL Operating Context

FCPL operates as a Direct Selling Agent \(DSA\) originating loan applications across multiple product categories and lender partners\. The business operates through:

\- \*\*2 Primary DSAs\*\*: FCPL and BW

\- \*\*Multiple Regions\*\*: ANDHERI, PUNE, DELHI, MUMBAI, etc\.

\- \*\*Connector Network\*\*: 700\+ active connectors/agents

\- \*\*Lender Partners\*\*: 25\+ banks and NBFCs

\- \*\*Products\*\*: Business Loans, Personal Loans, Home Loans, Loan Against Property

\#\#\# 1\.4 Relationship to Other Repository Documents

| Document | Relationship |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| DOC\-010 | Architecture foundation for industry configuration |

| DOC\-011 | Canonical data model referenced for all mappings |

| DOC\-014 | Finance & Operations Specifications for business logic |

| DOC\-017 | Core Module Specifications for implementation |

| DOC\-022 | Source\-to\-Canonical Mapping Guide for Excel sources |

| DOC\-023 | Rule Engine Translation Guide for formula logic |

\-\-\-

\#\# 2\. Organizational Structure

\#\#\# 2\.1 Company/Tenant Structure

FCPL operates as a single tenant \(\`CompanyID = 1\`\) within the ODOS platform, with internal operational hierarchy mapped as follows:

\#\#\#\# 2\.1\.1 Company Level \(MST\_Company\)

| Field | Value |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-|

| CompanyID | 1 \(System\-Generated\) |

| CompanyCode | FCPL |

| CompanyName | Fineoteric Consulting Pvt Ltd |

| PAN | \[To be populated\] |

| GSTIN | \[To be populated\] |

| CIN | \[To be populated\] |

| TAN | \[To be populated\] |

| RegisteredAddress | \[To be populated\] |

| ContactNumber | \[To be populated\] |

| Email | \[To be populated\] |

| IsActive | TRUE |

\#\#\#\# 2\.1\.2 Region Structure \(MST\_InternalRegion\)

| RegionID | RegionCode | RegionName | CompanyID | IsActive |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|

| 1 | WEST | West Region | 1 | TRUE |

| 2 | NORTH | North Region | 1 | TRUE |

| 3 | SOUTH | South Region | 1 | TRUE |

| 4 | EAST | East Region | 1 | TRUE |

\#\#\#\# 2\.1\.3 Branch Structure \(MST\_InternalBranch\)

| BranchID | BranchCode | BranchName | RegionID | City | IsActive |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|

| 1 | ANDHERI | Andheri Office | 1 | Mumbai | TRUE |

| 2 | PUNE | Pune Office | 1 | Pune | TRUE |

| 3 | DELHI | Delhi Office | 2 | Delhi | TRUE |

| 4 | MUMBAI | Mumbai Office | 1 | Mumbai | TRUE |

| 5 | DADAR | Dadar Office | 1 | Mumbai | TRUE |

| 6 | THANE | Thane Office | 1 | Thane | TRUE |

| 7 | HUBALI | Hubali Office | 1 | Hubballi | TRUE |

| 8 | CHENNAI | Chennai Office | 3 | Chennai | TRUE |

| 9 | HYDERABAD | Hyderabad Office | 3 | Hyderabad | TRUE |

| 10 | AHMEDABAD | Ahmedabad Office | 1 | Ahmedabad | TRUE |

| 11 | NOIDA | Noida Office | 2 | Noida | TRUE |

| 12 | BELAPUR | Belapur Office | 1 | Navi Mumbai | TRUE |

| 13 | UP | Uttar Pradesh Office | 2 | \[City\] | TRUE |

\#\#\#\# 2\.1\.4 Team Structure \(MST\_Team\)

| TeamID | TeamCode | TeamName | BranchID | IsActive |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|

| 1 | SALES\-ANDHERI | Sales \- Andheri | 1 | TRUE |

| 2 | SALES\-PUNE | Sales \- Pune | 2 | TRUE |

| 3 | SALES\-DELHI | Sales \- Delhi | 3 | TRUE |

| 4 | OPS\-MUMBAI | Operations \- Mumbai | 4 | TRUE |

| 5 | OPS\-ANDHERI | Operations \- Andheri | 1 | TRUE |

| 6 | SALES\-DADAR | Sales \- Dadar | 5 | TRUE |

| 7 | SALES\-THANE | Sales \- Thane | 6 | TRUE |

| 8 | SALES\-HUBALI | Sales \- Hubali | 7 | TRUE |

| 9 | SALES\-CHENNAI | Sales \- Chennai | 8 | TRUE |

\#\#\#\# 2\.1\.5 Employee Role Mapping

| Role | Description | Access Level |

|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| ADMIN | System Administrator | Full System Access |

| FINANCE | Finance & Accounts | Financial Data Access |

| OPS | Operations Team | Case & Document Management |

| SALES | Sales Team | Lead & Customer Management |

| MANAGER | Team/Branch Manager | Dashboard & Approvals |

| VIEWER | Read\-Only Viewer | Dashboard & Reports Only |

| CONNECTOR | External Connector | Limited Self\-Service Access |

\#\#\# 2\.2 Reporting Structure

\`\`\`

                    ┌─────────────────────┐

                    │      CEO / MD       │

                    └─────────────────────┘

                              │

                    ┌─────────────────────┐

                    │   CTO \(ChatGPT\)     │

                    │   \(Architecture\)    │

                    └─────────────────────┘

                              │

        ┌─────────────────────┼─────────────────────┐

        │                     │                     │

┌───────▼───────┐    ┌───────▼───────┐    ┌───────▼───────┐

│   Finance     │    │  Operations   │    │  Sales Head   │

│    Lead       │    │    Lead       │    │               │

└───────────────┘    └───────────────┘    └───────────────┘

        │                     │                     │

┌───────▼───────┐    ┌───────▼───────┐    ┌───────▼───────┐

│  Finance      │    │  Branch       │    │  Sales        │

│  Team         │    │  Managers     │    │  Managers     │

└───────────────┘    └───────────────┘    └───────────────┘

                              │

                    ┌─────────▼─────────┐

                    │   Team Leaders    │

                    │   Connectors      │

                    └───────────────────┘

\`\`\`

\-\-\-

\#\# 3\. Product Taxonomy

\#\#\# 3\.1 Product Classification

FCPL originates the following loan products, mapped to \`MST\_Product\`:

\#\#\#\# 3\.1\.1 Secured Products

| ProductCode | ProductName | Category | Type | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| HL | Home Loan | HL | Secured | Loan for purchase/construction of residential property |

| LAP | Loan Against Property | LAP | Secured | Loan secured against existing property |

| SBL\-TL | Secured Business Loan \- Term Loan | BL | Secured | Term loan against business assets |

| SBL\-OD | Secured Business Loan \- Overdraft | BL | Secured | Overdraft facility against business assets |

\#\#\#\# 3\.1\.2 Unsecured Products

| ProductCode | ProductName | Category | Type | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| BL\-TL | Business Loan \- Term Loan | BL | Unsecured | Unsecured term loan for businesses |

| BL\-OD | Business Loan \- Overdraft | BL | Unsecured | Unsecured overdraft for businesses |

| PL | Personal Loan | PL | Unsecured | Unsecured personal loan |

| PL\-OD | Personal Loan \- Overdraft | PL | Unsecured | Unsecured personal overdraft |

\#\#\# 3\.2 Product to Master Data Linkage

Each product maps to:

\- \`MST\_Product\`: Product master

\- \`MST\_LenderAgreement\`: Lender\-specific agreement

\- \`RUL\_CommissionRule\`: Commission calculation rules

\- \`META\_FieldDefinition\`: Product\-specific metadata

\#\#\# 3\.3 Product Attributes

| Product | Loan Type | Min Amount | Max Amount | Typical Tenure | Interest Rate Range |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| HL | Secured | ₹5,00,000 | ₹5,00,00,000 | 5\-30 Years | 6\.5% \- 9\.5% |

| LAP | Secured | ₹5,00,000 | ₹10,00,00,000 | 5\-20 Years | 8\.0% \- 14\.0% |

| SBL\-TL | Secured | ₹5,00,000 | ₹50,00,000 | 1\-7 Years | 10\.0% \- 18\.0% |

| SBL\-OD | Secured | ₹5,00,000 | ₹50,00,000 | 1\-7 Years | 10\.0% \- 18\.0% |

| BL\-TL | Unsecured | ₹1,00,000 | ₹30,00,000 | 1\-5 Years | 12\.0% \- 24\.0% |

| BL\-OD | Unsecured | ₹1,00,000 | ₹30,00,000 | 1\-5 Years | 12\.0% \- 24\.0% |

| PL | Unsecured | ₹50,000 | ₹15,00,000 | 1\-5 Years | 10\.0% \- 24\.0% |

| PL\-OD | Unsecured | ₹50,000 | ₹15,00,000 | 1\-5 Years | 10\.0% \- 24\.0% |

\-\-\-

\#\# 4\. Lender/Bank Master

\#\#\# 4\.1 Lender Classification

| LenderID | LenderCode | LenderName | IsNBFC | DSA Code | Category |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|

| 1 | FTCASH | FT Cash | FALSE | \[Code\] | Bank |

| 2 | PROTIUM | Protium | TRUE | \[Code\] | NBFC |

| 3 | TATA | Tata Capital | TRUE | \[Code\] | NBFC |

| 4 | INDIFI | Indifi | TRUE | \[Code\] | NBFC |

| 5 | PIRAMAL | Piramal Capital | TRUE | \[Code\] | NBFC |

| 6 | ABFL | Aditya Birla Finance | TRUE | \[Code\] | NBFC |

| 7 | FLEXI | Flexi Loan | TRUE | \[Code\] | NBFC |

| 8 | GODREJ | Godrej Capital | TRUE | \[Code\] | NBFC |

| 9 | L&T | L&T Finance | TRUE | \[Code\] | NBFC |

| 10 | AXIS | Axis Bank | FALSE | \[Code\] | Bank |

| 11 | HDFC | HDFC Bank | FALSE | \[Code\] | Bank |

| 12 | ICICI | ICICI Bank | FALSE | \[Code\] | Bank |

| 13 | SBI | State Bank of India | FALSE | \[Code\] | Bank |

| 14 | KOTAK | Kotak Mahindra Bank | FALSE | \[Code\] | Bank |

| 15 | YES | Yes Bank | FALSE | \[Code\] | Bank |

| 16 | IDFC | IDFC First Bank | FALSE | \[Code\] | Bank |

| 17 | TMB | Tamilnad Mercantile Bank | FALSE | \[Code\] | Bank |

| 18 | STANDARD | Standard Chartered | FALSE | \[Code\] | Bank |

| 19 | CITI | Citibank | FALSE | \[Code\] | Bank |

| 20 | HSBC | HSBC Bank | FALSE | \[Code\] | Bank |

| 21 | RBL | RBL Bank | FALSE | \[Code\] | Bank |

| 22 | DCB | DCB Bank | FALSE | \[Code\] | Bank |

| 23 | EQUITAS | Equitas Small Finance Bank | FALSE | \[Code\] | Bank |

| 24 | AU | AU Small Finance Bank | FALSE | \[Code\] | Bank |

| 25 | JANA | Jana Small Finance Bank | FALSE | \[Code\] | Bank |

\#\#\# 4\.2 Lender Agreement Configuration

Each lender agreement \(\`MST\_LenderAgreement\`\) shall specify:

\- Commission rates by product

\- Payment terms \(invoice generation, due date, credit period\)

\- TDS applicability

\- GST applicability

\#\#\# 4\.3 Lender Branch Mapping

Lender branches \(\`MST\_LenderBranch\`\) shall be configured for each lender with active business relationships\.

\-\-\-

\#\# 5\. Connector Master

\#\#\# 5\.1 Connector Structure

Connectors \(MST\_Connector\) represent the channel partner network:

| Field | Description | Source |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| ConnectorID | System\-generated identifier | System |

| ConnectorCode | Business key from FCPL | 'Connector Directory' |

| ConnectorName | Full name of connector | 'Connector Directory' |

| PAN | Tax identifier | 'Connector Directory' |

| BankAccountID | Link to bank account details | MST\_PartyBankAccount |

| HierarchyLevel | 1, 2, 3 \(Sub\-DSA levels\) | MST\_ConnectorHierarchy |

| IsActive | Status flag | System |

\#\#\# 5\.2 Connector Hierarchy \(MST\_ConnectorHierarchy\)

\`\`\`

┌─────────────────────────────────────────────────────────────────┐

│                     CONNECTOR HIERARCHY                        │

├─────────────────────────────────────────────────────────────────┤

│                                                                 │

│   Level 1: Master Connector \(DSA\)                              │

│   ├── FCPL \(Primary DSA\)                                       │

│   └── BW \(Secondary DSA\)                                       │

│                                                                 │

│   Level 2: Regional Connectors                                 │

│   ├── Connectors with city/region assignment                   │

│   └── Managed by Unit Heads                                   │

│                                                                 │

│   Level 3: Field Connectors                                    │

│   ├── Individual agents                                        │

│   ├── Referral partners                                        │

│   └── Managed by Regional Connectors                           │

│                                                                 │

└─────────────────────────────────────────────────────────────────┘

\`\`\`

\#\#\# 5\.3 Connector Bank Account Details \(MST\_PartyBankAccount\)

| Field | Description | Source |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| BankAccountID | System\-generated identifier | System |

| ConnectorID | Link to MST\_Connector | System |

| BankName | Bank name | 'Bank Account Master' |

| AccountNumber | Account number | 'Bank Account Master' |

| IFSC | IFSC code | 'Bank Account Master' |

| GSTIN | GST identification \(if applicable\) | 'Bank Account Master' |

\#\#\# 5\.4 Connector Data Quality Notes

\- \*\*Missing Connector Codes\*\*: ~12% of rows have "NA" in connector code\. These shall be handled via fuzzy matching on connector name\.

\- \*\*Duplicate Connectors\*\*: Same entity may appear under different names\. Fuzzy matching recommendations shall be applied\.

\- \*\*Inactive Connectors\*\*: Connectors with no activity in the last 90 days shall be flagged for review\.

\-\-\-

\#\# 6\. Reference Data

\#\#\# 6\.1 Party Types \(REF\_PartyType\)

| PartyTypeID | PartyTypeCode | PartyTypeName | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| 1 | CUSTOMER | Customer | Loan applicant/borrower |

| 2 | CONNECTOR | Connector | Channel partner/agent |

| 3 | EMPLOYEE | Employee | Internal employee |

| 4 | VENDOR | Vendor | Supplier/vendor |

| 5 | LENDER | Lender | Financial institution |

| 6 | COMPANY | Company | FCPL entity itself |

| 7 | CO\_BORROWER | Co\-Borrower | Joint applicant |

\#\#\# 6\.2 Status Values \(REF\_Status\)

\#\#\#\# 6\.2\.1 Case Status \(from FCPL Secured Tracker\)

| StatusCode | StatusName | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| DISBURSED | Disbursed | Fully disbursed |

| PART\_DISBURSED | Partially Disbursed | Partially disbursed |

| CANCELLED | Cancelled | Cancelled by lender/borrower |

| DUPLICATE | Duplicate | Duplicate entry |

| PENDING | Pending | Awaiting processing |

| APPROVED | Approved | Approved by lender |

| REJECTED | Rejected | Rejected by lender |

| HOLD | Hold | On hold |

| LOGIN\_DONE | Login Done \- In Process | Application logged, under process |

| IN\_PROCESS | In Process | Processing ongoing |

\#\#\#\# 6\.2\.2 Bill/Invoice Status

| StatusCode | StatusName | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| RECEIVED | Received | Payment received |

| PENDING | Pending | Awaiting payment |

| RAISED | Raised | Invoice raised |

| DUPLICATE | Duplicate | Duplicate invoice |

| CANCELLED | Cancelled | Invoice cancelled |

\#\#\#\# 6\.2\.3 Payment Status \(REF\_PaymentStatus\)

| StatusCode | StatusName | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| PENDING | Pending | Payment initiated but not processed |

| PROCESSING | Processing | Payment in processing |

| COMPLETED | Completed | Payment completed |

| RECONCILED | Reconciled | Matched with bank statement |

| FAILED | Failed | Payment failed |

| REJECTED | Rejected | Payment rejected |

\#\#\# 6\.3 Priority Levels \(REF\_Priority\)

| PriorityCode | PriorityName | Description | SLA Hours |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|

| CRITICAL | Critical | Urgent / Immediate | 4 |

| HIGH | High | High priority | 8 |

| MEDIUM | Medium | Normal priority | 24 |

| LOW | Low | Low priority | 72 |

\#\#\# 6\.4 Document Types \(REF\_DocumentType\)

| DocumentTypeCode | DocumentTypeName | IsKYC | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| PAN | PAN Card | TRUE | Permanent Account Number |

| AADHAAR | Aadhaar Card | TRUE | Aadhaar identification |

| ITR | Income Tax Return | TRUE | Income Tax Return |

| BANK\_STATEMENT | Bank Statement | TRUE | Last 6 months bank statement |

| SALARY\_SLIP | Salary Slip | TRUE | Salary slip |

| SANCTION\_LETTER | Sanction Letter | FALSE | Lender sanction letter |

| AGREEMENT | Agreement | FALSE | Loan agreement |

| INVOICE | Invoice | FALSE | Commission invoice |

| GST\_CERT | GST Certificate | TRUE | GST Registration |

| ADDRESS\_PROOF | Address Proof | TRUE | Address proof |

| PHOTO | Photograph | TRUE | Passport size photograph |

| PROPERTY\_DOCS | Property Documents | FALSE | Property related documents |

\#\#\# 6\.5 Reference Data Domains \(REF\_ tables\)

| Table | Domain | Values |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| REF\_Country | Country | India, etc\. |

| REF\_State | State | Maharashtra, Gujarat, Delhi, Karnataka, Tamil Nadu, Uttar Pradesh, Telangana, etc\. |

| REF\_District | District | As per FCPL operating locations |

| REF\_City | City | Mumbai, Pune, Delhi, Chennai, Hyderabad, Ahmedabad, Noida, Thane, Hubballi, etc\. |

| REF\_Gender | Gender | Male, Female, Transgender |

| REF\_MaritalStatus | Marital Status | Married, Unmarried, Single, Divorced |

| REF\_Occupation | Occupation | Salaried, Self\-Employed, Professional, Business |

| REF\_Industry | Industry | Banking, Finance, IT, Manufacturing, etc\. |

| REF\_LoanPurpose | Loan Purpose | Business Expansion, Working Capital, Home Purchase, Personal Needs, etc\. |

| REF\_PropertyType | Property Type | Residential, Commercial, Industrial, Agricultural |

\-\-\-

\#\# 7\. Profile Types

\#\#\# 7\.1 Customer/Applicant Profiles

FCPL classifies applicants by profile type:

| ProfileCode | ProfileName | Description | Risk Category |

|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| SENP | Senior Professional | Senior professional \(Doctor, CA, Lawyer, etc\.\) | Low Risk |

| SALARIED | Salaried | Regular salaried employee | Medium Risk |

| N/A | Not Applicable | Profile not classified | — |

\#\#\# 7\.2 Profile\-to\-Product Mapping

| Profile | Recommended Products | Eligibility Criteria |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| SENP | HL, LAP, BL\-TL | Professional degree, 5\+ years experience |

| SALARIED | HL, PL | Regular income, 3\+ months employment |

| N/A | PL, BL\-TL, BL\-OD | Varies by product |

\#\#\# 7\.3 Profile Attributes Mapping

| Attribute | Source Field | Target Field | Transformation |

|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Profile Type | PROFILE \(Excel\) | MST\_Customer\.Profile | Direct mapping |

| Senior Professional | SENP | MST\_Customer\.ProfileCode | Map to SENP |

| Salaried | SALARIED | MST\_Customer\.ProfileCode | Map to SALARIED |

| Not Applicable | N/A | MST\_Customer\.ProfileCode | Map to N/A |

\-\-\-

\#\# 8\. Configuration Cross\-Reference

\#\#\# 8\.1 Configuration Tables Summary

| Configuration Table | Purpose | Key Values |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|

| CFG\_CompanySettings | Tenant configuration | FCPL\-specific settings |

| CFG\_FinancialYear | Financial year definitions | FY 2026\-27 \(April\-March\) |

| CFG\_AutoNumbering | Auto\-numbering rules | Case IDs, Invoice Numbers |

| CFG\_Calendar | Holiday calendar | Public holidays by region |

| CFG\_Feature | Feature toggles | FCPL\-specific features |

| CFG\_CompanyFeature | Company\-specific features | FCPL feature enables |

| CFG\_EmailSMSConfig | Communication templates | FCPL\-branded templates |

\#\#\# 8\.2 Seed Data Requirements

| Category | Data Source | Priority |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|

| Organizational Structure | FCPL HR/Admin | High |

| Product Taxonomy | FCPL Product Team | High |

| Lender Master | FCPL Partnerships | High |

| Connector Master | FCPL Connector Directory | High |

| Reference Data | FCPL Operations | Medium |

| Profile Types | FCPL Sales | Low |

\#\#\# 8\.3 Configuration Precedence

\`\`\`

┌─────────────────────────────────────────────────────────────────┐

│                 CONFIGURATION PRECEDENCE                       │

├─────────────────────────────────────────────────────────────────┤

│                                                                 │

│  1\. CFG\_CompanySettings \(Tenant\-level\)                         │

│  2\. CFG\_CompanyFeature \(Feature toggles\)                       │

│  3\. CFG\_AutoNumbering \(Numbering rules\)                        │

│  4\. CFG\_Calendar \(Holiday/Working days\)                        │

│  5\. CFG\_FinancialYear \(Financial period\)                       │

│  6\. CFG\_EmailSMSConfig \(Communication\)                         │

│                                                                 │

└─────────────────────────────────────────────────────────────────┘

\`\`\`

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

\*\*This document is designated as an Industry Configuration Baseline Artefact\.\*\*

\*\*Following approval:\*\*

\- Structural changes to industry configuration require a new Architecture Decision Record \(ADR\)\.

\- Changes to product taxonomy require Architecture Review Board \(ARB\) approval\.

\- All FCPL implementation shall use this document as the governing configuration baseline\.

\*\*Freeze Status:\*\* ✅ \*\*FROZEN\*\*

\#\#\# 9\.3 Approval Sign\-Off

| Role | Name | Signature | Date |

|\-\-\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-|

| Enterprise Architect | Architecture Review Board | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

| Business Lead | \[Name\] | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

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

| DOC\-010 | Architecture & ADRs referencing industry configuration |

| DOC\-011 | Data Model referencing configuration tables |

| DOC\-014 | Finance & Operations referencing business rules |

| DOC\-022 | Source\-to\-Canonical Mapping Guide referencing this configuration |

| DOC\-023 | Rule Engine Translation Guide referencing this configuration |

\-\-\-

\#\# End of Document

\*\*Document ID:\*\* DOC\-021  

\*\*Document Name:\*\* \*FCPL Industry Configuration Specification\*  

\*\*Version:\*\* 1\.0  

\*\*Status:\*\* Approved / Frozen  

\*\*Owner:\*\* CTO

