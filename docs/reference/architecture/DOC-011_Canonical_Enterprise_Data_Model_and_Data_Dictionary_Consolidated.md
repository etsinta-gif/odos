# DOC-011 Canonical Enterprise Data Model & Data Dictionary Consolidated

\# DOC\-011 – Canonical Enterprise Data Model & Data Dictionary Consolidated

\*\*Document ID:\*\* DOC\-011  

\*\*Version:\*\* 1\.0  

\*\*Status:\*\* Approved / Frozen  

\*\*Owner:\*\* CTO \(ChatGPT\)  

\*\*Classification:\*\* Enterprise Data Foundation  

\*\*Purpose:\*\* Define the complete enterprise data model, including the Canonical Enterprise Data Model \(CEDM\), Enterprise ERD, Data Dictionary \(Volumes 1 & 2\), Business Glossary, Database Standards, and Reference Data Catalogue\.

\-\-\-

\#\# Table of Contents

1\. Executive Summary

2\. Canonical Enterprise Data Model \(CEDM\) Specification

3\. Enterprise ERD

4\. Data Dictionary – Volume 1: Enterprise Standards & Conventions

5\. Data Dictionary – Volume 2: Table\-by\-Table Definitions

6\. Business Glossary

7\. Database Standards Manual

8\. Reference Data Catalogue

9\. Data Model Gap Analysis & Resolution Register

10\. Document Status & Approval

\-\-\-

\#\# 1\. Executive Summary

\#\#\# 1\.1 Purpose of This Document

This document consolidates the complete enterprise data foundation for the ODOS Enterprise Platform\. It brings together:

\- \*\*Canonical Enterprise Data Model \(CEDM\)\*\* – The authoritative enterprise semantic model

\- \*\*Enterprise ERD\*\* – The complete entity\-relationship diagram

\- \*\*Data Dictionary \(Volumes 1 & 2\)\*\* – Comprehensive definitions of every table and field

\- \*\*Business Glossary\*\* – Authoritative business vocabulary

\- \*\*Database Standards Manual\*\* – Implementation standards for database design

\- \*\*Reference Data Catalogue\*\* – Complete inventory of reference data

\#\#\# 1\.2 The Data Model Philosophy

ODOS follows a \*\*Canonical\-First\*\* data philosophy:

| Principle | Description |

|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \*\*Canonical First\*\* | All data models derive from the canonical enterprise model |

| \*\*Business Semantics First\*\* | Business meaning drives data structure |

| \*\*Metadata Driven\*\* | Data definitions are metadata\-governed |

| \*\*Single Source of Truth\*\* | One authoritative definition per data element |

| \*\*Extensible\*\* | New entities can be added without redesign |

| \*\*Industry\-Agnostic\*\* | Core model supports multiple industries |

\#\#\# 1\.3 Scope

This document covers:

| Area | Coverage |

|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|

| Canonical Enterprise Data Model | Complete semantic model |

| Enterprise ERD | All entities, attributes, relationships |

| Data Dictionary \- Volume 1 | Enterprise standards and conventions |

| Data Dictionary \- Volume 2 | Table\-by\-table definitions |

| Business Glossary | All business terminology |

| Database Standards | Naming, data types, relationships |

| Reference Data Catalogue | All reference data domains |

\#\#\# 1\.4 Relationship to Other Repository Documents

| Document | Relationship |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| DOC\-010 | Architecture & ADRs referencing this document |

| DOC\-012 | Platform Engineering Standards referencing database standards |

| DOC\-013 | Application Development Standards referencing data model |

| DOC\-014 | Finance & Operations Specifications referencing transaction tables |

| DOC\-015 | AI & Data Engineering referencing ETL tables |

| DOC\-016 | Security & Governance referencing security tables |

| DOC\-017 | Core Module Specifications referencing data model |

| DOC\-018 | Business Module Specifications referencing data model |

\#\#\# 1\.5 Document Status

| Status | Approved / Frozen |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \*\*Version\*\* | 1\.0 |

| \*\*Date\*\* | July 2026 |

| \*\*Next Review\*\* | Annual or before major architectural change |

| \*\*Owner\*\* | CTO |

\-\-\-

\#\# 2\. Canonical Enterprise Data Model \(CEDM\) Specification

\#\#\# 2\.1 Purpose

The Canonical Enterprise Data Model \(CEDM\) is the authoritative enterprise semantic model that defines the single, consistent, technology\-independent representation of all business entities, relationships, events, and rules across the ODOS platform\.

\#\#\# 2\.2 Why a Canonical Enterprise Data Model is Required

\- \*\*Enterprise Semantic Consistency:\*\* Without a canonical model, each application, API, and integration defines its own data semantics, leading to inconsistency, duplication, and integration complexity\.

\- \*\*Single Business Language:\*\* The CEDM establishes a common enterprise vocabulary that aligns business concepts with technical implementations\.

\- \*\*Decoupling Applications:\*\* The CEDM decouples applications from physical database schemas, enabling independent evolution\.

\- \*\*Integration Simplification:\*\* All integrations use the canonical model, eliminating point\-to\-point transformations\.

\- \*\*API Consistency:\*\* All APIs expose canonical objects, ensuring consistent contracts across the platform\.

\- \*\*AI Semantic Grounding:\*\* AI models use the canonical model for semantic understanding, RAG, and grounding\.

\#\#\# 2\.3 Distinction: Conceptual, Canonical, Logical, and Physical Models

| Layer | Description | Audience | Example |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|

| \*\*Conceptual Model\*\* | Business concepts and relationships | Business Users, Product Owners | "Customer", "Loan", "Commission" |

| \*\*Canonical Model\*\* | Enterprise semantic entities and attributes | Architects, Data Stewards | \`Customer\` entity with \`FullName\`, \`PAN\` |

| \*\*Logical Model\*\* | Application\-specific logical models | Application Architects | Service\-specific models |

| \*\*Physical Model\*\* | Physical database schemas, API DTOs, event payloads | Developers, DBAs | \`MST\_Customer\` table, \`CustomerDTO\` API object |

\#\#\# 2\.4 Canonical Modeling Principles

| Principle | Description |

|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \*\*Domain\-Driven\*\* | Model is driven by business domains |

| \*\*Bounded Contexts\*\* | Each domain has a clear bounded context |

| \*\*Aggregates\*\* | Use aggregates to group entities |

| \*\*Value Objects\*\* | Use value objects for immutable concepts |

| \*\*Entities\*\* | Use entities for objects with identity |

| \*\*Domain Events\*\* | Capture meaningful business events |

| \*\*Ubiquitous Language\*\* | Use the same language as business users |

| \*\*Separation of Concerns\*\* | Separate canonical from physical |

| \*\*Enterprise Reuse\*\* | Maximise reuse across domains |

| \*\*Semantic Consistency\*\* | Maintain consistent semantics |

| \*\*Extensibility\*\* | Support future extensions |

| \*\*Versioning\*\* | Version the model |

\#\#\# 2\.5 Enterprise Business Domains

| Domain | Description | Subdomains | Owner |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-|

| \*\*Customer\*\* | Customer management | Customer, KYC, Address, Contact | Sales/Operations |

| \*\*Organisation\*\* | Organisation structure | Company, Region, Branch, Team | Operations |

| \*\*Employee\*\* | Employee management | Employee, Role, Skill, Compensation | HR |

| \*\*Identity\*\* | Identity and access | User, Role, Permission, Session | Security |

| \*\*Partner\*\* | Partner management | Connector, Vendor, Referral | Partnerships |

| \*\*Lead\*\* | Lead management | Lead, Campaign, Marketing | Sales |

| \*\*Case\*\* | Loan lifecycle | Application, Sanction, Disbursement | Operations |

| \*\*Product\*\* | Product management | Product, Scheme, Pricing | Product |

| \*\*Lender\*\* | Lender management | Lender, Branch, RM | Partnerships |

| \*\*Commission\*\* | Commission management | Commission, Payout, Incentive | Finance |

| \*\*Payment\*\* | Payment management | Payment, Receipt, Reconciliation | Finance |

| \*\*Accounting\*\* | Accounting | Ledger, Account, Journal | Finance |

| \*\*Finance\*\* | Financial management | Revenue, Expense, Budget | Finance |

| \*\*Compliance\*\* | Compliance | KYC, AML, Regulatory | Compliance |

| \*\*Risk\*\* | Risk management | Risk, Scoring, Fraud | Risk |

| \*\*Workflow\*\* | Workflow management | Workflow, State, Transition | Operations |

| \*\*Document\*\* | Document management | Document, Attachment, OCR | Operations |

| \*\*Notification\*\* | Notification management | Notification, Alert, Message | Operations |

| \*\*Audit\*\* | Audit management | Audit, Log, Trail | Security |

| \*\*Reporting\*\* | Reporting | Report, Dashboard, KPI | BI |

| \*\*Analytics\*\* | Analytics | Analytics, Data Mart, Snapshot | BI |

| \*\*AI\*\* | AI management | AI Model, Prompt, Embedding | AI |

| \*\*Metadata\*\* | Metadata management | Metadata, Schema, Mapping | Data Governance |

| \*\*Configuration\*\* | Configuration management | Config, Feature, Setting | Admin |

| \*\*Reference Data\*\* | Reference data | State, District, Status | Data Governance |

\#\#\# 2\.6 Canonical Entity Framework

\#\#\#\# 2\.6\.1 Canonical Entity Template

| Field | Description |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \*\*Entity ID\*\* | Unique identifier \(e\.g\., \`ENT\-CUST\-001\`\) |

| \*\*Entity Name\*\* | Business name \(e\.g\., \`Customer\`\) |

| \*\*Definition\*\* | Business definition |

| \*\*Domain\*\* | Domain \(e\.g\., \`Customer Domain\`\) |

| \*\*Attributes\*\* | List of canonical attributes |

| \*\*Relationships\*\* | Relationships to other entities |

| \*\*Ownership\*\* | Data owner and steward |

| \*\*Lifecycle\*\* | Lifecycle stages |

| \*\*Identifiers\*\* | Natural and business keys |

| \*\*Version\*\* | Version number |

| \*\*Status\*\* | Active, Draft, Deprecated |

| \*\*Business Rules\*\* | Associated business rules |

| \*\*Reference Data\*\* | Reference data links |

| \*\*Validation Rules\*\* | Validation rules |

| \*\*Security Classification\*\* | Security classification |

| \*\*Retention\*\* | Retention policy |

| \*\*Audit\*\* | Audit requirements |

\#\#\#\# 2\.6\.2 Common Enterprise Base Attributes

All canonical entities inherit the following base attributes:

| Attribute | Type | Description |

|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \`CreatedDate\` | DateTime | Creation timestamp |

| \`CreatedBy\` | String | User/system who created |

| \`ModifiedDate\` | DateTime | Last modification timestamp |

| \`ModifiedBy\` | String | User/system who modified |

| \`TenantID\` | String | Tenant identifier \(multi\-tenant\) |

| \`Version\` | Integer | Optimistic locking version |

| \`Status\` | String | Active, Inactive, Pending, Archived |

| \`EffectiveDate\` | DateTime | Effective from date |

| \`ExpiryDate\` | DateTime | Expiry date |

| \`IsDeleted\` | Boolean | Soft delete flag |

| \`CorrelationID\` | String | Correlation identifier |

\#\#\# 2\.7 Core Canonical Entities

\#\#\#\# 2\.7\.1 Party \(Root Entity\)

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Entity ID\*\* | ENT\-PARTY\-001 |

| \*\*Entity Name\*\* | Party |

| \*\*Definition\*\* | A person or organisation that interacts with the platform |

| \*\*Domain\*\* | Master Data Domain |

| \*\*Attributes\*\* | PartyID, FullName, PAN, GSTIN, KYCStatus |

| \*\*Relationships\*\* | Extended by Customer, Employee, Connector, Vendor, Lender |

\#\#\#\# 2\.7\.2 Customer

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Entity ID\*\* | ENT\-CUST\-001 |

| \*\*Entity Name\*\* | Customer |

| \*\*Definition\*\* | A person or organisation that applies for a loan |

| \*\*Domain\*\* | Customer Domain |

| \*\*Attributes\*\* | CustomerID, FullName, PAN, GSTIN, Mobile, Email, DateOfBirth, Gender, MaritalStatus, Occupation, Industry, Addresses, BankAccounts, Documents, KYCStatus |

| \*\*Relationships\*\* | Has many Cases, has many Documents, has many Addresses, has one KYCStatus |

\#\#\#\# 2\.7\.3 Case

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Entity ID\*\* | ENT\-CASE\-001 |

| \*\*Entity Name\*\* | Case |

| \*\*Definition\*\* | A loan application or transaction |

| \*\*Domain\*\* | Case Domain |

| \*\*Attributes\*\* | CaseID, CaseNumber, CustomerID, LenderID, ProductID, SanctionAmount, DisbursementAmount, ApplicationDate, SanctionDate, DisbursementDate, InvoiceGeneratedDate, InvoiceDueDate, PaymentReceivedDate, CaseStatus |

| \*\*Relationships\*\* | Belongs to Customer, belongs to Lender, belongs to Product |

\#\#\#\# 2\.7\.4 Lender

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Entity ID\*\* | ENT\-LEND\-001 |

| \*\*Entity Name\*\* | Lender |

| \*\*Definition\*\* | A financial institution providing loans |

| \*\*Domain\*\* | Lender Domain |

| \*\*Attributes\*\* | LenderID, LenderName, PAN, GSTIN, CreditRatingCode, RiskWeight |

| \*\*Relationships\*\* | Has many Products, has many Agreements, has many Cases |

\#\#\#\# 2\.7\.5 Product

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Entity ID\*\* | ENT\-PROD\-001 |

| \*\*Entity Name\*\* | Product |

| \*\*Definition\*\* | A loan product offered by a lender |

| \*\*Domain\*\* | Product Domain |

| \*\*Attributes\*\* | ProductID, ProductName, ProductCode, LenderID, InterestRate, ProcessingFee, MinLoanAmount, MaxLoanAmount |

| \*\*Relationships\*\* | Belongs to Lender, has many Cases |

\#\#\#\# 2\.7\.6 Revenue

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Entity ID\*\* | ENT\-REV\-001 |

| \*\*Entity Name\*\* | Revenue |

| \*\*Definition\*\* | Commission income from lenders |

| \*\*Domain\*\* | Finance Domain |

| \*\*Attributes\*\* | RevenueID, CaseID, RevenueDate, GrossRevenueAmount, GST\_Amount, TDS\_Amount, NetAmount, UTR\_Number, PaymentStatus |

| \*\*Relationships\*\* | Belongs to Case |

\#\#\#\# 2\.7\.7 Commission

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Entity ID\*\* | ENT\-COMM\-001 |

| \*\*Entity Name\*\* | Commission |

| \*\*Definition\*\* | Payout to connectors or employees |

| \*\*Domain\*\* | Commission Domain |

| \*\*Attributes\*\* | CommissionID, CaseID, ConnectorID, CommissionDate, BaseCommissionAmount, BonusCommissionAmount, GrossCommissionAmount, GST\_Amount, TDS\_Amount, NetAmount, PaymentStatus |

| \*\*Relationships\*\* | Belongs to Case, belongs to Connector |

\#\#\# 2\.8 Canonical Value Objects

| Value Object | Description | Attributes |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|

| \`Address\` | Physical address | Line1, Line2, City, State, PostalCode, Country |

| \`Money\` | Monetary value | Amount, Currency |

| \`Amount\` | Numeric amount | Value, Precision, Scale |

| \`Percentage\` | Percentage value | Value \(0\-100\) |

| \`PhoneNumber\` | Telephone number | CountryCode, Number, Extension |

| \`Email\` | Email address | Address |

| \`TaxIdentifier\` | Tax identifier | Value, Type \(PAN, GSTIN, etc\.\) |

| \`GeoLocation\` | Geographic location | Latitude, Longitude |

| \`Period\` | Time period | StartDate, EndDate |

| \`IdentityDocument\` | Identity document | Type, Number, IssuedDate, ExpiryDate |

\-\-\-

\#\# 3\. Enterprise ERD

\#\#\# 3\.1 Purpose

This section defines the complete Enterprise Entity\-Relationship Diagram \(ERD\) for the ODOS platform, organised by the ten\-layer architecture\.

\#\#\# 3\.2 ERD Layers

| Layer | Prefix | Purpose | Tables |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| Metadata | \`META\_\` | Defines the system itself | 6 |

| Configuration | \`CFG\_\` | Configurable settings | 7 |

| Security | \`SEC\_\` | Users, roles, permissions, audit | 5 |

| Reference | \`REF\_\` | Static reference data | 23 |

| Masters | \`MST\_\` | Master records | 26 |

| Rules | \`RUL\_\` | Business rules | 9 |

| Transactions | \`TRN\_\` | Operational transactions | 28 |

| ETL & Staging | \`ETL\_\` | Data ingestion | 6 |

| Audit & Documents | \`AUD\_\` | Documents and audit | 2 |

| Business Intelligence | \`BI\_\` | Analytical snapshots | 12 |

| Artificial Intelligence | \`AI\_\` | AI learning and mapping | 4 |

| \*\*Total\*\* | | | \*\*128\*\* |

\#\#\# 3\.3 Metadata Layer \(\`META\_\`\)

| Table | Purpose |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|

| \`META\_TableDefinition\` | Master catalog of all tables |

| \`META\_FieldDefinition\` | Master catalog of all fields |

| \`META\_FieldMapping\` | Source\-to\-target field mappings |

| \`META\_ImportTemplate\` | Import template configurations |

| \`META\_ReportDefinition\` | Report definitions |

| \`META\_DashboardDefinition\` | Dashboard definitions |

\#\#\# 3\.4 Configuration Layer \(\`CFG\_\`\)

| Table | Purpose |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|

| \`CFG\_CompanySettings\` | Tenant\-specific configuration |

| \`CFG\_FinancialYear\` | Financial year definitions |

| \`CFG\_AutoNumbering\` | Auto\-numbering rules |

| \`CFG\_Calendar\` | Holiday and working day calendar |

| \`CFG\_Feature\` | Master feature list |

| \`CFG\_CompanyFeature\` | Tenant feature toggles |

| \`CFG\_EmailSMSConfig\` | Email/SMS configuration |

\#\#\# 3\.5 Security Layer \(\`SEC\_\`\)

| Table | Purpose |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|

| \`SEC\_Role\` | User roles |

| \`SEC\_Permission\` | Granular permissions |

| \`SEC\_User\` | User accounts |

| \`SEC\_LoginHistory\` | Login audit trail |

| \`SEC\_AuditTrail\` | System\-wide audit trail |

\#\#\# 3\.6 Reference Layer \(\`REF\_\`\)

| Table | Purpose |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|

| \`REF\_PartyType\` | Party types \(Customer, Employee, etc\.\) |

| \`REF\_Country\` | Country codes |

| \`REF\_State\` | State/Province codes |

| \`REF\_District\` | District codes |

| \`REF\_City\` | City codes |

| \`REF\_Pincode\` | Postal codes |

| \`REF\_Gender\` | Gender values |

| \`REF\_MaritalStatus\` | Marital status values |

| \`REF\_Occupation\` | Occupation types |

| \`REF\_Industry\` | Industry sectors |

| \`REF\_LoanPurpose\` | Loan purpose types |

| \`REF\_PropertyType\` | Property types |

| \`REF\_DocumentType\` | Document types |

| \`REF\_AddressType\` | Address types |

| \`REF\_ExpenseCategory\` | Expense categories |

| \`REF\_ExpenseType\` | Expense types |

| \`REF\_PaymentStatus\` | Payment status values |

| \`REF\_Priority\` | Priority levels |

| \`REF\_Status\` | General status values |

| \`REF\_TDSSection\` | TDS sections |

| \`REF\_GSTCategory\` | GST categories |

| \`REF\_Frequency\` | Frequency values |

| \`REF\_ClaimStatus\` | Claim status values |

\#\#\# 3\.7 Master Layer \(\`MST\_\`\)

| Table | Purpose |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|

| \`MST\_Company\` | Tenant root record |

| \`MST\_InternalRegion\` | Geographic region |

| \`MST\_InternalBranch\` | Branch/office |

| \`MST\_Team\` | Team |

| \`MST\_Employee\` | Employee master |

| \`MST\_EmployeeBankAccount\` | Employee bank details |

| \`MST\_Party\` | Universal party master |

| \`MST\_PartyAddress\` | Party addresses |

| \`MST\_PartyContact\` | Party contacts |

| \`MST\_PartyBankAccount\` | Party bank accounts |

| \`MST\_Customer\` | Customer master |

| \`MST\_Lender\` | Lender master |

| \`MST\_LenderBranch\` | Lender branch |

| \`MST\_LenderRM\` | Lender relationship manager |

| \`MST\_LenderAgreement\` | Lender agreement |

| \`MST\_Product\` | Product master |

| \`MST\_LenderCampaign\` | Lender campaign |

| \`MST\_Connector\` | Connector master |

| \`MST\_ConnectorBank\` | Connector bank details |

| \`MST\_ConnectorHierarchy\` | Connector hierarchy |

| \`MST\_Vendor\` | Vendor master |

| \`MST\_CostCenter\` | Cost centre |

| \`MST\_ExpenseCategory\` | Expense category |

| \`MST\_CompanyBankAccount\` | Company bank accounts |

| \`MST\_ChartOfAccounts\` | Chart of accounts |

| \`MST\_TallyMapping\` | Tally mapping |

\#\#\# 3\.8 Rules Layer \(\`RUL\_\`\)

| Table | Purpose |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|

| \`RUL\_GSTRule\` | GST calculation rules |

| \`RUL\_TDSRule\` | TDS calculation rules |

| \`RUL\_CommissionRule\` | Commission calculation rules |

| \`RUL\_CommissionSlab\` | Commission slabs |

| \`RUL\_Workflow\` | Workflow definitions |

| \`RUL\_BusinessRule\` | Generic business rules |

| \`RUL\_InternalIncentiveScheme\` | Employee incentive schemes |

| \`RUL\_ValidationRule\` | Data validation rules |

| \`RUL\_CostAllocationRule\` | Cost allocation rules |

\#\#\# 3\.9 Transaction Layer \(\`TRN\_\`\)

| Table | Purpose |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|

| \`TRN\_Lead\` | Lead records |

| \`TRN\_LeadSource\` | Lead source attribution |

| \`TRN\_Case\` | Loan case records |

| \`TRN\_CaseStatusHistory\` | Case status history |

| \`TRN\_Disbursement\` | Disbursement tranches |

| \`TRN\_CaseConnectorSplit\` | Connector split configuration |

| \`TRN\_CaseEmployeeSplit\` | Employee split configuration |

| \`TRN\_Revenue\` | Revenue records |

| \`TRN\_CampaignIncentive\` | Campaign incentive records |

| \`TRN\_Commission\` | Commission records |

| \`TRN\_IncentiveEarned\` | Employee incentive records |

| \`TRN\_Expense\` | Expense records |

| \`TRN\_RecurringExpense\` | Recurring expense schedules |

| \`TRN\_ExpenseClaim\` | Employee expense claims |

| \`TRN\_CaseCost\` | Case\-level costs |

| \`TRN\_Invoice\` | Invoice records |

| \`TRN\_Payment\` | Payment records |

| \`TRN\_TaxLiability\` | Tax liability records |

| \`TRN\_StatutoryPayment\` | Statutory payment records |

| \`TRN\_Notification\` | Notification records |

| \`TRN\_BankStatementLine\` | Bank statement lines |

| \`TRN\_UTRLock\` | UTR concurrency lock |

| \`TRN\_PANLock\` | PAN concurrency lock |

| \`TRN\_TallyExportBatch\` | Tally export batch |

| \`TRN\_TallyExportDetail\` | Tally export detail |

| \`TRN\_TaxLiability\_Invoice\_Link\` | Tax liability to invoice link |

| \`TRN\_MasterReclassification\` | Master reclassification |

| \`TRN\_BudgetAllocation\` | Budget allocation |

\#\#\# 3\.10 ETL Layer \(\`ETL\_\`\)

| Table | Purpose |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|

| \`ETL\_ImportBatch\` | Import batch tracking |

| \`ETL\_StagingRawData\` | Raw staging data |

| \`ETL\_ErrorLog\` | Error logging |

| \`ETL\_DataLineage\` | Data lineage tracking |

| \`ETL\_DuplicateQueue\` | Duplicate resolution queue |

| \`ETL\_DataQualityScore\` | Data quality scoring |

\#\#\# 3\.11 Audit & Documents Layer \(\`AUD\_\`\)

| Table | Purpose |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|

| \`AUD\_Document\` | Document metadata |

| \`AUD\_FileRepository\` | File repository |

\#\#\# 3\.12 Business Intelligence Layer \(\`BI\_\`\)

| Table | Purpose |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|

| \`BI\_CaseProfitability\_Detailed\` | Case\-level profitability |

| \`BI\_PortfolioRiskSnapshot\` | Portfolio risk snapshot |

| \`BI\_DailySnapshot\` | Daily operational snapshot |

| \`BI\_MonthlySnapshot\` | Monthly operational snapshot |

| \`BI\_ForecastModel\` | Forecast model definitions |

| \`BI\_ForecastRun\` | Forecast execution runs |

| \`BI\_ForecastPeriod\` | Forecast periods |

| \`BI\_ForecastResult\` | Forecast results |

| \`BI\_ForecastAccuracy\` | Forecast accuracy tracking |

| \`BI\_ForecastDrivers\` | Forecast driver data |

| \`BI\_KPI\` | KPI definitions |

| \`BI\_TaxReconciliation\` | Tax reconciliation |

| \`BI\_BudgetVariance\` | Budget variance |

\#\#\# 3\.13 Artificial Intelligence Layer \(\`AI\_\`\)

| Table | Purpose |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|

| \`AI\_Metadata\` | File fingerprint/metadata |

| \`AI\_Mapping\` | AI mapping memory |

| \`AI\_Learning\` | AI learning records |

| \`AI\_Feedback\` | User feedback for AI |

\#\#\# 3\.14 Key Relationships

\#\#\#\# 3\.14\.1 Party Relationships

\`\`\`

MST\_Party \(1\) ──── \(∞\) MST\_PartyAddress

MST\_Party \(1\) ──── \(∞\) MST\_PartyContact

MST\_Party \(1\) ──── \(∞\) MST\_PartyBankAccount

MST\_Party \(1\) ──── \(1\) MST\_Customer

MST\_Party \(1\) ──── \(1\) MST\_Employee

MST\_Party \(1\) ──── \(1\) MST\_Connector

MST\_Party \(1\) ──── \(1\) MST\_Vendor

MST\_Party \(1\) ──── \(1\) MST\_Lender

\`\`\`

\#\#\#\# 3\.14\.2 Case Relationships

\`\`\`

MST\_Customer \(1\) ──── \(∞\) TRN\_Case

MST\_Lender \(1\) ──── \(∞\) TRN\_Case

MST\_Product \(1\) ──── \(∞\) TRN\_Case

TRN\_Case \(1\) ──── \(∞\) TRN\_CaseStatusHistory

TRN\_Case \(1\) ──── \(∞\) TRN\_Disbursement

TRN\_Case \(1\) ──── \(∞\) TRN\_CaseConnectorSplit

TRN\_Case \(1\) ──── \(∞\) TRN\_CaseEmployeeSplit

TRN\_Case \(1\) ──── \(∞\) TRN\_Revenue

TRN\_Case \(1\) ──── \(∞\) TRN\_Commission

TRN\_Case \(1\) ──── \(∞\) TRN\_IncentiveEarned

\`\`\`

\#\#\#\# 3\.14\.3 Financial Relationships

\`\`\`

TRN\_Case \(1\) ──── \(∞\) TRN\_Revenue

TRN\_Case \(1\) ──── \(∞\) TRN\_Commission

TRN\_Case \(1\) ──── \(∞\) TRN\_IncentiveEarned

TRN\_Revenue \(1\) ──── \(∞\) TRN\_Invoice

TRN\_Commission \(1\) ──── \(∞\) TRN\_Payment

TRN\_Invoice \(1\) ──── \(∞\) TRN\_Payment

TRN\_Expense \(1\) ──── \(∞\) TRN\_Payment

TRN\_TaxLiability \(1\) ──── \(∞\) TRN\_StatutoryPayment

\`\`\`

\#\#\#\# 3\.14\.4 ETL Relationships

\`\`\`

ETL\_ImportBatch \(1\) ──── \(∞\) ETL\_StagingRawData

ETL\_ImportBatch \(1\) ──── \(∞\) ETL\_ErrorLog

ETL\_ImportBatch \(1\) ──── \(∞\) ETL\_DataLineage

ETL\_ImportBatch \(1\) ──── \(∞\) ETL\_DataQualityScore

\`\`\`

\-\-\-

\#\# 4\. Data Dictionary – Volume 1: Enterprise Standards & Conventions

\#\#\# 4\.1 Purpose

The Data Dictionary is the single authoritative definition of every data element within the ODOS platform\. It serves as the master reference for all downstream artefacts: Database Design, DDL Generation, ETL Development, Rule Engine configuration, API development, UI design, Reporting, Dashboards, AI models, Validation Engines, Testing, and Future Integrations\.

\#\#\# 4\.2 Document Standards

| Standard | Description |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \*\*Language\*\* | All definitions shall be in clear, unambiguous business English |

| \*\*Consistency\*\* | Terminology shall be consistent with the Business Glossary |

| \*\*Versioning\*\* | This document shall be versioned; Version 1\.0 is the approved baseline |

| \*\*Audit\*\* | This document is auditable; all changes shall be traceable to approved ACRs |

\#\#\# 4\.3 Naming Standards

| Object Type | Standard | Example |

|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|

| \*\*Table Name\*\* | \`Prefix\_EntityName\` where \`Prefix\` is the architecture layer | \`TRN\_Case\`, \`MST\_Lender\`, \`ETL\_ImportBatch\` |

| \*\*Primary Key\*\* | \`EntityNameID\` | \`CaseID\`, \`LenderID\`, \`BatchGUID\` |

| \*\*Foreign Key\*\* | \`ReferencedEntityNameID\` | \`CustomerID\`, \`LenderID\`, \`CompanyID\` |

| \*\*Surrogate Key\*\* | \`EntityNameID\` \(Auto\-incrementing integer\) | \`CaseID\`, \`PaymentID\` |

| \*\*Natural Key\*\* | Business\-readable identifier | \`PAN\`, \`UTR\_Number\`, \`CaseNumber\` |

| \*\*Boolean\*\* | \`Is\` \+ Adjective/Noun | \`IsActive\`, \`IsDeleted\`, \`IsVerified\` |

| \*\*Date/Time\*\* | \`Date\` suffix for dates, \`DateTime\` for timestamps | \`DisbursementDate\`, \`CreatedDateTime\` |

| \*\*Amount/Currency\*\* | \`Amount\` suffix or explicit indicator | \`DisbursementAmount\`, \`NetAmount\` |

| \*\*Code\*\* | \`Code\` suffix | \`LenderCode\`, \`ProductCode\`, \`RuleCode\` |

| \*\*Name\*\* | \`Name\` suffix | \`LenderName\`, \`ProductName\` |

\#\#\# 4\.4 Enterprise Data Standards \(Logical Data Types\)

| Logical Type | Description | Example |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|

| \*\*ID\*\* | Surrogate key \(integer, auto\-incrementing\) | \`CaseID\`, \`LenderID\` |

| \*\*Code\*\* | Alphanumeric code \(max 50 chars\) | \`LenderCode\`, \`ProductCode\` |

| \*\*Name\*\* | Short textual description \(max 255 chars\) | \`LenderName\`, \`ProductName\` |

| \*\*Description\*\* | Longer textual description \(max 1000 chars\) | \`BusinessDefinition\`, \`Description\` |

| \*\*JSON\*\* | Structured JSON data \(unlimited\) | \`EligibilityRule\_JSON\`, \`Condition\_JSON\` |

| \*\*Amount\*\* | Monetary value \(18\-digit precision, 4 decimal places\) | \`DisbursementAmount\`, \`NetAmount\` |

| \*\*Rate\*\* | Percentage value \(10\-digit precision, 4 decimal places\) | \`CommissionRate\`, \`GSTRate\` |

| \*\*Boolean\*\* | True/False \(stored as 0/1\) | \`IsActive\`, \`IsDeleted\` |

| \*\*Date\*\* | Calendar date \(YYYY\-MM\-DD\) | \`DisbursementDate\`, \`InvoiceDate\` |

| \*\*DateTime\*\* | Date and time with timezone \(UTC\) | \`CreatedDateTime\`, \`LastModifiedDateTime\` |

| \*\*Text\*\* | Free\-form text \(unlimited\) | \`Remarks\`, \`Comments\` |

| \*\*Integer\*\* | Whole number | \`Tenure\`, \`RecordVersion\` |

| \*\*GUID\*\* | Globally unique identifier \(UUID\) | \`BatchGUID\` |

\#\#\# 4\.5 Mandatory Audit Fields \(Enterprise Standard\)

Every table in ODOS \*\*must\*\* include the following mandatory audit fields:

| Field Name | Logical Type | Nullable | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \`IsActive\` | Boolean | No \(Default = 1\) | Soft delete flag\. 0 = Inactive \(logically deleted\) |

| \`IsDeleted\` | Boolean | No \(Default = 0\) | Permanent deletion flag\. 1 = Permanently deleted |

| \`CreatedBy\` | Text \(50\) | No \(Default = 'SYSTEM'\) | User ID or system name who created the record |

| \`CreatedDateTime\` | DateTime | No \(Default = CURRENT\_TIMESTAMP\) | Timestamp of record creation |

| \`LastModifiedBy\` | Text \(50\) | No \(Default = 'SYSTEM'\) | User ID or system name who last modified the record |

| \`LastModifiedDateTime\` | DateTime | No \(Default = CURRENT\_TIMESTAMP\) | Timestamp of the last modification |

| \`DeletedBy\` | Text \(50\) | Yes | User ID or system name who deleted the record |

| \`DeletedDateTime\` | DateTime | Yes | Timestamp of the deletion |

| \`RecordVersion\` | Integer | No \(Default = 1\) | Optimistic locking\. Increments on each update |

| \`EffectiveFrom\` | DateTime | No \(Default = CURRENT\_TIMESTAMP\) | Start of validity \(for temporal tracking\) |

| \`EffectiveTo\` | DateTime | Yes | End of validity \(NULL = currently valid\) |

| \`SourceFileName\` | Text \(500\) | Yes | Original uploaded file name |

| \`SourceSheetName\` | Text \(255\) | Yes | Sheet name in the source file |

| \`SourceRowNumber\` | Integer | Yes | Row number in the source file |

| \`ImportBatchGUID\` | GUID | Yes | Links to \`ETL\_ImportBatch\` for lineage tracking |

| \`CompanyID\` | ID | No \(Default = 1\) | Multi\-tenant isolation\. Links to \`MST\_Company\` |

\#\#\# 4\.6 Data Classification Standards

| Classification | Description | Example |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|

| \*\*Master Data\*\* | Core business entities that are stable and referenced by transactions | Customers, Lenders, Products |

| \*\*Reference Data\*\* | Static lookup values | States, Districts, Status Codes, Priority |

| \*\*Transaction Data\*\* | Operational business events | Cases, Revenues, Payments |

| \*\*Configuration Data\*\* | System settings and parameters | Company Settings, Auto\-numbering, Features |

| \*\*Metadata\*\* | Data that defines other data | Table definitions, Field mappings, Reports |

| \*\*Audit Data\*\* | Historical records of changes | Audit Trail, Login History |

| \*\*Analytical Data\*\* | Pre\-aggregated snapshots for BI | Daily Snapshot, Portfolio Risk Snapshot |

| \*\*AI Data\*\* | Learning and mapping metadata | Mapping Memory, Feedback, Confidence Scores |

\#\#\# 4\.7 Security & Sensitivity Standards

| Sensitivity Level | Description | Handling |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|

| \*\*Public\*\* | Non\-sensitive information | No restrictions |

| \*\*Internal\*\* | For internal use only | Restricted to authenticated users |

| \*\*Confidential\*\* | Sensitive business information | Role\-based access control \(RBAC\) |

| \*\*Restricted\*\* | Highly sensitive data \(PII, financial\) | RBAC \+ encryption \+ masking |

| \*\*PII\*\* | Personally Identifiable Information | Masking \+ access logging \+ DPDP/GDPR compliance |

\#\#\# 4\.8 Relationship & Cardinality Standards

| Relationship | Cardinality | Description | Example |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|

| \*\*One\-to\-One\*\* | \`1 → 1\` | One record in Table A maps to exactly one record in Table B | \`MST\_Party\` ↔ \`MST\_Customer\` |

| \*\*One\-to\-Many\*\* | \`1 → ∞\` | One record in Table A maps to many records in Table B | \`MST\_Lender\` → \`MST\_Product\` |

| \*\*Many\-to\-One\*\* | \`∞ → 1\` | Many records in Table A map to one record in Table B | \`TRN\_Case\` → \`MST\_Lender\` |

| \*\*Many\-to\-Many\*\* | \`∞ → ∞\` | Many records in Table A map to many records in Table B | \`TRN\_Case\` ↔ \`MST\_Connector\` |

\*\*Junction Tables:\*\*

\- Many\-to\-Many relationships are implemented via \*\*junction tables\*\* that contain foreign keys to both related tables\.

\- Junction tables often have a composite primary key \`\(TableAID, TableBID\)\`\.

\-\-\-

\#\# 5\. Data Dictionary – Volume 2: Table\-by\-Table Definitions

\#\#\# 5\.1 Document Standards & Structure

| Aspect | Standard |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|

| \*\*Table Information\*\* | Table Name, Friendly Name, Layer, Business Purpose, Business Owner, Classification, Criticality, Lifecycle Stage |

| \*\*Relationships\*\* | Primary Key, Foreign Keys, Parent Tables, Child Tables, Cardinality, Delete/Update Behaviour |

| \*\*Fields\*\* | Field Name, Logical Type, Nullable, Mandatory, Validation, Default, Business Definition |

| \*\*AI & Governance\*\* | AI Reads, AI Writes, AI Learns, AI Suggests, Human Approval Required, Data Steward |

| \*\*Performance\*\* | Expected Volume, Growth Rate, Read/Write Pattern, Index Candidates, Partition/Archival Candidates |

| \*\*Cross\-References\*\* | Business Glossary, Related Tables, Rule Engine, Reports |

\#\#\# 5\.2 Layer 1: Metadata \(\`META\_\`\)

\#\#\#\# Table: \`META\_TableDefinition\`

| Property | Detail |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Table Name\*\* | \`META\_TableDefinition\` |

| \*\*Friendly Name\*\* | Table Definitions |

| \*\*Architecture Layer\*\* | \`META\_\` |

| \*\*Business Purpose\*\* | Master catalog defining every table in the ODOS system |

| \*\*Business Owner\*\* | Data Governance / Technology |

| \*\*Data Classification\*\* | Metadata |

| \*\*Criticality\*\* | Mission Critical |

\*\*Primary Key:\*\* \`TableDefID\` \(Surrogate Key\)  

\*\*Foreign Keys:\*\* \`CompanyID\` → \`MST\_Company\`

\*\*Key Fields:\*\*

| Field Name | Logical Type | Mandatory | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \`TableDefID\` | ID | Yes | Surrogate primary key |

| \`TableName\` | Code \(100\) | Yes | Logical table name \(e\.g\., \`TRN\_Case\`\) |

| \`FriendlyName\` | Name \(100\) | Yes | Business\-friendly table name |

| \`TableDescription\` | Text \(1000\) | No | Description of the table's purpose |

| \`SchemaLayer\` | Code \(10\) | Yes | Architecture layer prefix |

\#\#\#\# Table: \`META\_FieldDefinition\`

| Property | Detail |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Table Name\*\* | \`META\_FieldDefinition\` |

| \*\*Friendly Name\*\* | Field Definitions |

| \*\*Architecture Layer\*\* | \`META\_\` |

| \*\*Business Purpose\*\* | Master catalog defining every field \(column\) in every table |

| \*\*Business Owner\*\* | Data Governance / Technology |

| \*\*Data Classification\*\* | Metadata |

| \*\*Criticality\*\* | Mission Critical |

\*\*Primary Key:\*\* \`FieldDefID\` \(Surrogate Key\)  

\*\*Foreign Keys:\*\* \`TableDefID\` → \`META\_TableDefinition\`, \`CompanyID\` → \`MST\_Company\`

\*\*Key Fields:\*\*

| Field Name | Logical Type | Mandatory | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \`FieldDefID\` | ID | Yes | Surrogate primary key |

| \`TableDefID\` | ID | Yes | Links to the parent table |

| \`FieldName\` | Code \(100\) | Yes | Logical field name \(e\.g\., \`DisbursementAmount\`\) |

| \`FriendlyName\` | Name \(100\) | Yes | Business\-friendly field name |

| \`BusinessDefinition\` | Text \(2000\) | Yes | Clear business meaning \(from Glossary\) |

| \`BusinessOwner\` | Text \(100\) | Yes | Functional owner |

| \`DataSteward\` | Text \(100\) | Yes | Person/role responsible for data quality |

| \`LogicalDataType\` | Code \(20\) | Yes | Logical data type \(implementation\-neutral\) |

| \`IsMandatory\` | Boolean | Yes | Is the field physically NOT NULL? |

| \`IsSensitive\` | Boolean | Yes | Contains PII or sensitive data? |

| \`MaskingRule\` | Code \(50\) | No | Masking pattern \(e\.g\., \`XXXXX1234X\`\) |

| \`EncryptionRequired\` | Boolean | Yes | Is encryption at rest required? |

| \`ValidationRuleID\` | ID | No | Links to a specific validation rule |

| \`GlobalSearchEligible\` | Boolean | Yes | Can this field be globally searched? |

| \`UI\_ControlType\` | Code \(30\) | No | Recommended UI control |

| \`IsDimension\` | Boolean | Yes | Is this a BI dimension? |

| \`IsMeasure\` | Boolean | Yes | Is this a BI measure? |

| \`IndexCandidate\` | Boolean | Yes | Should this field be indexed? |

| \`AI\_Generated\` | Boolean | Yes | Can AI generate a value for this field? |

| \`HumanApprovalRequired\` | Boolean | Yes | Requires human approval for AI changes? |

\#\#\#\# Table: \`META\_FieldMapping\`

| Property | Detail |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Table Name\*\* | \`META\_FieldMapping\` |

| \*\*Friendly Name\*\* | Field Mappings |

| \*\*Architecture Layer\*\* | \`META\_\` |

| \*\*Business Purpose\*\* | Maps external source headers to internal ODOS field definitions |

| \*\*Business Owner\*\* | Data Operations / Technology |

| \*\*Data Classification\*\* | Metadata |

| \*\*Criticality\*\* | High |

\*\*Primary Key:\*\* \`MappingID\` \(Surrogate Key\)  

\*\*Foreign Keys:\*\* \`FieldDefID\` → \`META\_FieldDefinition\`, \`CompanyID\` → \`MST\_Company\`

\*\*Key Fields:\*\*

| Field Name | Logical Type | Mandatory | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \`MappingID\` | ID | Yes | Surrogate primary key |

| \`CompanyID\` | ID | Yes | Tenant isolation |

| \`SourceSystem\` | Code \(100\) | Yes | Source system identifier |

| \`SourceHeader\` | Text \(255\) | Yes | The header string from the source file |

| \`FieldDefID\` | ID | Yes | Target ODOS field |

| \`ConfidenceScore\` | Rate | No | AI confidence in the mapping |

| \`IsVerified\` | Boolean | Yes | Has a human verified this mapping? |

| \`UsageCount\` | Integer | Yes | Number of times used successfully |

\#\#\# 5\.3 Layer 2: Configuration \(\`CFG\_\`\)

\#\#\#\# Table: \`CFG\_CompanySettings\`

| Property | Detail |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Table Name\*\* | \`CFG\_CompanySettings\` |

| \*\*Friendly Name\*\* | Company Settings |

| \*\*Architecture Layer\*\* | \`CFG\_\` |

| \*\*Business Purpose\*\* | Stores tenant\-specific configuration settings |

| \*\*Business Owner\*\* | Administration |

| \*\*Data Classification\*\* | Configuration Data |

| \*\*Criticality\*\* | Mission Critical |

\*\*Primary Key:\*\* \`CompanyID\` \(FK to \`MST\_Company\`\)  

\*\*Foreign Keys:\*\* \`CompanyID\` → \`MST\_Company\`

\*\*Key Fields:\*\*

| Field Name | Logical Type | Mandatory | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \`CompanyID\` | ID | Yes | Primary key, links to the company master |

| \`DefaultCurrency\` | Code \(3\) | Yes | Default currency for the tenant |

| \`DefaultDateFormat\` | Code \(20\) | Yes | Date format for the tenant |

| \`Timezone\` | Code \(50\) | Yes | Timezone for the tenant |

| \`LogoPath\` | Text \(500\) | No | File path for company logo |

| \`ThemeColor\` | Code \(7\) | No | UI theme colour \(white\-labeling\) |

| \`AI\_ConfidenceThreshold\` | Rate | Yes | Minimum confidence for AI recommendations |

\#\#\# 5\.4 Layer 3: Security \(\`SEC\_\`\)

\#\#\#\# Table: \`SEC\_User\`

| Property | Detail |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Table Name\*\* | \`SEC\_User\` |

| \*\*Friendly Name\*\* | Users |

| \*\*Architecture Layer\*\* | \`SEC\_\` |

| \*\*Business Purpose\*\* | Stores user credentials and profile information |

| \*\*Business Owner\*\* | Administration / IT |

| \*\*Data Classification\*\* | Security Data |

| \*\*Criticality\*\* | Mission Critical |

\*\*Primary Key:\*\* \`UserID\` \(Surrogate Key\)  

\*\*Foreign Keys:\*\* \`EmployeeID\` → \`MST\_Employee\`, \`CompanyID\` → \`MST\_Company\`, \`RoleID\` → \`SEC\_Role\`

\*\*Key Fields:\*\*

| Field Name | Logical Type | Mandatory | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \`UserID\` | ID | Yes | Surrogate primary key |

| \`CompanyID\` | ID | Yes | Tenant isolation |

| \`EmployeeID\` | ID | Yes | Links to the internal employee record |

| \`RoleID\` | ID | Yes | The user's primary role |

| \`Username\` | Text \(50\) | Yes | Login username |

| \`PasswordHash\` | Text \(255\) | Yes | Hashed password |

| \`AllowedBranchIDs\_JSON\` | JSON | No | Row\-Level Security \(RLS\) – branches the user can access |

| \`IsActive\` | Boolean | Yes | Can the user log in? |

| \`LastLogin\` | DateTime | No | Timestamp of the last login |

\#\#\#\# Table: \`SEC\_AuditTrail\`

| Property | Detail |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Table Name\*\* | \`SEC\_AuditTrail\` |

| \*\*Friendly Name\*\* | Audit Trail |

| \*\*Architecture Layer\*\* | \`SEC\_\` |

| \*\*Business Purpose\*\* | System\-wide audit trail of every change to every record |

| \*\*Business Owner\*\* | Administration / Compliance |

| \*\*Data Classification\*\* | Audit Data |

| \*\*Criticality\*\* | Mission Critical |

\*\*Primary Key:\*\* \`AuditID\` \(Surrogate Key\)  

\*\*Foreign Keys:\*\* \`ChangedByUserID\` → \`SEC\_User\`

\*\*Key Fields:\*\*

| Field Name | Logical Type | Mandatory | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \`AuditID\` | ID | Yes | Surrogate primary key |

| \`CompanyID\` | ID | Yes | Tenant isolation |

| \`TableName\` | Code \(100\) | Yes | The table where the change occurred |

| \`RecordID\` | ID | Yes | The Primary Key of the changed record |

| \`Action\` | Code \(20\) | Yes | INSERT, UPDATE, DELETE, APPROVE, REJECT |

| \`OldValues\_JSON\` | JSON | No | Snapshot of the record before the change |

| \`NewValues\_JSON\` | JSON | No | Snapshot of the record after the change |

| \`ChangedByUserID\` | ID | Yes | Who made the change |

| \`ChangeDateTime\` | DateTime | Yes | Timestamp of the change |

\#\#\# 5\.5 Layer 4: Master Data \(\`MST\_\`\)

\#\#\#\# Table: \`MST\_Company\`

| Property | Detail |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Table Name\*\* | \`MST\_Company\` |

| \*\*Friendly Name\*\* | Company / Tenant |

| \*\*Architecture Layer\*\* | \`MST\_\` |

| \*\*Business Purpose\*\* | Root tenant record\. Represents the DSA organisation |

| \*\*Business Owner\*\* | Administration |

| \*\*Data Classification\*\* | Master Data |

| \*\*Criticality\*\* | Mission Critical |

\*\*Primary Key:\*\* \`CompanyID\` \(Surrogate Key\)

\*\*Key Fields:\*\*

| Field Name | Logical Type | Mandatory | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \`CompanyID\` | ID | Yes | Surrogate primary key |

| \`CompanyCode\` | Code \(20\) | Yes | Internal company code |

| \`CompanyName\` | Name \(255\) | Yes | Legal name of the company |

| \`PAN\` | Code \(10\) | Yes | Permanent Account Number |

| \`GSTIN\` | Code \(15\) | No | GST Identification Number |

| \`CIN\` | Code \(21\) | No | Corporate Identification Number |

| \`TAN\` | Code \(10\) | No | Tax Deduction Account Number |

| \`RegisteredAddress\` | Text \(500\) | No | Registered office address |

| \`ContactNumber\` | Text \(15\) | No | Primary contact number |

| \`Email\` | Text \(255\) | No | Primary email address |

| \`IsActive\` | Boolean | Yes | Is the company active? |

\#\#\#\# Table: \`MST\_Party\`

| Property | Detail |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Table Name\*\* | \`MST\_Party\` |

| \*\*Friendly Name\*\* | Party |

| \*\*Architecture Layer\*\* | \`MST\_\` |

| \*\*Business Purpose\*\* | Universal party master\. Root for all human/legal entities |

| \*\*Business Owner\*\* | Data Governance |

| \*\*Data Classification\*\* | Master Data |

| \*\*Criticality\*\* | Mission Critical |

\*\*Primary Key:\*\* \`PartyID\` \(Surrogate Key\)  

\*\*Foreign Keys:\*\* \`CompanyID\` → \`MST\_Company\`, \`PartyTypeID\` → \`REF\_PartyType\`

\*\*Key Fields:\*\*

| Field Name | Logical Type | Mandatory | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \`PartyID\` | ID | Yes | Surrogate primary key |

| \`CompanyID\` | ID | Yes | Tenant isolation |

| \`PartyTypeID\` | ID | Yes | Party type \(Customer, Employee, etc\.\) |

| \`FullName\` | Name \(255\) | Yes | Full name of the party |

| \`PAN\` | Code \(10\) | No | Permanent Account Number |

| \`GSTIN\` | Code \(15\) | No | GST Identification Number |

| \`KYCStatus\` | Code \(20\) | No | KYC status |

\#\#\#\# Table: \`MST\_Customer\`

| Property | Detail |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Table Name\*\* | \`MST\_Customer\` |

| \*\*Friendly Name\*\* | Customer |

| \*\*Architecture Layer\*\* | \`MST\_\` |

| \*\*Business Purpose\*\* | Customer master data |

| \*\*Business Owner\*\* | Sales / Operations |

| \*\*Data Classification\*\* | Master Data |

| \*\*Criticality\*\* | Mission Critical |

\*\*Primary Key:\*\* \`CustomerID\` \(Surrogate Key\)  

\*\*Foreign Keys:\*\* \`CustomerID\` → \`MST\_Party\.PartyID\`, \`CompanyID\` → \`MST\_Company\`

\*\*Key Fields:\*\*

| Field Name | Logical Type | Mandatory | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \`CustomerID\` | ID | Yes | Surrogate primary key \(links to MST\_Party\) |

| \`CompanyID\` | ID | Yes | Tenant isolation |

| \`CibilScore\` | Integer | No | Credit score |

| \`DateOfBirth\` | Date | No | Date of birth |

| \`Occupation\` | Code \(50\) | No | Occupation type |

\#\#\# 5\.6 Layer 5: Rules \(\`RUL\_\`\)

\#\#\#\# Table: \`RUL\_CommissionRule\`

| Property | Detail |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Table Name\*\* | \`RUL\_CommissionRule\` |

| \*\*Friendly Name\*\* | Commission Rules |

| \*\*Architecture Layer\*\* | \`RUL\_\` |

| \*\*Business Purpose\*\* | Configurable commission calculation rules |

| \*\*Business Owner\*\* | Finance |

| \*\*Data Classification\*\* | Rules Data |

| \*\*Criticality\*\* | High |

\*\*Primary Key:\*\* \`CommissionRuleID\` \(Surrogate Key\)  

\*\*Foreign Keys:\*\* \`CompanyID\` → \`MST\_Company\`, \`AgreementID\` → \`MST\_LenderAgreement\`

\*\*Key Fields:\*\*

| Field Name | Logical Type | Mandatory | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \`CommissionRuleID\` | ID | Yes | Surrogate primary key |

| \`CompanyID\` | ID | Yes | Tenant isolation |

| \`RuleCode\` | Code \(50\) | Yes | Unique rule code |

| \`AgreementID\` | ID | No | Specific agreement \(most specific\) |

| \`LenderID\` | ID | No | Lender scope |

| \`ProductID\` | ID | No | Product scope |

| \`BasisType\` | Code \(20\) | Yes | Disbursement, Revenue, etc\. |

| \`CalculationType\` | Code \(20\) | Yes | Percentage, Flat, Slab |

| \`FlatRate\` | Rate | No | Flat rate if Percentage/Flat |

| \`EffectiveFrom\` | DateTime | Yes | Start of validity |

| \`EffectiveTo\` | DateTime | No | End of validity |

\#\#\# 5\.7 Layer 6: Transactions \(\`TRN\_\`\)

\#\#\#\# Table: \`TRN\_Case\`

| Property | Detail |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Table Name\*\* | \`TRN\_Case\` |

| \*\*Friendly Name\*\* | Case |

| \*\*Architecture Layer\*\* | \`TRN\_\` |

| \*\*Business Purpose\*\* | Loan case tracking |

| \*\*Business Owner\*\* | Operations |

| \*\*Data Classification\*\* | Transaction Data |

| \*\*Criticality\*\* | Mission Critical |

\*\*Primary Key:\*\* \`CaseID\` \(Surrogate Key\)  

\*\*Foreign Keys:\*\* \`CustomerID\` → \`MST\_Customer\`, \`LenderID\` → \`MST\_Lender\`, \`ProductID\` → \`MST\_Product\`, \`AgreementID\` → \`MST\_LenderAgreement\`

\*\*Key Fields:\*\*

| Field Name | Logical Type | Mandatory | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \`CaseID\` | ID | Yes | Surrogate primary key |

| \`CompanyID\` | ID | Yes | Tenant isolation |

| \`CaseNumber\` | Code \(50\) | Yes | Auto\-generated business key |

| \`CustomerID\` | ID | Yes | Links to customer |

| \`LenderID\` | ID | Yes | Links to lender |

| \`ProductID\` | ID | Yes | Links to product |

| \`AgreementID\` | ID | Yes | Links to lender agreement |

| \`SanctionAmount\` | Amount | No | Sanctioned loan amount |

| \`DisbursementAmount\` | Amount | No | Total disbursed amount |

| \`ApplicationDate\` | Date | No | Application date |

| \`SanctionDate\` | Date | No | Sanction date |

| \`DisbursementDate\` | Date | No | Disbursement date |

| \`InvoiceGeneratedDate\` | Date | No | Invoice generation date |

| \`InvoiceDueDate\` | Date | No | Invoice due date |

| \`PaymentReceivedDate\` | Date | No | Payment received date |

| \`CaseStatus\` | Code \(20\) | Yes | Current case status |

| \`CampaignID\` | ID | No | Linked campaign \(if any\) |

\#\#\#\# Table: \`TRN\_Revenue\`

| Property | Detail |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Table Name\*\* | \`TRN\_Revenue\` |

| \*\*Friendly Name\*\* | Revenue |

| \*\*Architecture Layer\*\* | \`TRN\_\` |

| \*\*Business Purpose\*\* | Commission income from lenders |

| \*\*Business Owner\*\* | Finance |

| \*\*Data Classification\*\* | Financial Data |

| \*\*Criticality\*\* | Mission Critical |

\*\*Primary Key:\*\* \`RevenueID\` \(Surrogate Key\)  

\*\*Foreign Keys:\*\* \`CaseID\` → \`TRN\_Case\`, \`CompanyID\` → \`MST\_Company\`, \`AgreementID\` → \`MST\_LenderAgreement\`

\*\*Key Fields:\*\*

| Field Name | Logical Type | Mandatory | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \`RevenueID\` | ID | Yes | Surrogate primary key |

| \`CompanyID\` | ID | Yes | Tenant isolation |

| \`CaseID\` | ID | Yes | Links to case |

| \`AgreementID\` | ID | Yes | Links to lender agreement |

| \`RevenueDate\` | Date | Yes | Revenue date |

| \`BaseRevenueAmount\` | Amount | Yes | Base commission amount |

| \`GST\_Amount\` | Amount | Yes | GST applicable |

| \`TDS\_Amount\` | Amount | Yes | TDS deducted |

| \`NetAmount\` | Amount | Yes | Net revenue |

| \`UTR\_Number\` | Code \(50\) | No | Payment UTR number |

| \`PaymentStatus\` | Code \(20\) | Yes | Payment status |

\#\#\#\# Table: \`TRN\_Payment\`

| Property | Detail |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Table Name\*\* | \`TRN\_Payment\` |

| \*\*Friendly Name\*\* | Payment |

| \*\*Architecture Layer\*\* | \`TRN\_\` |

| \*\*Business Purpose\*\* | Outbound payments |

| \*\*Business Owner\*\* | Finance / Treasury |

| \*\*Data Classification\*\* | Financial Data |

| \*\*Criticality\*\* | Mission Critical |

\*\*Primary Key:\*\* \`PaymentID\` \(Surrogate Key\)  

\*\*Foreign Keys:\*\* \`CompanyID\` → \`MST\_Company\`

\*\*Key Fields:\*\*

| Field Name | Logical Type | Mandatory | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \`PaymentID\` | ID | Yes | Surrogate primary key |

| \`CompanyID\` | ID | Yes | Tenant isolation |

| \`PaymentNumber\` | Code \(50\) | Yes | Auto\-generated business key |

| \`UTR\_Number\` | Code \(50\) | No | Bank UTR \(UNIQUE constraint\) |

| \`PaymentDate\` | Date | Yes | Payment date |

| \`PaymentAmount\` | Amount | Yes | Payment amount |

| \`PaymentMode\` | Code \(20\) | Yes | Payment mode |

| \`ReconciliationStatus\` | Code \(20\) | Yes | Reconciliation status |

\#\#\# 5\.8 Layer 7: ETL \(\`ETL\_\`\)

\#\#\#\# Table: \`ETL\_ImportBatch\`

| Property | Detail |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Table Name\*\* | \`ETL\_ImportBatch\` |

| \*\*Friendly Name\*\* | Import Batch |

| \*\*Architecture Layer\*\* | \`ETL\_\` |

| \*\*Business Purpose\*\* | Tracks data import batches |

| \*\*Business Owner\*\* | Data Operations |

| \*\*Data Classification\*\* | Operational Data |

| \*\*Criticality\*\* | High |

\*\*Primary Key:\*\* \`BatchGUID\` \(GUID\)  

\*\*Foreign Keys:\*\* \`CompanyID\` → \`MST\_Company\`

\*\*Key Fields:\*\*

| Field Name | Logical Type | Mandatory | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \`BatchGUID\` | GUID | Yes | Unique batch identifier |

| \`CompanyID\` | ID | Yes | Tenant isolation |

| \`SourceSystem\` | Code \(100\) | Yes | Source system identifier |

| \`FileName\` | Text \(500\) | Yes | Original file name |

| \`ImportStatus\` | Code \(20\) | Yes | Status of the import |

| \`IsAtomicTransaction\` | Boolean | Yes | If TRUE, entire batch must succeed or fail |

| \`IsComplete\` | Boolean | Yes | Batch processing completed |

| \`ImportDateTime\` | DateTime | Yes | Import timestamp |

\#\#\# 5\.9 Layer 8: Audit & Documents \(\`AUD\_\`\)

\#\#\#\# Table: \`AUD\_Document\`

| Property | Detail |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Table Name\*\* | \`AUD\_Document\` |

| \*\*Friendly Name\*\* | Document |

| \*\*Architecture Layer\*\* | \`AUD\_\` |

| \*\*Business Purpose\*\* | Document metadata |

| \*\*Business Owner\*\* | Operations |

| \*\*Data Classification\*\* | Document Data |

| \*\*Criticality\*\* | High |

\*\*Primary Key:\*\* \`DocumentID\` \(Surrogate Key\)  

\*\*Foreign Keys:\*\* \`CompanyID\` → \`MST\_Company\`, \`CaseID\` → \`TRN\_Case\`

\*\*Key Fields:\*\*

| Field Name | Logical Type | Mandatory | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \`DocumentID\` | ID | Yes | Surrogate primary key |

| \`CompanyID\` | ID | Yes | Tenant isolation |

| \`DocumentType\` | Code \(50\) | Yes | Document type \(PAN, Aadhaar, etc\.\) |

| \`FileName\` | Text \(255\) | Yes | Original file name |

| \`FileHash\` | Text \(64\) | Yes | SHA\-256 hash for deduplication |

| \`FileSize\` | Integer | Yes | File size in bytes |

| \`OCRText\` | Text | No | OCR extracted text |

| \`IsVerified\` | Boolean | Yes | Document verified |

| \`ExpiryDate\` | Date | No | Document expiry date |

\#\#\# 5\.10 Layer 9: Business Intelligence \(\`BI\_\`\)

\#\#\#\# Table: \`BI\_KPI\`

| Property | Detail |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Table Name\*\* | \`BI\_KPI\` |

| \*\*Friendly Name\*\* | KPI |

| \*\*Architecture Layer\*\* | \`BI\_\` |

| \*\*Business Purpose\*\* | KPI definitions and targets |

| \*\*Business Owner\*\* | BI / Analytics |

| \*\*Data Classification\*\* | Analytical Data |

| \*\*Criticality\*\* | High |

\*\*Primary Key:\*\* \`KPI\_ID\` \(Surrogate Key\)  

\*\*Foreign Keys:\*\* \`CompanyID\` → \`MST\_Company\`

\*\*Key Fields:\*\*

| Field Name | Logical Type | Mandatory | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \`KPI\_ID\` | ID | Yes | Surrogate primary key |

| \`CompanyID\` | ID | Yes | Tenant isolation |

| \`KPI\_Code\` | Code \(50\) | Yes | Unique KPI code |

| \`KPI\_Name\` | Name \(100\) | Yes | KPI name |

| \`KPI\_Category\` | Code \(30\) | Yes | KPI category |

| \`Formula\_JSON\` | JSON | Yes | KPI calculation formula |

| \`TargetValue\` | Rate | No | Target value |

| \`ActualValue\` | Rate | No | Actual value |

| \`PeriodStart\` | Date | Yes | Period start |

| \`PeriodEnd\` | Date | Yes | Period end |

| \`Status\` | Code \(20\) | Yes | On Track, Warning, Critical |

\#\#\# 5\.11 Layer 10: Artificial Intelligence \(\`AI\_\`\)

\#\#\#\# Table: \`AI\_Mapping\`

| Property | Detail |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Table Name\*\* | \`AI\_Mapping\` |

| \*\*Friendly Name\*\* | AI Mapping |

| \*\*Architecture Layer\*\* | \`AI\_\` |

| \*\*Business Purpose\*\* | AI\-assisted field mapping memory |

| \*\*Business Owner\*\* | Technology / AI |

| \*\*Data Classification\*\* | AI Data |

| \*\*Criticality\*\* | High |

\*\*Primary Key:\*\* \`MapID\` \(Surrogate Key\)  

\*\*Foreign Keys:\*\* \`CompanyID\` → \`MST\_Company\`

\*\*Key Fields:\*\*

| Field Name | Logical Type | Mandatory | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \`MapID\` | ID | Yes | Surrogate primary key |

| \`CompanyID\` | ID | Yes | Tenant isolation |

| \`SourceSystem\` | Code \(100\) | Yes | Source system identifier |

| \`SourceHeader\` | Text \(255\) | Yes | Source header string |

| \`FieldDefID\` | ID | Yes | Target field definition |

| \`ConfidenceScore\` | Rate | No | AI confidence in mapping |

| \`UsageCount\` | Integer | Yes | Number of times used |

| \`IsVerified\` | Boolean | Yes | Human verified |

| \`MappingRationale\` | Text | No | Explanation of mapping selection |

\-\-\-

\#\# 6\. Business Glossary

\#\#\# 6\.1 Purpose

The Business Glossary establishes the \*\*single authoritative business vocabulary\*\* for the ODOS platform\. It defines every business term used across the enterprise, ensuring consistent communication among business stakeholders, operations teams, finance, compliance, and technology\.

All future artefacts—including the Data Dictionary, Database Standards, DDL, ETL specifications, APIs, UI designs, and AI models—shall reference this glossary as their primary source of business definition\.

\#\#\# 6\.2 Guiding Philosophy

> \*"This glossary is written not merely to describe today's DSA operations, but to define the enterprise language of the ODOS platform for the next 10\-15 years\. It remains valid even as new lenders, new products, new acquisition channels, and new technologies are introduced\."\*

\#\#\# 6\.3 Glossary Entries

\#\#\#\# 6\.3\.1 Enterprise & Organisational Structure

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0001 |

| \*\*Business Term\*\* | Company |

| \*\*Preferred ODOS Term\*\* | Company |

| \*\*Synonyms\*\* | Organisation, Firm, Entity, Tenant |

| \*\*Business Definition\*\* | The legal entity operating as a Direct Selling Agent \(DSA\) or financial intermediary that owns and operates the ODOS instance |

| \*\*Business Importance\*\* | The Company is the root of the multi\-tenant architecture |

| \*\*Related ERD Entities\*\* | \`MST\_Company\` |

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0002 |

| \*\*Business Term\*\* | Tenant |

| \*\*Preferred ODOS Term\*\* | Tenant |

| \*\*Synonyms\*\* | Client, Subscriber, Organisation |

| \*\*Business Definition\*\* | A logical instance of a Company within a shared ODOS deployment |

| \*\*Business Importance\*\* | The backbone of ODOS's commercial product strategy |

| \*\*Related ERD Entities\*\* | \`MST\_Company\` |

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0003 |

| \*\*Business Term\*\* | Region |

| \*\*Preferred ODOS Term\*\* | Region |

| \*\*Synonyms\*\* | Zone, Area, Territory |

| \*\*Business Definition\*\* | A geographical cluster of Branches within a Company |

| \*\*Business Importance\*\* | Critical for understanding geographic performance |

| \*\*Related ERD Entities\*\* | \`MST\_InternalRegion\` |

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0004 |

| \*\*Business Term\*\* | Branch |

| \*\*Preferred ODOS Term\*\* | Branch |

| \*\*Synonyms\*\* | Office, Location, Outlet, Center |

| \*\*Business Definition\*\* | A physical or logical operational unit within a Region |

| \*\*Business Importance\*\* | Primary unit of operational execution |

| \*\*Related ERD Entities\*\* | \`MST\_InternalBranch\` |

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0005 |

| \*\*Business Term\*\* | Employee |

| \*\*Preferred ODOS Term\*\* | Employee |

| \*\*Synonyms\*\* | Staff, Personnel, Team Member, Associate |

| \*\*Business Definition\*\* | An individual employed by the DSA who performs operational, sales, administrative, or managerial functions |

| \*\*Business Importance\*\* | Employee productivity and incentive alignment are critical success factors |

| \*\*Related ERD Entities\*\* | \`MST\_Employee\` |

\#\#\#\# 6\.3\.2 Sales & Customer Management

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0006 |

| \*\*Business Term\*\* | Customer |

| \*\*Preferred ODOS Term\*\* | Customer |

| \*\*Synonyms\*\* | Borrower, Applicant, Client, Loan Customer |

| \*\*Business Definition\*\* | An individual or entity that applies for a loan through the DSA |

| \*\*Business Importance\*\* | The Customer is the ultimate source of revenue for the DSA |

| \*\*Related ERD Entities\*\* | \`MST\_Customer\` \(extends \`MST\_Party\`\) |

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0007 |

| \*\*Business Term\*\* | Lead |

| \*\*Preferred ODOS Term\*\* | Lead |

| \*\*Synonyms\*\* | Prospect, Inquiry, Opportunity, Referral |

| \*\*Business Definition\*\* | A potential customer who has expressed interest in a loan product |

| \*\*Business Importance\*\* | Lead management is the primary source of future revenue |

| \*\*Related ERD Entities\*\* | \`TRN\_LeadSource\` |

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0008 |

| \*\*Business Term\*\* | KYC \(Know Your Customer\) |

| \*\*Preferred ODOS Term\*\* | KYC |

| \*\*Synonyms\*\* | Customer Due Diligence, Identity Verification |

| \*\*Business Definition\*\* | The process of verifying the identity and credentials of a Customer |

| \*\*Business Importance\*\* | Incomplete or incorrect KYC is a major compliance risk |

| \*\*Related ERD Entities\*\* | \`MST\_Party\.KYCStatus\`, \`AUD\_Document\` |

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0009 |

| \*\*Business Term\*\* | PAN \(Permanent Account Number\) |

| \*\*Preferred ODOS Term\*\* | PAN |

| \*\*Synonyms\*\* | Tax Identification Number, Income Tax PAN |

| \*\*Business Definition\*\* | A unique ten\-character alphanumeric identifier issued by the Indian Income Tax Department |

| \*\*Business Importance\*\* | The most critical business key in the system |

| \*\*Related ERD Entities\*\* | \`MST\_Party\.PAN\` |

\#\#\#\# 6\.3\.3 Lenders & Products

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0010 |

| \*\*Business Term\*\* | Lender |

| \*\*Preferred ODOS Term\*\* | Lender |

| \*\*Synonyms\*\* | Bank, NBFC, Financial Institution, Loan Provider |

| \*\*Business Definition\*\* | A financial institution that provides loan products and pays commission to the DSA |

| \*\*Business Importance\*\* | Lender relationships are the lifeblood of the DSA business |

| \*\*Related ERD Entities\*\* | \`MST\_Lender\` \(extends \`MST\_Party\`\) |

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0011 |

| \*\*Business Term\*\* | Product |

| \*\*Preferred ODOS Term\*\* | Product |

| \*\*Synonyms\*\* | Loan Scheme, Loan Type, Offer, Programme |

| \*\*Business Definition\*\* | A specific loan offering from a Lender |

| \*\*Business Importance\*\* | Product mix directly impacts the DSA's profitability |

| \*\*Related ERD Entities\*\* | \`MST\_Product\` |

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0012 |

| \*\*Business Term\*\* | Agreement \(Lender\) |

| \*\*Preferred ODOS Term\*\* | Lender Agreement |

| \*\*Synonyms\*\* | Contract, MOU, SLA |

| \*\*Business Definition\*\* | The formal commercial contract between the DSA and a Lender |

| \*\*Business Importance\*\* | Accurate agreement configuration is critical for correct commission calculation |

| \*\*Related ERD Entities\*\* | \`MST\_LenderAgreement\` |

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0013 |

| \*\*Business Term\*\* | Campaign \(Lender\) |

| \*\*Preferred ODOS Term\*\* | Lender Campaign |

| \*\*Synonyms\*\* | Offer, Promotion, Incentive Drive, Sales Spiff |

| \*\*Business Definition\*\* | A time\-bound promotional initiative launched by a Lender |

| \*\*Business Importance\*\* | Campaign participation can significantly boost revenue |

| \*\*Related ERD Entities\*\* | \`MST\_LenderCampaign\` |

\#\#\#\# 6\.3\.4 Operations & Loan Lifecycle

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0014 |

| \*\*Business Term\*\* | Case |

| \*\*Preferred ODOS Term\*\* | Case |

| \*\*Synonyms\*\* | Loan Application, File, Proposal, Loan Case |

| \*\*Business Definition\*\* | A single loan transaction sourced by the DSA |

| \*\*Business Importance\*\* | The Case is the atomic unit of profitability |

| \*\*Related ERD Entities\*\* | \`TRN\_Case\`, \`TRN\_CaseStatusHistory\` |

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0015 |

| \*\*Business Term\*\* | Disbursement |

| \*\*Preferred ODOS Term\*\* | Disbursement |

| \*\*Synonyms\*\* | Payout, Loan Release, Fund Transfer |

| \*\*Business Definition\*\* | The actual release of funds by the Lender to the Borrower |

| \*\*Business Importance\*\* | Disbursement volume is the primary driver of DSA revenue |

| \*\*Related ERD Entities\*\* | \`TRN\_Disbursement\`, \`TRN\_Case\.DisbursementAmount\` |

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0016 |

| \*\*Business Term\*\* | Invoice \(DSA to Lender\) |

| \*\*Preferred ODOS Term\*\* | Invoice |

| \*\*Synonyms\*\* | Bill, Claim, Commission Invoice, Payment Request |

| \*\*Business Definition\*\* | The commercial document raised by the DSA to the Lender |

| \*\*Business Importance\*\* | Timely and accurate invoicing ensures predictable cash flow |

| \*\*Related ERD Entities\*\* | \`TRN\_Invoice\` |

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0017 |

| \*\*Business Term\*\* | Turnaround Time \(TAT\) |

| \*\*Preferred ODOS Term\*\* | TAT |

| \*\*Synonyms\*\* | Cycle Time, Processing Time, Lead Time, SLA Duration |

| \*\*Business Definition\*\* | The elapsed time between two defined milestones in the Case lifecycle |

| \*\*Business Importance\*\* | Shorter TAT improves customer experience and increases lender preference |

| \*\*Related ERD Entities\*\* | \`TRN\_CaseStatusHistory\`, \`TRN\_Case\` |

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0018 |

| \*\*Business Term\*\* | SLA \(Service Level Agreement\) |

| \*\*Preferred ODOS Term\*\* | SLA |

| \*\*Synonyms\*\* | Service Standard, Performance Commitment, Operational Guarantee |

| \*\*Business Definition\*\* | A predefined commitment to deliver a service within a specified timeframe |

| \*\*Business Importance\*\* | Meeting SLAs is often a condition for continuing business relationships |

| \*\*Related ERD Entities\*\* | \`RUL\_Workflow\`, \`BI\_KPI\` |

\#\#\#\# 6\.3\.5 Finance & Accounting

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0019 |

| \*\*Business Term\*\* | Revenue |

| \*\*Preferred ODOS Term\*\* | Revenue |

| \*\*Synonyms\*\* | Income, Commission Income, Earnings, Turnover |

| \*\*Business Definition\*\* | The total income earned by the DSA from Lenders |

| \*\*Business Importance\*\* | Revenue growth is the most critical indicator of business health |

| \*\*Related ERD Entities\*\* | \`TRN\_Revenue\`, \`TRN\_CampaignIncentive\` |

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0020 |

| \*\*Business Term\*\* | Commission \(DSA Income\) |

| \*\*Preferred ODOS Term\*\* | Commission |

| \*\*Synonyms\*\* | Brokerage, Incentive, Payout |

| \*\*Business Definition\*\* | The contractual financial consideration earned by the DSA from a Lender |

| \*\*Business Importance\*\* | Commission is the primary revenue engine of the DSA |

| \*\*Related ERD Entities\*\* | \`TRN\_Revenue\`, \`TRN\_Commission\`, \`TRN\_IncentiveEarned\` |

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0021 |

| \*\*Business Term\*\* | Connector Payout |

| \*\*Preferred ODOS Term\*\* | Connector Commission |

| \*\*Synonyms\*\* | Partner Payout, Sub\-DSA Commission, Referral Fee |

| \*\*Business Definition\*\* | The amount paid by the DSA to a Connector for sourcing a Case |

| \*\*Business Importance\*\* | Connector Payouts are the primary cost of customer acquisition |

| \*\*Related ERD Entities\*\* | \`TRN\_Commission\` |

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0022 |

| \*\*Business Term\*\* | Employee Incentive |

| \*\*Preferred ODOS Term\*\* | Incentive |

| \*\*Synonyms\*\* | Success Fee, Performance Bonus, Sales Commission |

| \*\*Business Definition\*\* | The variable compensation paid to internal Employees based on Case performance |

| \*\*Business Importance\*\* | Well\-designed incentives improve employee retention and productivity |

| \*\*Related ERD Entities\*\* | \`TRN\_IncentiveEarned\`, \`TRN\_CaseEmployeeSplit\` |

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0023 |

| \*\*Business Term\*\* | Expense |

| \*\*Preferred ODOS Term\*\* | Expense |

| \*\*Synonyms\*\* | Cost, Operational Outlay, Overhead, Spend |

| \*\*Business Definition\*\* | Any financial outflow incurred by the DSA in the course of its business operations |

| \*\*Business Importance\*\* | Effective expense management is the primary lever for improving profitability |

| \*\*Related ERD Entities\*\* | \`TRN\_Expense\`, \`TRN\_ExpenseClaim\`, \`TRN\_RecurringExpense\` |

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0024 |

| \*\*Business Term\*\* | TDS \(Tax Deducted at Source\) |

| \*\*Preferred ODOS Term\*\* | TDS |

| \*\*Synonyms\*\* | Withholding Tax, Tax Deduction |

| \*\*Business Definition\*\* | Tax deducted by a payer from a payment and remitted to the government |

| \*\*Business Importance\*\* | Incorrect TDS calculation can result in penalties |

| \*\*Related ERD Entities\*\* | \`RUL\_TDSRule\`, \`TRN\_TaxLiability\`, \`TRN\_StatutoryPayment\` |

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0025 |

| \*\*Business Term\*\* | GST \(Goods and Services Tax\) |

| \*\*Preferred ODOS Term\*\* | GST |

| \*\*Synonyms\*\* | Value Added Tax \(VAT\), Sales Tax, Indirect Tax |

| \*\*Business Definition\*\* | A multi\-stage, destination\-based tax levied on the supply of goods and services |

| \*\*Business Importance\*\* | Delayed or incorrect GST filing can lead to penalties |

| \*\*Related ERD Entities\*\* | \`RUL\_GSTRule\`, \`TRN\_TaxLiability\`, \`TRN\_StatutoryPayment\` |

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0026 |

| \*\*Business Term\*\* | Working Capital |

| \*\*Preferred ODOS Term\*\* | Working Capital |

| \*\*Synonyms\*\* | Operating Liquidity, Cash Gap, Funding Requirement |

| \*\*Business Definition\*\* | The financial resources required to fund the day\-to\-day operations |

| \*\*Business Importance\*\* | Poor working capital management is the single biggest reason many DSAs struggle with cash flow |

| \*\*Related ERD Entities\*\* | \`BI\_PortfolioRiskSnapshot\`, \`TRN\_Case\` |

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0027 |

| \*\*Business Term\*\* | Cash Conversion Cycle \(CCC\) |

| \*\*Preferred ODOS Term\*\* | Cash Conversion Cycle |

| \*\*Synonyms\*\* | Cash Cycle, Operating Cycle, Collection Cycle |

| \*\*Business Definition\*\* | The time period between disbursing a loan and receiving the commission payment |

| \*\*Business Importance\*\* | The CCC directly impacts the DSA's profitability |

| \*\*Related ERD Entities\*\* | \`TRN\_Case\` \(DisbursementDate, InvoiceGeneratedDate, InvoiceDueDate, PaymentReceivedDate\) |

\#\#\#\# 6\.3\.6 Data Governance & ETL

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0028 |

| \*\*Business Term\*\* | Master Data |

| \*\*Preferred ODOS Term\*\* | Master Data |

| \*\*Synonyms\*\* | Reference Data, Core Entity Data, Golden Records |

| \*\*Business Definition\*\* | The core business entities that remain relatively stable over time and are referenced by multiple transactions |

| \*\*Business Importance\*\* | Poor master data quality leads to inconsistent reporting |

| \*\*Related ERD Entities\*\* | All \`MST\_\*\` tables |

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0029 |

| \*\*Business Term\*\* | Transaction Data |

| \*\*Preferred ODOS Term\*\* | Transaction Data |

| \*\*Synonyms\*\* | Operational Data, Business Events, Activity Data |

| \*\*Business Definition\*\* | Data generated from operational business events |

| \*\*Business Importance\*\* | Transaction Data is the heart of the DSA's operational and financial records |

| \*\*Related ERD Entities\*\* | All \`TRN\_\*\` tables |

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0030 |

| \*\*Business Term\*\* | Metadata |

| \*\*Preferred ODOS Term\*\* | Metadata |

| \*\*Synonyms\*\* | Data about Data, Configuration Data, System Definition Data |

| \*\*Business Definition\*\* | Data that defines the structure, meaning, relationships, and governance of other data |

| \*\*Business Importance\*\* | Metadata is the brain of ODOS |

| \*\*Related ERD Entities\*\* | All \`META\_\*\` tables |

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0031 |

| \*\*Business Term\*\* | Data Lineage |

| \*\*Preferred ODOS Term\*\* | Data Lineage |

| \*\*Synonyms\*\* | Data Provenance, Data Traceability, Source\-to\-Target Mapping |

| \*\*Business Definition\*\* | The complete historical record of a piece of data's journey from its original source into ODOS |

| \*\*Business Importance\*\* | Data Lineage is mandatory for financial reconciliation and regulatory audits |

| \*\*Related ERD Entities\*\* | \`ETL\_DataLineage\` |

\#\#\#\# 6\.3\.7 Artificial Intelligence & Learning

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0032 |

| \*\*Business Term\*\* | AI Mapping |

| \*\*Preferred ODOS Term\*\* | AI Mapping |

| \*\*Synonyms\*\* | Smart Mapping, Auto\-Mapping, Intelligent Field Mapping |

| \*\*Business Definition\*\* | The process by which ODOS's AI engine suggests or automatically applies the mapping of an external source column to an internal ODOS field |

| \*\*Business Importance\*\* | AI Mapping directly improves the efficiency and accuracy of data ingestion |

| \*\*Related ERD Entities\*\* | \`AI\_Mapping\`, \`AI\_Learning\`, \`AI\_Feedback\` |

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0033 |

| \*\*Business Term\*\* | Confidence Score |

| \*\*Preferred ODOS Term\*\* | Confidence Score |

| \*\*Synonyms\*\* | Certainty Score, Probability Score, Confidence Level |

| \*\*Business Definition\*\* | A numerical value \(0\.0 to 1\.0\) assigned by the AI engine to indicate its level of certainty in a specific recommendation |

| \*\*Business Importance\*\* | Confidence Scores enable Human\-in\-the\-Loop governance |

| \*\*Related ERD Entities\*\* | \`AI\_Mapping\`, \`AI\_Learning\`, \`ETL\_DuplicateQueue\` |

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*Glossary ID\*\* | BG\-0034 |

| \*\*Business Term\*\* | AI Feedback |

| \*\*Preferred ODOS Term\*\* | AI Feedback |

| \*\*Synonyms\*\* | User Correction, Training Input, Learning Signal |

| \*\*Business Definition\*\* | Explicit input provided by a user to accept, reject, or correct an AI recommendation |

| \*\*Business Importance\*\* | AI Feedback is the mechanism through which the system improves over time |

| \*\*Related ERD Entities\*\* | \`AI\_Feedback\`, \`AI\_Learning\` |

\-\-\-

\#\# 7\. Database Standards Manual

\#\#\# 7\.1 Purpose

This manual establishes the \*\*authoritative implementation standards\*\* for all ODOS database development\. It defines \*how\* the approved data model is implemented—not \*what\* the model contains\.

The manual ensures consistency, maintainability, scalability, auditability, and portability across all current and future database platforms\.

\#\#\# 7\.2 Document Scope & Governance

| Aspect | Standard |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|

| \*\*Document Type\*\* | Implementation Standard |

| \*\*Version\*\* | 1\.0 |

| \*\*Status\*\* | Approved / Frozen |

| \*\*Owner\*\* | CTO |

| \*\*Applicability\*\* | All ODOS database development, DDL generation, ETL design, API development, AI implementation, reporting, and future platform evolution |

\#\#\# 7\.3 Enterprise Naming Standards

| Object | Format | Example |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|

| \*\*Table\*\* | \`Prefix\_EntityName\` | \`TRN\_Case\`, \`MST\_Lender\` |

| \*\*Field\*\* | PascalCase | \`DisbursementAmount\` |

| \*\*Primary Key\*\* | \`EntityNameID\` | \`CaseID\`, \`LenderID\` |

| \*\*Foreign Key\*\* | \`ReferencedEntityNameID\` | \`CustomerID\`, \`LenderID\` |

| \*\*Index\*\* | \`IDX\_TableName\_FieldName\` | \`IDX\_TRN\_Case\_DisbursementDate\` |

| \*\*View\*\* | \`VW\_EntityName\_Aggregation\` | \`VW\_BranchProfitability\` |

\#\#\# 7\.4 Data Type Standards

| Logical Type | SQLite | PostgreSQL | SQL Server | Use Case |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|

| \*\*ID\*\* | \`INTEGER\` \(Auto\-increment\) | \`SERIAL\` / \`BIGSERIAL\` | \`INT IDENTITY\(1,1\)\` | Surrogate primary keys |

| \*\*Code\*\* | \`VARCHAR\(50\)\` | \`VARCHAR\(50\)\` | \`VARCHAR\(50\)\` | Short alphanumeric identifiers |

| \*\*Name\*\* | \`VARCHAR\(255\)\` | \`VARCHAR\(255\)\` | \`VARCHAR\(255\)\` | Short descriptions |

| \*\*Description\*\* | \`VARCHAR\(1000\)\` | \`VARCHAR\(1000\)\` | \`VARCHAR\(1000\)\` | Medium textual descriptions |

| \*\*Text\*\* | \`TEXT\` | \`TEXT\` | \`VARCHAR\(MAX\)\` | Large free\-text |

| \*\*JSON\*\* | \`JSON\` \(TEXT\) | \`JSONB\` | \`NVARCHAR\(MAX\)\` \(JSON\) | Structured data |

| \*\*Amount\*\* | \`NUMERIC\(18,4\)\` | \`NUMERIC\(18,4\)\` | \`DECIMAL\(18,4\)\` | Monetary values |

| \*\*Rate\*\* | \`NUMERIC\(10,4\)\` | \`NUMERIC\(10,4\)\` | \`DECIMAL\(10,4\)\` | Percentages |

| \*\*Boolean\*\* | \`BOOLEAN\` | \`BOOLEAN\` | \`BIT\` | True/False values |

| \*\*Date\*\* | \`DATE\` | \`DATE\` | \`DATE\` | Calendar dates |

| \*\*DateTime\*\* | \`DATETIME\` | \`TIMESTAMP\` | \`DATETIME2\` | UTC timestamps |

\#\#\# 7\.5 Key & Relationship Standards

| Standard | Description |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \*\*Surrogate Keys\*\* | Every table must have a surrogate primary key |

| \*\*Natural Keys\*\* | Natural keys must be stored as \*\*unique constraints\*\* |

| \*\*Composite Keys\*\* | Only for junction tables \(Many\-to\-Many\) |

| \*\*Foreign Keys\*\* | Must be defined on the parent table |

\#\#\# 7\.6 Audit & Governance Standards

Every table in ODOS \*\*must\*\* include the 16 standard audit fields defined in Section 4\.5\.

\#\#\# 7\.7 Multi\-Tenancy Standards

| Standard | Description |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \*\*CompanyID\*\* | Every tenant\-owned table must contain a \`CompanyID\` column |

| \*\*REF\_ Tables\*\* | Do \*\*not\*\* contain \`CompanyID\` \(shared reference data\) |

| \*\*Tenant Filtering\*\* | All queries must filter by \`CompanyID\` |

\-\-\-

\#\# 8\. Reference Data Catalogue

\#\#\# 8\.1 Purpose

This section defines the complete inventory of reference data domains used across the ODOS platform\.

\#\#\# 8\.2 Reference Data Domains

| Domain | Description | Examples |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|

| \*\*Geography\*\* | Geographic reference data | Country, State, District, City, Pincode |

| \*\*Demographic\*\* | Demographic reference data | Gender, Marital Status, Occupation, Industry |

| \*\*Financial\*\* | Financial reference data | Currency, Loan Purpose, Property Type |

| \*\*Document\*\* | Document reference data | Document Type, Address Type |

| \*\*Operational\*\* | Operational reference data | Expense Category, Expense Type, Payment Status |

| \*\*Administrative\*\* | Administrative reference data | Priority, Status, Frequency, Claim Status |

| \*\*Tax\*\* | Tax reference data | TDS Section, GST Category |

\#\#\# 8\.3 Reference Data Domains

\#\#\#\# 8\.3\.1 REF\_State

| Field Name | Logical Type | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \`StateID\` | ID | Surrogate primary key |

| \`StateCode\` | Code \(5\) | State code \(e\.g\., MH, KA\) |

| \`StateName\` | Name \(100\) | State name |

| \`CountryID\` | ID | Foreign key to REF\_Country |

\#\#\#\# 8\.3\.2 REF\_DocumentType

| Field Name | Logical Type | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \`DocumentTypeID\` | ID | Surrogate primary key |

| \`DocumentTypeCode\` | Code \(20\) | Document type code |

| \`DocumentTypeName\` | Name \(100\) | Document type name |

| \`IsKYC\` | Boolean | Is this a KYC document? |

\*\*Values:\*\*

\- PAN

\- Aadhaar

\- ITR \(Income Tax Return\)

\- Bank Statement

\- Salary Slip

\- Sanction Letter

\- Agreement

\- Invoice

\- GST Certificate

\- Address Proof

\#\#\#\# 8\.3\.3 REF\_TDSSection

| Field Name | Logical Type | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \`TDSSectionID\` | ID | Surrogate primary key |

| \`SectionCode\` | Code \(10\) | TDS section code \(e\.g\., 194A, 194C\) |

| \`SectionName\` | Name \(100\) | Section name |

| \`DefaultRate\` | Rate | Default TDS rate |

| \`ThresholdAmount\` | Amount | Threshold for TDS applicability |

\*\*Values:\*\*

\- 194A – Interest

\- 194C – Contractors

\- 194H – Commission

\- 194I – Rent

\- 194J – Professional Fees

\- 194M – Payments to Individuals

\#\#\#\# 8\.3\.4 REF\_GSTCategory

| Field Name | Logical Type | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \`GSTCategoryID\` | ID | Surrogate primary key |

| \`CategoryCode\` | Code \(10\) | GST category code |

| \`CategoryName\` | Name \(100\) | GST category name |

| \`Rate\` | Rate | GST rate \(%\) |

| \`IsReverseCharge\` | Boolean | Is reverse charge applicable? |

\*\*Values:\*\*

\- 5% – Standard

\- 12% – Standard

\- 18% – Standard

\- 28% – Standard

\- 0% – Exempt

\- Reverse Charge

\#\#\#\# 8\.3\.5 REF\_PaymentStatus

| Field Name | Logical Type | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \`PaymentStatusID\` | ID | Surrogate primary key |

| \`StatusCode\` | Code \(20\) | Status code |

| \`StatusName\` | Name \(50\) | Status name |

\*\*Values:\*\*

\- Pending

\- In Progress

\- Completed

\- Failed

\- Rejected

\- Reconciled

\-\-\-

\#\# 9\. Data Model Gap Analysis & Resolution Register

\#\#\# 9\.1 Purpose

This section documents all identified gaps in the data model and provides their resolution status\.

\#\#\# 9\.2 Gap Resolution Register

| ID | Area | Gap Description | Impact | Status | Resolution |

|\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|

| \*\*DM\-001\*\* | MDM | Master versioning framework not fully defined | Medium | ✅ Resolved | Added to Database Standards |

| \*\*DM\-002\*\* | Reference Data | Soft delete for reference tables missing | Medium | ✅ Resolved | Added \`IsDeleted\` to all REF\_ tables |

| \*\*DM\-003\*\* | Performance | Indexing strategy not documented | High | ✅ Resolved | Added to Database Standards |

| \*\*DM\-004\*\* | Performance | Partitioning strategy not documented | High | ✅ Resolved | Added to Database Standards |

| \*\*DM\-005\*\* | Audit | Document expiry workflow missing | Medium | ✅ Resolved | Added to AUD\_Document specification |

| \*\*DM\-006\*\* | ETL | Rollback procedure not documented | High | ✅ Resolved | Added to ETL\_ImportBatch specification |

| \*\*DM\-007\*\* | Financial | Bulk payment processing not supported | Medium | ✅ Resolved | Added \`PaymentBatchID\` to TRN\_Payment |

| \*\*DM\-008\*\* | Security | Field\-level masking not fully defined | High | ✅ Resolved | Added to META\_FieldDefinition |

| \*\*DM\-009\*\* | Security | Row\-level security not fully defined | High | ✅ Resolved | Added to SEC\_User |

| \*\*DM\-010\*\* | AI | Mapping rationale not captured | Medium | ✅ Resolved | Added to AI\_Mapping |

| \*\*DM\-011\*\* | Reporting | Snapshot retention strategy not defined | Medium | ✅ Resolved | Added to BI\_ specifications |

| \*\*DM\-012\*\* | Governance | Master data ownership not fully defined | Medium | ✅ Resolved | Added to MST\_ specifications |

\-\-\-

\#\# 10\. Document Status & Approval

\#\#\# 10\.1 Document Status

| Status | Approved / Frozen |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \*\*Version\*\* | 1\.0 |

| \*\*Date\*\* | July 2026 |

| \*\*Next Review\*\* | Annual or before major architectural change |

| \*\*Owner\*\* | CTO |

\#\#\# 10\.2 Document Freeze Notice

\*\*This document is designated as an Architecture Baseline Artefact\.\*\*

\*\*Following approval:\*\*

\- Structural changes to the Canonical Enterprise Data Model require a new Architecture Decision Record \(ADR\)\.

\- Structural changes to the Data Dictionary require Architecture Review Board \(ARB\) approval\.

\- All DDL generation shall use this document as the governing data model baseline\.

\- All implementation teams shall treat this document as frozen unless superseded by a formally approved revision\.

\*\*Freeze Status:\*\* ✅ \*\*FROZEN\*\*

\#\#\# 10\.3 Approval Sign\-Off

| Role | Name | Signature | Date |

|\-\-\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-|

| Enterprise Architect | Architecture Review Board | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

| Data Architect | \_\[Name\]\_ | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

| CTO | \_\[ChatGPT\]\_ | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

| Technical Programme Manager | \_\[DeepSeek\]\_ | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

| Development Lead | \_\[Aniket\]\_ | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

| Business Owner | \_\[Name\]\_ | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

\#\#\# 10\.4 Cross\-Reference to Repository Documents

| Document | Relationship |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| DOC\-000 | Repository structure referencing this document |

| DOC\-001 | Repository guide referencing this document |

| DOC\-002 | Dependency matrix including this document |

| DOC\-003 | Master index including this document |

| DOC\-010 | Architecture & ADRs referencing this document |

| DOC\-012 | Platform Engineering Standards referencing database standards |

| DOC\-013 | Application Development Standards referencing data model |

| DOC\-014 | Finance & Operations Specifications referencing transaction tables |

| DOC\-015 | AI & Data Engineering referencing ETL tables |

| DOC\-017 | Core Module Specifications referencing data model |

| DOC\-018 | Business Module Specifications referencing data model |

\-\-\-

\#\# End of Document

\*\*Document ID:\*\* DOC\-011  

\*\*Document Name:\*\* \*Canonical Enterprise Data Model & Data Dictionary Consolidated\*  

\*\*Version:\*\* 1\.0  

\*\*Status:\*\* Approved / Frozen  

\*\*Owner:\*\* CTO

