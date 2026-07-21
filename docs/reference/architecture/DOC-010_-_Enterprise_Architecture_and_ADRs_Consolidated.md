# DOC-010 – Enterprise Architecture & ADRs Consolidated

\# DOC\-010 – Enterprise Architecture & ADRs Consolidated

\*\*Document ID:\*\* DOC\-010  

\*\*Version:\*\* 1\.0  

\*\*Status:\*\* Approved / Frozen  

\*\*Owner:\*\* CTO \(ChatGPT\)  

\*\*Classification:\*\* Enterprise Architecture Foundation  

\*\*Purpose:\*\* Define the complete enterprise architecture foundation, including architecture principles, industry\-agnostic core design, cross\-cutting concerns, and all approved Architecture Decision Records \(ADR\-001 to ADR\-018\), along with comprehensive gap analysis and addendum\.

\-\-\-

\#\# Table of Contents

1\. Executive Summary

2\. Enterprise Architecture Principles

3\. Industry\-Agnostic Core Architecture

4\. Enterprise Foundation & Cross\-Cutting Concerns

5\. Architecture Decision Records \(ADR\-001 to ADR\-018\)

6\. Architecture Gap Analysis & Resolution Register

7\. Architecture Addendum – Industry\-Agnostic Core & Configurable Industry Layer

8\. Document Status & Approval

\-\-\-

\#\# 1\. Executive Summary

\#\#\# 1\.1 Purpose of This Document

This document consolidates the complete enterprise architecture foundation for the ODOS Enterprise Platform\. It brings together:

\- \*\*Architecture Principles\*\* – The non\-negotiable rules governing all design decisions

\- \*\*Industry\-Agnostic Core Architecture\*\* – The immutable platform foundation

\- \*\*Cross\-Cutting Concerns\*\* – Shared architectural services applicable across all modules

\- \*\*Architecture Decision Records \(ADR\-001 to ADR\-018\)\*\* – The complete rationale for every major architectural decision

\- \*\*Gap Analysis & Resolution\*\* – Identified gaps and their resolution status

\- \*\*Architecture Addendum\*\* – Industry\-agnostic core design principles

\#\#\# 1\.2 The ODOS Platform Philosophy

ODOS is not a software application\. ODOS is an \*\*Enterprise Operating Platform\*\*\.

Its objective is to become the digital operating system for organisations involved in financial intermediation and, ultimately, any enterprise requiring configurable business processes, workflow automation, data governance, analytics, and AI\-assisted operations\.

\*\*Key Philosophy:\*\*

\- \*\*Configuration over Customisation\*\* – Industry\-specific behaviour through metadata and configuration

\- \*\*Metadata before Code\*\* – Business logic driven by metadata wherever possible

\- \*\*AI as Co\-worker\*\* – AI assists, humans remain accountable

\- \*\*Data as Strategic Asset\*\* – Every data point preserved, governed, and traceable

\#\#\# 1\.3 Scope

This document covers:

| Area | Coverage |

|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|

| Architecture Principles | All 16 principles |

| Industry\-Agnostic Core | Complete core engine definition |

| Cross\-Cutting Concerns | All shared services |

| Architecture Decisions | ADR\-001 to ADR\-018 |

| Gap Analysis | Identified gaps and resolutions |

| Addendum | Industry\-agnostic design patterns |

\#\#\# 1\.4 Relationship to Other Repository Documents

| Document | Relationship |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| DOC\-000 to DOC\-009 | Governance framework referencing this document |

| DOC\-011 | Data Model \(CEDM, ERD, Data Dictionary\) |

| DOC\-012 | Platform Engineering Standards |

| DOC\-013 | Application Development Standards |

| DOC\-014 | Finance & Operations Specifications |

| DOC\-015 | AI & Data Engineering Specifications |

| DOC\-016 | Security & Governance Specifications |

| DOC\-017 | Core Module Specifications |

| DOC\-018 | Business Module Specifications |

| DOC\-019 | Reporting & Analytics Specification |

| DOC\-020 | Templates |

\#\#\# 1\.5 Document Status

| Status | Approved / Frozen |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \*\*Version\*\* | 1\.0 |

| \*\*Date\*\* | July 2026 |

| \*\*Next Review\*\* | Annual or before major architectural change |

| \*\*Owner\*\* | CTO |

\-\-\-

\#\# 2\. Enterprise Architecture Principles

\#\#\# 2\.1 Purpose

These principles establish the fundamental architectural philosophy of ODOS\. They represent the non\-negotiable design rules that guide all future development, enhancements, integrations, and product evolution\.

These principles have been established after careful evaluation of business requirements, enterprise architecture best practices, and the long\-term vision of transforming ODOS from an internal DSA operating platform into a configurable commercial enterprise solution\.

Unless formally superseded through the Architecture Governance process, these principles shall remain valid throughout the lifecycle of ODOS\.

\#\#\# 2\.2 Principle 1 – Single Source of Truth \(SSOT\)

Every business entity and every business fact shall exist only once within the system\.

\*\*Implications:\*\*

\- One Customer record

\- One Lender record

\- One Product definition

\- One Employee record

\- One Chart of Accounts

\- One Commission Rule

\- One Configuration value

\*\*Governance:\*\*

\- Duplicate storage of business information shall be avoided unless specifically required for historical snapshots, auditing, reporting, or performance optimization\.

\- Master data shall always be maintained in its designated master tables\.

\- Transactional data shall reference master records through defined relationships\.

\#\#\# 2\.3 Principle 2 – Metadata\-Driven Architecture

Business behaviour shall be controlled through metadata rather than hardcoded application logic wherever practical\.

\*\*Metadata shall govern:\*\*

\- Field definitions

\- Table definitions

\- Import templates

\- Excel mappings

\- Validation rules

\- Business rules

\- Report definitions

\- Dashboard definitions

\- Workflow configurations

\- AI learning mappings

\- Data lineage definitions

\- Data quality definitions

\*\*Application code shall interpret metadata at runtime\*\* to execute configurable business processes\.

\*\*Implications:\*\*

\- New lenders, products, reports, or import formats should be introduced through configuration rather than software changes\.

\- Application code shall contain no organisation\-specific business logic\.

\#\#\# 2\.4 Principle 3 – Configuration over Hardcoding

Business policies, calculations, workflows, numbering schemes, tax rules, commission structures, and operational parameters shall be configurable\.

\*\*Rules:\*\*

\- No lender\-specific, branch\-specific, or company\-specific business logic shall be embedded directly within application code unless approved as an architectural exception\.

\- Configuration tables shall always take precedence over hardcoded values\.

\*\*Scope of Configuration:\*\*

\- Commission structures

\- Incentive schemes

\- GST and TDS rules

\- Workflow stages

\- Approval hierarchies

\- Validation rules

\- Financial year settings

\- Auto\-numbering

\- Calendar and holiday definitions

\- Lender agreements

\- Import templates

\- Dashboard parameters

\- Report definitions

\#\#\# 2\.5 Principle 4 – ETL\-First Data Processing

All external data entering ODOS shall pass through the ETL pipeline before reaching operational tables\.

\*\*Standard Processing Sequence:\*\*

\`\`\`

External Source

        ↓

Raw Staging

        ↓

Validation

        ↓

Duplicate Detection

        ↓

Business Rules

        ↓

Approval

        ↓

Master & Transaction Tables

\`\`\`

\*\*Rules:\*\*

\- Direct updates from external files to operational tables are strictly prohibited\.

\- No dashboard, report, KPI, forecast, or AI model shall consume unvalidated staging data\.

\#\#\# 2\.6 Principle 5 – AI\-Assisted, Human\-Governed Processing

Artificial Intelligence shall assist users in improving productivity but shall not replace human accountability for critical business decisions\.

\*\*AI May:\*\*

\- Recommend mappings

\- Detect anomalies

\- Suggest duplicate records

\- Classify documents

\- Generate insights

\- Learn user behaviour

\*\*AI Shall Not:\*\*

\- Approve financial postings

\- Merge master records automatically

\- Delete operational records

\- Override business rules

\- Modify approved transactions

\*\*Final approval for business\-critical actions\*\* shall remain under authorised user control\.

\#\#\# 2\.7 Principle 6 – Audit by Design

Every significant business transaction shall be traceable\.

\*\*The system shall maintain complete auditability for:\*\*

\- Data creation

\- Data modification

\- Data deletion \(logical\)

\- Imports

\- User actions

\- Business rule execution

\- AI recommendations

\- Financial transactions

\*\*Rules:\*\*

\- Audit capability shall be designed into the architecture rather than added later\.

\- Historical information shall never be silently overwritten\.

\- Approved financial transactions shall never be physically modified or deleted\.

\#\#\# 2\.8 Principle 7 – Financial Integrity

Financial information shall always be complete, traceable, and reconcilable\.

\*\*Scope:\*\*

\- Revenue

\- Commissions

\- Expenses

\- Taxes

\- Incentives

\- Invoices

\- Payments

\- Working capital calculations

\*\*Rules:\*\*

\- Revenue, commission, expenses, invoices, payments, taxes, working capital, and profitability shall remain internally consistent\.

\- Historical financial transactions shall never be modified after approval\.

\- Corrections shall be performed through adjustment entries\.

\#\#\# 2\.9 Principle 8 – Multi\-Tenant by Design

The architecture shall support multiple organisations operating independently within the same application framework\.

\*\*Rules:\*\*

\- Company\-specific data shall remain logically isolated\.

\- Shared metadata where appropriate\.

\- Centralised product maintenance\.

\- Future commercialisation shall not require structural redesign of the database\.

\*\*Scope:\*\*

\- All MST\_, TRN\_, ETL\_, BI\_ tables shall contain CompanyID\.

\- REF\_ tables are shared and do not contain CompanyID\.

\#\#\# 2\.10 Principle 9 – Extensibility without Structural Redesign

The architecture shall support future business expansion without requiring database redesign\.

\*\*Mechanisms:\*\*

\- Metadata

\- Configuration

\- Reference data

\- Business rules

\- Plugin modules

\- Version\-controlled enhancements

\*\*Scope:\*\*

\- New lenders

\- New products

\- New workflows

\- New reports

\- New integrations

\#\#\# 2\.11 Principle 10 – Security and Privacy by Design

Security shall be incorporated into the architecture from the outset\.

\*\*The platform shall support:\*\*

\- Authentication

\- Authorization

\- Role\-based access control

\- Audit logging

\- Sensitive data classification

\- Data masking

\- Encryption where required

\- Regulatory compliance

\- Protection of customer and financial information

\#\#\# 2\.12 Principle 11 – Analytics by Design

Operational data shall be structured to support reporting, dashboards, forecasting, profitability analysis, and AI without requiring redesign\.

\*\*The architecture shall facilitate:\*\*

\- Historical analysis

\- Trend reporting

\- KPI measurement

\- Multidimensional business intelligence across:

  \- Customers

  \- Lenders

  \- Products

  \- Branches

  \- Teams

  \- Employees

  \- Financial performance

\#\#\# 2\.13 Principle 12 – Architecture Governance

All future structural changes shall be governed through formal architecture management\.

\*\*Any modification affecting:\*\*

\- Database schema

\- Core business entities

\- Relationships

\- Metadata framework

\- Financial model

\- Security architecture

\- ETL architecture

\*\*Shall require:\*\*

\- Business justification

\- Impact assessment

\- Architecture review

\- Approval through the Architecture Decision Register \(ADR\)

\- Version\-controlled implementation

\#\#\# 2\.14 Principle 13 – Enterprise Product Mindset

ODOS shall be designed as a reusable enterprise platform rather than a bespoke internal application\.

\*\*All architectural decisions shall consider:\*\*

\- Future deployment across multiple DSAs

\- Additional financial products

\- Evolving regulatory requirements

\- Integration with external ecosystems

\#\#\# 2\.15 Principle 14 – Modular Architecture

The platform shall be composed of loosely coupled modules with clearly defined responsibilities\.

\*\*Rules:\*\*

\- Each module shall evolve independently\.

\- Enterprise consistency preserved through shared metadata, master data, and governance standards\.

\#\#\# 2\.16 Principle 15 – Explainability and Transparency

Every automated decision shall be understandable\.

\*\*Users shall be able to determine:\*\*

\- Why a mapping was selected

\- Why a duplicate was identified

\- How a commission was calculated

\- Why a validation failed

\- How a KPI was derived

\*\*No business\-critical decision shall rely upon opaque logic\.\*\*

\#\#\# 2\.17 Principle 16 – Industry\-Agnostic by Design

The Core Engine shall remain independent of any single industry\. All industry\-specific logic shall be implemented through metadata, configuration, and business rules\.

\*\*The platform must be capable of supporting a new industry vertical with zero code changes to the Core Engine\.\*\*

\#\#\# 2\.18 Principle Summary Table

| \# | Principle | Key Constraint |

|\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| 1 | Single Source of Truth | One authoritative record per entity |

| 2 | Metadata\-Driven Architecture | Behaviour controlled by metadata |

| 3 | Configuration over Hardcoding | No hardcoded business logic |

| 4 | ETL\-First Data Processing | All data through ETL pipeline |

| 5 | AI\-Assisted, Human\-Governed | Human approval for critical decisions |

| 6 | Audit by Design | Every transaction traceable |

| 7 | Financial Integrity | Immutable financial records |

| 8 | Multi\-Tenant by Design | CompanyID isolation |

| 9 | Extensibility without Redesign | Configurable, not customised |

| 10 | Security and Privacy by Design | Security embedded |

| 11 | Analytics by Design | Data structured for analysis |

| 12 | Architecture Governance | Formal change management |

| 13 | Enterprise Product Mindset | Platform, not application |

| 14 | Modular Architecture | Loose coupling, high cohesion |

| 15 | Explainability and Transparency | Decisions understandable |

| 16 | Industry\-Agnostic by Design | Zero code changes for new industries |

\-\-\-

\#\# 3\. Industry\-Agnostic Core Architecture

\#\#\# 3\.1 Purpose

This section defines the architectural boundary between the reusable, immutable enterprise \*\*Core Engine\*\* and the configurable \*\*Industry\-Specific Layer\*\*\.

This ensures ODOS remains an enterprise platform capable of serving multiple industries \(DSA, MSME Lending, Manufacturing, Insurance Distribution, etc\.\) with minimal reconfiguration effort\.

\#\#\# 3\.2 Executive Summary

The ODOS platform is not a bespoke DSA application\. It is an \*\*Enterprise Operating Platform\*\* designed for \*\*loan distribution, financial intermediation, and general business operations\*\*\.

The architecture is intentionally split into two distinct layers:

| Layer | Nature | Reusability | Change Required for New Industry |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \*\*Core Engine\*\* | Immutable Enterprise Foundation | 100% | None |

| \*\*Configurable Layer\*\* | Industry\-Specific Configuration | 10\-30% \(Configuration\) | Metadata, Reference Data, Rules, Workflows, Reports |

\*\*Target:\*\* Spin up a new industry vertical \(e\.g\., MSME Lending, Manufacturing, Insurance\) with \*\*2\-4 weeks of configuration\*\*, \*\*zero code changes\*\* to the Core Engine\.

\#\#\# 3\.3 The Core Engine \(Immutable – 100% Reusable\)

The Core Engine is the \*\*enterprise operating system\*\* that remains identical regardless of the industry\. It cannot be changed or customised at the code level\. Customisation is achieved through metadata and configuration\.

| Component | Purpose | Reusability |

|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \*\*Multi\-Tenancy \(MST\_Company\)\*\* | Tenant isolation | ✅ 100% |

| \*\*Universal Party Model \(MST\_Party\)\*\* | Unified entity for Customers, Employees, Partners, Vendors, Suppliers | ✅ 100% |

| \*\*Security & RBAC \(SEC\_\)\*\* | Authentication, Authorization, Permissions, Audit | ✅ 100% |

| \*\*Audit & Lineage \(SEC\_AuditTrail, ETL\_DataLineage\)\*\* | Complete traceability and compliance | ✅ 100% |

| \*\*Metadata Engine \(META\_\)\*\* | Dynamic schema, validation, and UI generation | ✅ 100% |

| \*\*Configuration Engine \(CFG\_\)\*\* | Enterprise settings, feature toggles, numbering | ✅ 100% |

| \*\*ETL Pipeline \(ETL\_\)\*\* | Data ingestion, validation, staging, transformation, lineage | ✅ 100% |

| \*\*AI Mapping & Learning \(AI\_\)\*\* | Automated mapping, learning, and recommendations | ✅ 100% |

| \*\*Rule Engine \(RUL\_ – Framework\)\*\* | Configurable business rules \(the execution engine\) | ✅ 100% |

| \*\*Workflow Engine \(RUL\_Workflow – Framework\)\*\* | State management and process orchestration | ✅ 100% |

| \*\*Notification Engine \(TRN\_Notification\)\*\* | Omnichannel communication | ✅ 100% |

| \*\*Document Management \(AUD\_\)\*\* | Storage, OCR, versioning, lifecycle | ✅ 100% |

| \*\*General Ledger & Payments \(TRN\_Payment, TRN\_Invoice, TRN\_Expense\)\*\* | Universal financial operations | ✅ 100% |

| \*\*Tax Compliance \(RUL\_GSTRule, RUL\_TDSRule\)\*\* | Universal taxation framework | ✅ 100% |

| \*\*Database Abstraction & APIs\*\* | The API gateway and database access layer | ✅ 100% |

| \*\*Deployment & Infrastructure\*\* | DevOps, CI/CD, security, monitoring | ✅ 100% |

\#\#\# 3\.4 The Configurable Layer \(Industry\-Specific – 10\-30% Configuration\)

This layer is \*\*100% metadata and configuration driven\*\*\. No code changes are required to switch industries\.

All changes are applied through:

\- Reference Data \(\`REF\_\` tables\)

\- Metadata \(\`META\_FieldDefinition\`, \`META\_TableDefinition\`\)

\- Rules \(\`RUL\_\` tables\)

\- Workflows \(\`RUL\_Workflow\`\)

\- Seed Data

\- Configuration \(\`CFG\_\`\)

\- Report Definitions \(\`META\_ReportDefinition\`, \`BI\_KPI\`\)

\#\#\#\# 3\.4\.1 Configuration by Industry

| Component | DSA Configuration | Manufacturing Configuration | MSME Lending Configuration |

|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \*\*Party Types \(\`REF\_PartyType\`\)\*\* | Customer, Connector, Employee, Lender, Vendor | Customer, Supplier, Employee, Manufacturer, Distributor, Retailer, Vendor | Customer, MSME, Employee, Lender, Vendor |

| \*\*Product Model \(\`MST\_Product\`\)\*\* | Loan Products \(Home Loan, LAP, Personal Loan\) | Raw Material, Finished Goods, Spare Parts, Services | Working Capital, Equipment Finance, Invoice Discounting |

| \*\*Product Attributes \(\`META\_FieldDefinition\`\)\*\* | MinLoanAmount, MaxLoanAmount, InterestRate, ProcessingFee | UnitOfMeasure, Weight, Dimensions, MinOrderQuantity, LeadTime, ManufacturingCost | BusinessVintage, AnnualTurnover, CollateralType, GSTIN |

| \*\*Transaction Tables \(\`TRN\_\`\)\*\* | TRN\_Case, TRN\_Revenue, TRN\_Commission, TRN\_Disbursement | TRN\_Order, TRN\_PurchaseOrder, TRN\_ProductionRun, TRN\_Inventory, TRN\_Shipment | TRN\_Case \(with additional metadata for business loans\) |

| \*\*Workflow \(\`RUL\_Workflow\`\)\*\* | Lead → Application → Sanction → Disbursement → Closure | Sales Order → Production Planning → Procurement → Manufacturing → Dispatch → Invoicing | Lead → Application → Underwriting → Sanction → Disbursement → Collection |

| \*\*Rules \(\`RUL\_\`\)\*\* | Commission Rules, GST/TDS, Validation | Pricing Rules, Discount Rules, Inventory Rules, Quality Rules, Production Rules | Risk Scoring Rules, Pricing Rules, GST/TDS, Validation |

| \*\*Reference Data \(\`REF\_\`\)\*\* | LoanPurpose, PropertyType, Occupation | Industry, MaterialType, UnitOfMeasure, QualityStatus, ProductionStatus | LoanPurpose, Industry, BusinessType, CollateralType |

| \*\*KPIs \(\`BI\_KPI\`\)\*\* | Revenue, Profit, TAT, Conversion, Connector Performance | Production Efficiency, Inventory Turnover, On\-Time Delivery Rate, Quality Pass Rate | Disbursement Volume, NPA Rate, Portfolio Yield, Collection Efficiency |

| \*\*Document Types \(\`REF\_DocumentType\`\)\*\* | PAN, Aadhaar, ITR, Bank Statement, Sanction Letter | GST Certificate, Company Registration, Purchase Order, Invoice, Quality Certificate | GSTIN, Audited Financials, Bank Statement, Board Resolution |

\#\#\# 3\.5 The Separation Boundary

The Core Engine exposes a \*\*Canonical API\*\* and a \*\*Metadata\-Driven Configuration Interface\*\*\.

\`\`\`

┌──────────────────────┐      ┌──────────────────────┐      ┌──────────────────────┐

│     Industry         │      │     Industry         │      │     Core Engine      │

│     Configuration    │ \-\-\-> │     Metadata &       │ \-\-\-> │     \(100% Reusable\)  │

│     \(DSA/MSME/Man\)   │      │     Rules            │      │                      │

└──────────────────────┘      └──────────────────────┘      └──────────────────────┘

\`\`\`

\*\*Interaction Flow:\*\*

1\. \*\*Industry Configuration\*\* is loaded at startup via seed data and metadata\.

2\. \*\*All business logic\*\* is evaluated by the Core Engine's Rule Engine, which reads the industry\-specific rules from the \`RUL\_\` tables\.

3\. \*\*All workflows\*\* are executed by the Core Engine's Workflow Engine, which reads the industry\-specific states and transitions from \`RUL\_Workflow\`\.

4\. \*\*All forms and screens\*\* are generated dynamically by the Core Engine's UI Engine, which reads the industry\-specific metadata from \`META\_FieldDefinition\`\.

\#\#\# 3\.6 Multi\-Industry Implementation Flow

To launch a new industry vertical:

| Step | Action | Effort | Dependencies |

|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \*\*1\*\* | Define Industry Profile | 1 Day | None |

| \*\*2\*\* | Define Reference Data | 2\-3 Days | \`REF\_\` tables |

| \*\*3\*\* | Define Product Model | 2\-3 Days | \`MST\_Product\`, \`META\_FieldDefinition\` |

| \*\*4\*\* | Define Transaction Tables \(if new\) | 3\-5 Days | Extend \`TRN\_\` with new tables \(or reuse existing via metadata\) |

| \*\*5\*\* | Define Workflows | 2\-3 Days | \`RUL\_Workflow\` |

| \*\*6\*\* | Define Business Rules | 3\-5 Days | \`RUL\_\` tables |

| \*\*7\*\* | Define Reports & KPIs | 2\-3 Days | \`BI\_KPI\`, \`META\_ReportDefinition\` |

| \*\*8\*\* | Define UI Configuration | 2\-3 Days | \`META\_FieldDefinition\` \(visibility, labels, controls\) |

| \*\*9\*\* | Package Seed Data | 1\-2 Days | Seed Data Specification |

| \*\*10\*\* | Smoke Testing | 2\-3 Days | Testing Strategy |

| \*\*Total\*\* | \(Configuration Only\) | \*\*3\-4 Weeks\*\* | \*\*\(No Code Changes Required\)\*\* |

\#\#\# 3\.7 Conclusion

ODOS is designed to be \*\*industry\-agnostic by design\*\*\.

\- The \*\*Core Engine\*\* provides an immutable, stable, enterprise\-grade foundation\.

\- The \*\*Configurable Layer\*\* provides the industry\-specific business logic, data models, workflows, rules, and reports\.

\*\*Guarantee:\*\*

1\. The platform can be deployed in multiple industries with \*\*3\-4 weeks of configuration\*\*\.

2\. \*\*Zero code changes\*\* are required to the Core Engine\.

3\. The \*\*Canonical Enterprise Data Model\*\* remains the stable semantic backbone\.

4\. \*\*Future innovations\*\* \(AI, Scalability, Security\) benefit all industries simultaneously\.

\-\-\-

\#\# 4\. Enterprise Foundation & Cross\-Cutting Concerns

\#\#\# 4\.1 Purpose

This section defines the foundational architectural services that apply across all modules and components of the ODOS platform\.

\#\#\# 4\.2 Foundation Components

| Component | Purpose | Implementation |

|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \*\*Multi\-Tenancy\*\* | Tenant isolation | \`CompanyID\` in all tenant\-owned tables |

| \*\*Audit & Lineage\*\* | Complete traceability | \`SEC\_AuditTrail\`, \`ETL\_DataLineage\` |

| \*\*Security\*\* | Authentication, authorisation, encryption | \`SEC\_\` tables, RBAC |

| \*\*Metadata\*\* | Dynamic behaviour | \`META\_\` tables |

| \*\*Configuration\*\* | Runtime settings | \`CFG\_\` tables |

| \*\*Reference Data\*\* | Lookup values | \`REF\_\` tables |

| \*\*Rules\*\* | Business logic | \`RUL\_\` tables |

| \*\*ETL\*\* | Data ingestion | \`ETL\_\` tables |

| \*\*AI\*\* | Mapping and learning | \`AI\_\` tables |

| \*\*BI\*\* | Analytics and reporting | \`BI\_\` tables |

\#\#\# 4\.3 Cross\-Cutting Concerns

\#\#\#\# 4\.3\.1 Audit & Traceability

All modules must contribute to \`SEC\_AuditTrail\` for every insert, update, delete, approval, and rejection\.

| Module | Audit Contribution |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Import Management | Batch creation, batch approval, batch rollback |

| Metadata Management | Metadata changes \(tables, fields, mappings\) |

| Validation Engine | Validation pass/fail events |

| Duplicate Resolution | Duplicate detected, merged, rejected |

| Transaction Engine | Case, Revenue, Commission, Expense, Payment, Invoice creation/update |

\#\#\#\# 4\.3\.2 AI Participation Matrix

| Module | AI Reads | AI Learns | AI Suggests | AI Validates | AI Scores | Human Approval Required |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Metadata Management | Yes | Yes | Yes | No | Yes | Yes |

| Metadata Mapping | Yes | Yes | Yes | No | Yes | Yes \(if low confidence\) |

| Duplicate Resolution | Yes | Yes | Yes | No | Yes | Yes |

| Data Quality | Yes | No | No | No | Yes | No |

| Case Management | Yes | Yes | Yes | No | No | No |

| Revenue Management | No | No | No | Future | No | Yes \(Adjustments\) |

| Commission Management | No | No | No | No | No | Yes |

| Forecasting Engine | Yes | Yes | Yes | No | No | Yes \(Publication\) |

| AI Learning Engine | Yes | Yes | Yes | No | No | No |

\#\#\#\# 4\.3\.3 Confidence Scoring

| Module | Confidence Generated? | Confidence Updated? | Confidence Consumed? | Confidence Threshold | Escalation Rules |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Import Management | Yes \(Batch Quality\) | Yes | Yes \(UI\) | 0\.7 | Manual review if < 0\.7 |

| Metadata Mapping | Yes \(Mapping Conf\) | Yes | Yes \(ETL, UI\) | 0\.7 | Manual review if < 0\.7 |

| Validation Engine | Yes \(Validation Score\) | Yes | Yes \(Data Quality\) | N/A | N/A |

| Duplicate Resolution | Yes \(Duplicate Conf\) | Yes | Yes \(UI\) | 0\.8 | Manual review |

| Data Quality | Yes \(Quality Score\) | Yes | Yes \(Dashboards\) | N/A | N/A |

| Forecasting Engine | Yes \(Forecast Conf\) | Yes | Yes \(UI\) | 0\.7 | Manual review |

\#\#\#\# 4\.3\.4 Multi\-Tenancy

All modules enforce tenant isolation via \`CompanyID\` in all \`MST\_\`, \`TRN\_\`, and \`ETL\_\` tables\. \`REF\_\` tables are global\. Application\-level filtering ensures users only see data for their tenant\.

\#\#\#\# 4\.3\.5 Financial Integrity

Modules handling financial data \(Revenue, Commission, Expense, Payment\) enforce:

\- Immutable approved financial records

\- No destructive updates \(reversal/adjustment only\)

\- Full audit trail \(\`SEC\_AuditTrail\`\)

\- Reconciliation traceability \(\`ETL\_DataLineage\`\)

\-\-\-

\#\# 5\. Architecture Decision Records \(ADR\-001 to ADR\-018\)

\#\#\# 5\.1 ADR Overview

This section contains the complete Architecture Decision Records for the ODOS platform\. Each ADR documents a significant architectural decision, including the context, decision, alternatives considered, rationale, consequences, and related principles\.

\*\*ADR Lifecycle:\*\*

\`\`\`

Draft

    ↓

Under Review

    ↓

Approved

    ↓

Implemented

    ↓

Superseded \(optional\)

    ↓

Archived \(never deleted\)

\`\`\`

\*\*ADR Numbering:\*\*

\- ADR\-001 to ADR\-018: Approved and Frozen

\- Future ADRs continue from ADR\-019 onward

\-\-\-

\#\#\# 5\.2 ADR\-001: Metadata\-Driven Enterprise Architecture

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*ADR ID\*\* | ADR\-001 |

| \*\*Title\*\* | Adoption of a Metadata\-Driven Enterprise Architecture |

| \*\*Status\*\* | Accepted |

| \*\*Version\*\* | 1\.0 |

| \*\*Decision Date\*\* | July 2026 |

| \*\*Category\*\* | Enterprise Architecture |

| \*\*Owner\*\* | CTO |

\#\#\#\# Context

ODOS is intended to evolve from an internal operating platform for a Direct Selling Agent \(DSA\) into a configurable commercial enterprise solution capable of supporting multiple organisations, lenders, products, and business models\.

The platform must accommodate frequent changes in lender MIS formats, business rules, workflows, reports, and operational processes without requiring continuous application redevelopment\.

A conventional hardcoded architecture would result in high maintenance costs, limited scalability, and increased dependency on software releases for routine business changes\.

\#\#\#\# Problem Statement

Traditional enterprise applications frequently embed business logic, field mappings, validation rules, report definitions, and workflow behaviour directly within application code\.

This approach creates several challenges:

\- High maintenance effort

\- Frequent code modifications

\- Increased testing requirements

\- Limited adaptability to new lenders and products

\- Slow response to regulatory or business changes

\- Increased implementation costs for new clients

ODOS requires an architecture capable of adapting through configuration rather than software redevelopment\.

\#\#\#\# Decision

ODOS shall adopt a \*\*Metadata\-Driven Enterprise Architecture\*\*\.

Business behaviour shall be controlled through metadata stored within dedicated metadata tables rather than through hardcoded application logic wherever practical\.

\*\*Metadata shall govern:\*\*

\- Data field definitions

\- Table definitions

\- Import templates

\- Excel mappings

\- Validation rules

\- Business rules

\- Report definitions

\- Dashboard definitions

\- Workflow configurations

\- AI learning mappings

\- Data lineage definitions

\- Data quality definitions

\*\*Application code shall interpret metadata at runtime\*\* to execute configurable business processes\.

\#\#\#\# Alternatives Considered

| Alternative | Description | Reason for Rejection |

|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Hardcoded Business Logic | Business rules implemented directly within application code | Difficult to maintain, requires frequent deployments, poor scalability, high long\-term maintenance cost |

| Hybrid Configuration | Partial metadata with significant hardcoded functionality | Creates inconsistent architecture, difficult to determine ownership of business logic, limits future extensibility |

| Fully Metadata\-Driven Architecture | Business behaviour defined through metadata and configuration | \*\*Accepted\*\* |

\#\#\#\# Rationale

The metadata\-driven approach provides:

\- Greater flexibility

\- Reduced maintenance effort

\- Improved scalability

\- Faster onboarding of new lenders

\- Simplified product customisation

\- Improved AI\-assisted automation

\- Reduced implementation cost

\- Better separation between business rules and software

It aligns with the long\-term vision of ODOS as a configurable enterprise platform rather than a fixed application\.

\#\#\#\# Consequences

\*\*Positive:\*\*

\- Minimal code changes for new lender formats

\- Configurable business rules

\- Dynamic report generation

\- AI\-assisted mapping becomes feasible

\- Simplified future productization

\- Improved maintainability

\*\*Negative:\*\*

\- Higher initial design complexity

\- Increased importance of metadata governance

\- More comprehensive testing of metadata changes

\- Slightly greater runtime complexity

\#\#\#\# Risks

| Risk | Mitigation |

|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|

| Poor\-quality metadata causing incorrect system behaviour | Metadata validation |

| Inadequate governance over metadata updates | Version control, approval workflows |

| Performance overhead if metadata is excessively dynamic | Performance optimisation, caching |

\#\#\#\# Architectural Impact

This decision establishes the foundation for:

\- \`META\_\` layer

\- Configuration framework

\- ETL engine

\- AI mapping engine

\- Dynamic reporting

\- Business Rules Engine

\- Validation framework

\#\#\#\# Related Architecture Principles

\- Principle 1 – Single Source of Truth

\- Principle 2 – Metadata\-Driven Architecture

\- Principle 3 – Configuration over Hardcoding

\- Principle 9 – Extensibility without Structural Redesign

\#\#\#\# Related ERD Entities

\- \`META\_TableDefinition\`

\- \`META\_FieldDefinition\`

\- \`META\_FieldMapping\`

\- \`META\_ImportTemplate\`

\- \`META\_ReportDefinition\`

\- \`META\_DashboardDefinition\`

\- \`RUL\_BusinessRule\`

\- \`RUL\_ValidationRule\`

\- \`AI\_Mapping\`

\- \`ETL\_DataLineage\`

\#\#\#\# Implementation Guidance

Implementation shall ensure that:

\- Metadata is stored centrally\.

\- Application logic reads metadata dynamically wherever practical\.

\- Business users can modify approved metadata through controlled administrative interfaces\.

\- Metadata changes are fully audited and version\-controlled\.

\- Critical metadata modifications require appropriate authorisation before becoming effective\.

\-\-\-

\#\#\# 5\.3 ADR\-002: Ten\-Layer Enterprise Architecture

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*ADR ID\*\* | ADR\-002 |

| \*\*Title\*\* | Adoption of a Ten\-Layer Enterprise Architecture |

| \*\*Status\*\* | Accepted |

| \*\*Version\*\* | 1\.0 |

| \*\*Decision Date\*\* | July 2026 |

| \*\*Category\*\* | Enterprise Architecture |

| \*\*Owner\*\* | CTO |

\#\#\#\# Context

ODOS is envisioned as a comprehensive enterprise platform that integrates customer acquisition, loan processing, lender management, finance, accounting, document management, analytics, artificial intelligence, and operational governance within a single ecosystem\.

As the platform evolves, new modules, integrations, workflows, and business capabilities will be introduced\. To ensure long\-term maintainability, scalability, and separation of responsibilities, the architecture requires a structured logical organisation\.

\#\#\#\# Problem Statement

Enterprise systems often become difficult to maintain when business entities, configuration, security, transactions, analytics, and technical metadata are mixed within a single database structure\.

Such designs typically result in:

\- Poor maintainability

\- Difficult navigation

\- Tight coupling between modules

\- Increased development complexity

\- Reduced scalability

\- Limited reusability

ODOS requires a logical structure that clearly separates responsibilities while maintaining seamless integration across all functional areas\.

\#\#\#\# Decision

ODOS shall adopt a \*\*Ten\-Layer Enterprise Data Architecture\*\*, with each layer representing a distinct business or technical responsibility\.

| Layer | Prefix | Purpose |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|

| Metadata | \`META\_\` | Defines the system itself, including tables, fields, mappings, reports, dashboards, and metadata |

| Configuration | \`CFG\_\` | Stores configurable settings, numbering schemes, calendars, company settings, and application parameters |

| Security | \`SEC\_\` | Manages users, roles, permissions, authentication, authorisation, and audit trails |

| Reference | \`REF\_\` | Stores static reference data such as country codes, status codes, and lookup values |

| Masters | \`MST\_\` | Maintains master records such as companies, customers, lenders, employees, products, vendors, and reference entities |

| Rules | \`RUL\_\` | Defines configurable business rules, commission structures, validation logic, tax rules, workflows, and calculation models |

| Transactions | \`TRN\_\` | Stores operational business transactions including leads, cases, revenues, commissions, expenses, invoices, and payments |

| ETL & Staging | \`ETL\_\` | Supports data ingestion, staging, validation, duplicate detection, lineage, and import monitoring |

| Audit & Documents | \`AUD\_\` | Maintains document repositories, file metadata, audit evidence, and document lifecycle information |

| Business Intelligence | \`BI\_\` | Stores analytical snapshots, profitability metrics, forecasts, KPIs, and reporting datasets |

| Artificial Intelligence | \`AI\_\` | Supports machine learning, mapping intelligence, user feedback, confidence scoring, and continuous learning |

Each layer shall have clearly defined responsibilities and shall interact with other layers only through approved architectural relationships\.

\#\#\#\# Alternatives Considered

| Alternative | Description | Reason for Rejection |

|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Flat Database Structure | All tables grouped together without logical separation | Difficult to navigate, poor scalability, weak governance |

| Functional Module\-Based Organisation | Separate tables only by application modules | Cross\-functional entities become duplicated, metadata and configuration become fragmented |

| Layered Enterprise Architecture | Logical separation based on architectural responsibility | \*\*Accepted\*\* |

\#\#\#\# Rationale

The Ten\-Layer Architecture provides:

\- Clear separation of responsibilities

\- Improved maintainability

\- Easier onboarding of new developers

\- Better governance

\- Simplified scalability

\- Improved productization

\- Better support for AI and analytics

\- Easier integration with external systems

\- Reduced long\-term technical debt

\#\#\#\# Consequences

\*\*Positive:\*\*

\- Consistent database organisation

\- Simplified navigation

\- Reduced coupling

\- Improved modularity

\- Better scalability

\- Easier maintenance

\- Improved documentation

\- Enhanced governance

\*\*Negative:\*\*

\- Slightly higher initial design effort

\- Additional discipline required during implementation

\- Developers must understand layer responsibilities before introducing new entities

\#\#\#\# Risks

| Risk | Mitigation |

|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|

| Incorrect placement of entities within layers | Database Standards Manual, Architecture reviews |

| Cross\-layer dependencies becoming excessive | ADR governance, Design validation |

| Future developers bypassing architectural conventions | Architecture reviews, Design validation during implementation |

\#\#\#\# Architectural Impact

This decision governs the organisation of the entire ODOS data model\.

All future entities shall be assigned to one of the ten approved layers\.

No new architectural layer shall be introduced without a formal Architecture Decision Record\.

The layer prefixes \(\`META\_\`, \`CFG\_\`, \`SEC\_\`, \`REF\_\`, \`MST\_\`, \`RUL\_\`, \`TRN\_\`, \`ETL\_\`, \`AUD\_\`, \`BI\_\`, \`AI\_\`\) are mandatory naming conventions and form part of the enterprise database standards\.

\#\#\#\# Related Architecture Principles

\- Principle 2 – Metadata\-Driven Architecture

\- Principle 3 – Configuration over Hardcoding

\- Principle 9 – Extensibility without Structural Redesign

\- Principle 12 – Architecture Governance

\#\#\#\# Implementation Guidance

Implementation shall ensure that:

\- Every new table is assigned to one of the ten architectural layers\.

\- Table prefixes conform to the approved naming standards\.

\- Cross\-layer dependencies are minimised and documented\.

\- Shared services are implemented through metadata, configuration, or business rules rather than duplication\.

\- Layer responsibilities are preserved throughout the lifecycle of the platform\.

\-\-\-

\#\#\# 5\.4 ADR\-003: Multi\-Tenant Enterprise Architecture

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*ADR ID\*\* | ADR\-003 |

| \*\*Title\*\* | Adoption of a Multi\-Tenant Enterprise Architecture |

| \*\*Status\*\* | Accepted |

| \*\*Version\*\* | 1\.0 |

| \*\*Decision Date\*\* | July 2026 |

| \*\*Category\*\* | Enterprise Architecture |

| \*\*Owner\*\* | CTO |

\#\#\#\# Context

ODOS is initially being developed as the internal operating system for a Direct Selling Agent \(DSA\)\. However, the long\-term vision is to evolve ODOS into a configurable commercial platform capable of serving multiple independent DSA organisations using a common application framework\.

To avoid costly architectural redesign during future productization, multi\-tenancy must be incorporated into the core data architecture from the outset\.

\#\#\#\# Problem Statement

Traditional single\-organisation systems tightly couple business logic and data structures to a single company's operations\. Such systems become difficult and expensive to convert into multi\-client enterprise applications\.

Without a multi\-tenant architecture, future commercialisation would require:

\- Extensive database redesign

\- Significant application refactoring

\- Complex data migration

\- Increased implementation cost

\- Higher maintenance effort

\- Greater operational risk

ODOS requires an architecture that supports both internal deployment and future Software\-as\-a\-Service \(SaaS\) or on\-premise implementations without structural modification\.

\#\#\#\# Decision

ODOS shall adopt a \*\*Multi\-Tenant Enterprise Architecture\*\*\.

Each organisation \(tenant\) shall be represented by a master record in \`MST\_Company\`, and all tenant\-specific master and transactional data shall be logically associated with a \`CompanyID\`\.

The architecture shall ensure:

\- Logical isolation of each tenant's data

\- Shared application codebase

\- Shared metadata framework where appropriate

\- Tenant\-specific configuration

\- Tenant\-specific business rules

\- Tenant\-specific numbering schemes

\- Tenant\-specific reports and dashboards

\- Independent financial records

Future deployments shall support both:

\- Single\-tenant installations

\- Multi\-tenant enterprise deployments

No structural database redesign shall be required to transition between these deployment models\.

\#\#\#\# Alternatives Considered

| Alternative | Description | Reason for Rejection |

|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Single\-Tenant Architecture | A separate database for each organisation | Poor scalability, difficult productization, duplicate codebase maintenance, higher deployment costs |

| Separate Schema per Tenant | Each organisation maintains its own database schema | Complex schema management, difficult version synchronization, increased maintenance overhead, poor scalability for large numbers of tenants |

| Shared Database with Logical Tenant Isolation | A single logical database supporting multiple tenants through CompanyID\-based partitioning | \*\*Accepted\*\* |

\#\#\#\# Rationale

The selected architecture provides:

\- Future SaaS readiness

\- Single codebase maintenance

\- Simplified upgrades

\- Reduced implementation costs

\- Consistent architecture across all deployments

\- Easier onboarding of new DSA organisations

\- Shared platform innovation while preserving complete data isolation

\#\#\#\# Consequences

\*\*Positive:\*\*

\- Future\-proof architecture

\- Simplified commercialisation

\- Reduced technical debt

\- Shared platform improvements

\- Consistent product evolution

\- Easier deployment management

\- Improved scalability

\*\*Negative:\*\*

\- Slight increase in initial database complexity

\- Mandatory tenant filtering throughout the application

\- Additional security considerations

\#\#\#\# Risks

| Risk | Mitigation |

|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|

| Cross\-tenant data exposure due to application errors | Mandatory CompanyID validation, Standardised repository and query patterns, Security testing |

| Missing CompanyID references in future tables | Architecture reviews, Automated validation during development |

| Inconsistent tenant filtering in reports or integrations | Architecture reviews, Security testing |

\#\#\#\# Architectural Impact

This decision affects nearly every layer of the architecture\.

All applicable master and transaction tables shall include \`CompanyID\` either:

\- Directly as a foreign key; or

\- Indirectly through a controlled parent relationship\.

Configuration, business rules, reports, workflows, and AI learning shall support tenant\-specific behaviour while preserving a common application framework\.

\#\#\#\# Related Architecture Principles

\- Principle 1 – Single Source of Truth

\- Principle 3 – Configuration over Hardcoding

\- Principle 8 – Multi\-Tenant by Design

\- Principle 9 – Extensibility without Structural Redesign

\- Principle 12 – Architecture Governance

\#\#\#\# Related ERD Entities

Primary entities include, but are not limited to:

\- \`MST\_Company\`

\- \`CFG\_CompanySettings\`

\- \`CFG\_FinancialYear\`

\- \`CFG\_AutoNumbering\`

\- \`SEC\_User\`

\- \`MST\_InternalBranch\`

\- \`MST\_Employee\`

\- \`MST\_Customer\`

\- \`MST\_Connector\`

\- \`MST\_Vendor\`

\- \`TRN\_Lead\`

\- \`TRN\_Case\`

\- \`TRN\_Revenue\`

\- \`TRN\_Commission\`

\- \`TRN\_Expense\`

\- \`TRN\_Invoice\`

\- \`TRN\_Payment\`

\- \`BI\_DailySnapshot\`

\- \`BI\_MonthlySnapshot\`

\#\#\#\# Implementation Guidance

Implementation shall ensure that:

\- \`CompanyID\` is treated as a mandatory architectural attribute for all tenant\-owned entities\.

\- All business transactions are executed within the context of a tenant\.

\- User authentication establishes tenant context at login\.

\- Reports, dashboards, AI models, and analytics automatically enforce tenant isolation\.

\- Future APIs include tenant context in every request\.

\- Administrative functions support secure management of multiple organisations\.

\-\-\-

\#\#\# 5\.5 ADR\-004: ETL\-First Data Ingestion and Validation Architecture

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*ADR ID\*\* | ADR\-004 |

| \*\*Title\*\* | Adoption of an ETL\-First Data Ingestion and Validation Architecture |

| \*\*Status\*\* | Accepted |

| \*\*Version\*\* | 1\.0 |

| \*\*Decision Date\*\* | July 2026 |

| \*\*Category\*\* | Data Architecture / ETL |

| \*\*Owner\*\* | CTO |

\#\#\#\# Context

The primary source of operational data for ODOS consists of Microsoft Excel workbooks, CSV files, lender MIS reports, connector reports, manually maintained spreadsheets, and, in future releases, APIs, OCR, and other external systems\.

These external sources are inherently inconsistent in structure, quality, completeness, and naming conventions\. Different lenders and partners frequently change their file formats without prior notice, increasing the risk of incorrect imports and compromised data quality\.

ODOS requires a controlled mechanism for ingesting, validating, cleansing, and transforming external data before it becomes part of the enterprise system of record\.

\#\#\#\# Problem Statement

Directly importing external files into operational tables presents significant risks, including:

\- Duplicate records

\- Invalid or incomplete data

\- Inconsistent field mappings

\- Data corruption

\- Loss of source traceability

\- Inability to perform validation

\- Limited auditability

\- Difficult rollback and recovery

\- Reduced confidence in analytical reports

As ODOS is intended to serve as the enterprise system of record, it must ensure that only validated and approved data enters operational tables\.

\#\#\#\# Decision

ODOS shall adopt an \*\*ETL\-First Data Ingestion Architecture\*\*\.

All external data sources shall pass through a structured ETL pipeline before updating any master or transaction tables\.

\*\*Standard Processing Workflow:\*\*

\`\`\`

External Source

        │

       ▼

ETL Import Batch

        │

       ▼

Raw Staging

        │

       ▼

File Identification

        │

       ▼

Column Mapping

        │

       ▼

Data Validation

        │

       ▼

Business Rule Validation

        │

       ▼

Duplicate Detection

        │

       ▼

Exception Handling

        │

       ▼

User Review \(if required\)

        │

       ▼

ERP Master & Transaction Tables

        │

       ▼

Audit & Data Lineage

\`\`\`

\*\*No external source shall update ERP tables directly\.\*\*

\#\#\#\# Alternatives Considered

| Alternative | Description | Reason for Rejection |

|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Direct Excel Import | External files update ERP tables immediately | High risk of data corruption, no validation layer, no duplicate control, limited auditability, difficult rollback |

| Manual Data Entry | Users manually re\-enter data into the application | Time\-consuming, error\-prone, poor scalability, not practical for enterprise operations |

| ETL\-First Architecture | All data passes through controlled validation before becoming operational data | \*\*Accepted\*\* |

\#\#\#\# Rationale

The ETL\-first approach provides:

\- High data quality

\- Controlled validation

\- Duplicate prevention

\- Complete audit trail

\- Full data lineage

\- AI\-assisted mapping

\- Import repeatability

\- Rollback capability

\- Consistent business rule enforcement

\#\#\#\# Consequences

\*\*Positive:\*\*

\- Improved data integrity

\- Better user confidence

\- Reduced operational errors

\- Simplified troubleshooting

\- Enhanced audit compliance

\- Support for future AI automation

\- Scalable onboarding of new lenders and partners

\*\*Negative:\*\*

\- Additional processing time before data becomes operational

\- Higher initial implementation effort

\- More sophisticated ETL infrastructure required

\#\#\#\# Risks

| Risk | Mitigation |

|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|

| Poorly designed validation rules | Configurable validation rules, Metadata\-driven mappings |

| Incorrect field mappings | Metadata\-driven mappings, AI\-assisted learning |

| Large import volumes affecting performance | Batch processing, Import monitoring |

| Incomplete exception handling | Comprehensive error logging, AI\-assisted learning |

\#\#\#\# Architectural Impact

This decision establishes the ETL layer as the mandatory gateway for all external data\.

It directly influences:

\- Data quality

\- Auditability

\- AI learning

\- Business rule execution

\- Reporting accuracy

\- Financial integrity

\#\#\#\# Related Architecture Principles

\- Principle 1 – Single Source of Truth

\- Principle 2 – Metadata\-Driven Architecture

\- Principle 4 – ETL\-First Data Processing

\- Principle 5 – AI\-Assisted, Human\-Governed Processing

\- Principle 6 – Audit by Design

\#\#\#\# Related ERD Entities

\- \`ETL\_ImportBatch\`

\- \`ETL\_StagingRawData\`

\- \`ETL\_ErrorLog\`

\- \`ETL\_DataLineage\`

\- \`ETL\_DuplicateQueue\`

\- \`ETL\_DataQualityScore\`

\- \`META\_FieldMapping\`

\- \`META\_ImportTemplate\`

\- \`RUL\_ValidationRule\`

\- \`AI\_Mapping\`

\- \`AI\_Learning\`

\#\#\#\# Implementation Guidance

Implementation shall ensure that:

\- Every import receives a unique Batch ID\.

\- Raw source files remain preserved\.

\- Original source data is never overwritten\.

\- Every imported value can be traced to its source file, worksheet, row, and column\.

\- Validation occurs before posting\.

\- Duplicate detection is configurable\.

\- Exception records are isolated for user review\.

\- Successful imports generate complete audit records\.

\- Failed imports do not partially update operational tables\.

\-\-\-

\#\#\# 5\.6 ADR\-005: Unified Party Management Architecture

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*ADR ID\*\* | ADR\-005 |

| \*\*Title\*\* | Adoption of a Unified Party Management Architecture |

| \*\*Status\*\* | Accepted |

| \*\*Version\*\* | 1\.0 |

| \*\*Decision Date\*\* | July 2026 |

| \*\*Category\*\* | Master Data Management \(MDM\) |

| \*\*Owner\*\* | CTO |

\#\#\#\# Context

ODOS manages multiple categories of entities that interact with the business, including customers, lenders, connectors, employees, vendors, referral partners, and other organisations\.

Although these entities perform different business roles, they share common characteristics such as names, addresses, contact information, banking details, tax identifiers, and documents\.

A consistent approach is required to manage these entities while supporting role\-specific business information\.

\#\#\#\# Problem Statement

Traditional ERP systems often maintain separate master records for different business entities\.

This frequently results in:

\- Duplicate information

\- Multiple records for the same person or organisation

\- Inconsistent contact information

\- Difficult KYC management

\- Repeated document storage

\- Poor relationship management

\- Increased maintenance effort

\- Limited reporting across business roles

ODOS requires a unified architectural approach that supports multiple business roles without unnecessary duplication\.

\#\#\#\# Decision

ODOS shall adopt a \*\*Unified Party Management Architecture\*\*\.

Every business participant shall be treated as a Party, capable of performing one or more business roles\.

\*\*Examples:\*\*

\- Customer

\- Connector

\- Employee

\- Vendor

\- Lender

\- Referral Partner

\- Branch

\- Government Authority

Role\-specific information shall remain within the appropriate master tables, while common business information shall follow standardised design principles\.

\#\#\#\# Alternatives Considered

| Alternative | Description | Reason for Rejection |

|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Independent Master Tables | Separate structures for every entity | High duplication, difficult maintenance, poor scalability, limited relationship management |

| Single Universal Party Table | Store every entity in one table | Increased implementation complexity, larger learning curve \(deferred to future\) |

| Unified Party Philosophy with Specialised Masters | Common architectural principles with dedicated business masters | \*\*Accepted\*\* |

\#\#\#\# Rationale

The selected approach provides:

\- Reduced duplication

\- Better consistency

\- Easier future migration

\- Improved reporting

\- Simplified KYC

\- Better document management

\- Improved relationship management

\- Flexibility for future product evolution

\#\#\#\# Consequences

\*\*Positive:\*\*

\- Consistent master data

\- Better customer lifecycle management

\- Easier future enhancements

\- Reduced duplicate records

\- Improved reporting

\- Better data governance

\*\*Negative:\*\*

\- Additional design discipline required

\- Future migration planning needed if a full Party model is adopted

\- Some duplication remains in Version 1\.0 for operational efficiency

\#\#\#\# Risks

| Risk | Mitigation |

|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|

| Duplicate parties across master tables | Duplicate detection, Standard validation |

| Inconsistent updates | Shared business rules, Common identification standards |

| Missing relationship links | AI\-assisted duplicate identification |

\#\#\#\# Architectural Impact

This decision influences all master data management within ODOS\.

It establishes common design principles for:

\- Identity management

\- Contact information

\- Banking information

\- Tax identifiers

\- Document management

\- Relationship management

\#\#\#\# Related Architecture Principles

\- Principle 1 – Single Source of Truth

\- Principle 2 – Metadata\-Driven Architecture

\- Principle 6 – Audit by Design

\- Principle 9 – Extensibility without Structural Redesign

\#\#\#\# Related ERD Entities

\- \`MST\_Customer\`

\- \`MST\_Connector\`

\- \`MST\_Employee\`

\- \`MST\_Vendor\`

\- \`MST\_Lender\`

\- \`MST\_LenderRM\`

\- \`MST\_Company\`

\- \`AUD\_Document\`

\- \`AUD\_FileRepository\`

\#\#\#\# Implementation Guidance

Implementation shall ensure that:

\- Standard naming conventions are applied across all master entities\.

\- PAN, GSTIN, Aadhaar, CIN, and other identifiers follow consistent validation rules\.

\- Address, contact, and banking information use standardised structures\.

\- Duplicate detection considers all party types where appropriate\.

\- Documents are associated using common document management principles\.

\- Future migration to a fully unified Party model remains feasible without significant redesign\.

\-\-\-

\#\#\# 5\.7 ADR\-006: Configuration\-Driven Business Rules

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*ADR ID\*\* | ADR\-006 |

| \*\*Title\*\* | Adoption of a Configuration\-Driven Business Rules Architecture |

| \*\*Status\*\* | Accepted |

| \*\*Version\*\* | 1\.0 |

| \*\*Decision Date\*\* | July 2026 |

| \*\*Category\*\* | Business Architecture / Configuration Management |

| \*\*Owner\*\* | CTO |

\#\#\#\# Context

ODOS operates in a dynamic business environment where commission structures, lender agreements, taxation, workflows, incentive schemes, approval hierarchies, validation rules, and operational policies are subject to frequent changes\.

Embedding such business rules directly within application code would require repeated software modifications, testing, and deployments, resulting in increased maintenance costs and reduced business agility\.

To ensure long\-term adaptability, business behaviour must be configurable rather than hardcoded\.

\#\#\#\# Problem Statement

Hardcoded business rules create significant operational and technical challenges, including:

\- Frequent code changes for routine business updates

\- Increased dependence on software developers

\- Longer implementation cycles

\- Higher testing and deployment effort

\- Greater risk of introducing defects

\- Difficulty supporting multiple lenders and tenants with different business rules

ODOS requires a flexible architecture where business users can manage operational rules through controlled configuration\.

\#\#\#\# Decision

ODOS shall adopt a \*\*Configuration\-Driven Business Rules Architecture\*\*\.

Business behaviour shall be controlled through configurable master data and rule tables rather than application code wherever practical\.

\*\*Configuration shall include, but not be limited to:\*\*

\- Commission structures

\- Incentive schemes

\- GST and TDS rules

\- Workflow stages

\- Approval hierarchies

\- Validation rules

\- Financial year settings

\- Auto\-numbering

\- Calendar and holiday definitions

\- Lender agreements

\- Import templates

\- Dashboard parameters

\- Report definitions

\*\*Application code shall execute these rules dynamically\*\* based on the active configuration\.

\#\#\#\# Alternatives Considered

| Alternative | Description | Reason for Rejection |

|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Hardcoded Rules | Business logic embedded directly within application code | Difficult to maintain, requires software releases for routine changes, not scalable for multiple lenders or tenants, high operational dependency on developers |

| Mixed Configuration and Hardcoding | Some rules configurable, others hardcoded | Creates inconsistent architecture, makes troubleshooting difficult, leads to unclear ownership of business logic |

| Configuration\-Driven Architecture | Business rules maintained through metadata and configuration | \*\*Accepted\*\* |

\#\#\#\# Rationale

A configuration\-driven approach provides:

\- Business flexibility

\- Faster implementation of policy changes

\- Reduced software maintenance

\- Simplified onboarding of new lenders

\- Better support for multi\-tenancy

\- Easier compliance with regulatory changes

\- Improved transparency of business rules

\- Greater product configurability for future customers

\#\#\#\# Consequences

\*\*Positive:\*\*

\- Minimal code changes for business policy updates

\- Faster response to regulatory changes

\- Easier implementation for new clients

\- Improved maintainability

\- Better separation of business logic from application logic

\*\*Negative:\*\*

\- Increased importance of configuration governance

\- More comprehensive validation required

\- Greater dependency on accurate configuration data

\#\#\#\# Risks

| Risk | Mitigation |

|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|

| Incorrect configuration affecting business operations | Role\-based access control, Versioning of configuration records |

| Unauthorised changes to business rules | Approval workflows for critical changes, Audit trails |

| Conflicting or incomplete rule definitions | Configuration validation during deployment |

\#\#\#\# Architectural Impact

This decision establishes configuration as the primary mechanism for controlling business behaviour\.

It directly influences:

\- Commission calculations

\- Incentive processing

\- Tax computation

\- Workflow management

\- ETL validation

\- Reporting

\- AI recommendations

\- Product customisation

\#\#\#\# Related Architecture Principles

\- Principle 2 – Metadata\-Driven Architecture

\- Principle 3 – Configuration over Hardcoding

\- Principle 8 – Multi\-Tenant by Design

\- Principle 9 – Extensibility without Structural Redesign

\#\#\#\# Related ERD Entities

\- \`CFG\_CompanySettings\`

\- \`CFG\_FinancialYear\`

\- \`CFG\_AutoNumbering\`

\- \`CFG\_Calendar\`

\- \`CFG\_EmailSMSConfig\`

\- \`RUL\_CommissionRule\`

\- \`RUL\_CommissionSlab\`

\- \`RUL\_Workflow\`

\- \`RUL\_BusinessRule\`

\- \`RUL\_GSTRule\`

\- \`RUL\_TDSRule\`

\- \`RUL\_ValidationRule\`

\- \`MST\_LenderAgreement\`

\- \`META\_ImportTemplate\`

\- \`META\_ReportDefinition\`

\#\#\#\# Implementation Guidance

Implementation shall ensure that:

\- Business rules are stored in dedicated configuration and rule tables\.

\- Configuration changes are audited and version\-controlled\.

\- Rule evaluation is deterministic and traceable\.

\- Critical configurations require appropriate authorisation before activation\.

\- Default configurations are provided for new tenants\.

\- Business users can manage approved configurations through administrative interfaces without requiring code changes\.

\-\-\-

\#\#\# 5\.8 ADR\-007: Audit by Design and Immutable Audit Trail

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*ADR ID\*\* | ADR\-007 |

| \*\*Title\*\* | Adoption of an Audit\-by\-Design Architecture with Immutable Audit Trails |

| \*\*Status\*\* | Accepted |

| \*\*Version\*\* | 1\.0 |

| \*\*Decision Date\*\* | July 2026 |

| \*\*Category\*\* | Security / Governance / Compliance |

| \*\*Owner\*\* | CTO |

\#\#\#\# Context

ODOS manages sensitive operational and financial information, including customer data, loan applications, commissions, invoices, payments, taxes, expenses, and business rules\.

As the platform evolves into an enterprise\-grade DSA Operating System, every significant business action must be traceable to ensure operational transparency, regulatory compliance, dispute resolution, and accountability\.

Auditability shall not be treated as an optional feature but as a foundational architectural capability\.

\#\#\#\# Problem Statement

Enterprise systems that do not maintain comprehensive audit records face several risks, including:

\- Inability to determine who changed data

\- Loss of historical information

\- Difficulty investigating operational issues

\- Increased fraud risk

\- Weak financial controls

\- Poor regulatory compliance

\- Limited accountability

\- Reduced confidence in reports and analytics

Because ODOS will become the operational system of record, it must maintain complete historical traceability for all significant business events\.

\#\#\#\# Decision

ODOS shall implement an \*\*Audit\-by\-Design Architecture\*\*\.

Audit capabilities shall be incorporated into every major functional area rather than added retrospectively\.

\*\*The architecture shall record:\*\*

\- Record creation

\- Record modification

\- Logical deletion

\- Status changes

\- Approval actions

\- User authentication events

\- Data imports

\- ETL processing

\- AI recommendations and overrides

\- Configuration changes

\- Business rule changes

\- Financial transactions

\- Workflow transitions

\*\*Audit records shall be retained as immutable historical evidence\.\*\*

No audit record shall be physically modified or deleted through normal application processes\.

\#\#\#\# Alternatives Considered

| Alternative | Description | Reason for Rejection |

|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Minimal Logging | Store only timestamps and last modified user | Insufficient for investigations, no historical reconstruction, poor regulatory support |

| Application Log Files | Maintain audit information within application logs | Difficult to query, poor business traceability, limited reporting capability, not integrated with operational data |

| Database\-Centric Audit Architecture | Maintain structured audit records within dedicated audit tables | \*\*Accepted\*\* |

\#\#\#\# Rationale

A structured audit architecture provides:

\- Complete accountability

\- Historical reconstruction

\- Regulatory compliance

\- Financial traceability

\- Support for internal audits

\- Simplified troubleshooting

\- Better governance

\- Improved user confidence

\- Enhanced fraud detection

\#\#\#\# Scope of Auditing

Audit records shall be maintained for, at a minimum:

\*\*Security Events:\*\*

\- Login

\- Logout

\- Password changes

\- Failed authentication

\- Permission changes

\*\*Master Data:\*\*

\- Customer changes

\- Lender updates

\- Connector updates

\- Vendor changes

\- Employee modifications

\- Product updates

\*\*Financial Data:\*\*

\- Revenue posting

\- Commission calculations

\- Expense recording

\- Invoice generation

\- Payment receipt

\- Bank reconciliation

\- Tax calculations

\*\*ETL Activities:\*\*

\- File uploads

\- Validation results

\- Duplicate detection

\- Import approvals

\- Import failures

\- Rollbacks

\*\*Configuration:\*\*

\- Business rule changes

\- Workflow updates

\- Commission revisions

\- Validation modifications

\- Metadata changes

\*\*AI Activities:\*\*

\- Suggested mappings

\- User overrides

\- Learning updates

\- Confidence scores

\*\*Audit Information to Capture:\*\*

Every audit record shall capture, where applicable:

\- AuditID

\- CompanyID

\- Entity Name

\- Record Identifier

\- Event Type

\- Operation \(Insert, Update, Delete, Approve, Reject\)

\- Previous Value

\- New Value

\- Changed Fields

\- UserID

\- Timestamp

\- Source \(Manual, ETL, API, AI\)

\- BatchID \(if ETL\)

\- SessionID

\- Reason for Change \(optional\)

\- Reference Document

\#\#\#\# Architectural Impact

This decision establishes auditing as a mandatory architectural capability\.

It directly influences:

\- \`SEC\_AuditTrail\`

\- \`ETL\_DataLineage\`

\- \`ETL\_ImportBatch\`

\- \`AI\_Learning\`

\- \`AI\_Feedback\`

\- All Master Tables

\- All Transaction Tables

\- Configuration Tables

\- Business Rule Tables

\#\#\#\# Related Architecture Principles

\- Principle 1 – Single Source of Truth

\- Principle 5 – AI\-Assisted, Human\-Governed Processing

\- Principle 6 – Audit by Design

\- Principle 7 – Financial Integrity

\- Principle 12 – Architecture Governance

\#\#\#\# Related ERD Entities

Primary audit entities include:

\- \`SEC\_AuditTrail\`

\- \`SEC\_LoginHistory\`

\- \`ETL\_ImportBatch\`

\- \`ETL\_DataLineage\`

\- \`ETL\_ErrorLog\`

\- \`AUD\_Document\`

\- \`AUD\_FileRepository\`

\- \`AI\_Learning\`

\- \`AI\_Feedback\`

All master and transaction entities shall participate in the audit framework through standardised audit fields\.

\#\#\#\# Implementation Guidance

Implementation shall ensure that:

\- Audit logging is automatic and cannot be bypassed by normal application users\.

\- Audit records are append\-only and immutable\.

\- Sensitive information is masked where required to protect privacy while preserving traceability\.

\- Every transaction can be traced back to the initiating user, process, or import batch\.

\- Audit retention policies are configurable to meet business and regulatory requirements\.

\- Audit data is optimised for reporting and investigation without impacting operational performance\.

\-\-\-

\#\#\# 5\.9 ADR\-008: Enterprise Data Lineage and Data Provenance

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*ADR ID\*\* | ADR\-008 |

| \*\*Title\*\* | Adoption of Enterprise Data Lineage and Data Provenance Architecture |

| \*\*Status\*\* | Accepted |

| \*\*Version\*\* | 1\.0 |

| \*\*Decision Date\*\* | July 2026 |

| \*\*Category\*\* | Data Governance / ETL / Enterprise Data Management |

| \*\*Owner\*\* | CTO |

\#\#\#\# Context

ODOS integrates data from multiple external sources, including lender MIS files, connector reports, customer spreadsheets, manual data entry, APIs, OCR outputs, and future third\-party integrations\.

Given the diversity and variability of these sources, it is essential that every piece of operational data stored within ODOS can be traced back to its original source\.

Data lineage is fundamental to ensuring trust, transparency, reconciliation, troubleshooting, regulatory compliance, and AI\-assisted learning\.

\#\#\#\# Problem Statement

Without data lineage, organisations face several operational risks:

\- Inability to identify the source of incorrect data

\- Difficulty reconciling imported information

\- Limited confidence in reports and analytics

\- Poor auditability

\- Inability to replay or reprocess imports

\- Difficulty improving import quality

\- Limited explainability of AI\-generated mappings

\- Increased operational risk during dispute resolution

\#\#\#\# Decision

ODOS shall implement a comprehensive \*\*Enterprise Data Lineage and Data Provenance Architecture\*\*\.

Every imported, transformed, validated, and stored data element shall maintain traceability to its origin\.

\*\*The lineage framework shall capture:\*\*

\- Source system

\- Source file

\- Source worksheet

\- Source table \(if applicable\)

\- Source row

\- Source column

\- Original value

\- Transformed value

\- Validation results

\- Business rules applied

\- Transformation logic

\- Import batch

\- Import timestamp

\- User or process initiating the import

\- AI mapping decisions \(where applicable\)

\*\*Lineage information shall be retained independently\*\* of operational data to support auditing, troubleshooting, and historical analysis\.

\#\#\#\# Alternatives Considered

| Alternative | Description | Reason for Rejection |

|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| No Lineage | Import data without recording its origin | Poor traceability, difficult investigations, weak governance, reduced trust in reports |

| File\-Level Lineage Only | Track only the source file | Insufficient granularity, cannot identify row\- or field\-level issues, limited debugging capability |

| Field\-Level Enterprise Lineage | Maintain lineage for every imported data element | \*\*Accepted\*\* |

\#\#\#\# Rationale

Field\-level lineage provides:

\- Complete traceability

\- Better audit support

\- Simplified troubleshooting

\- Easier duplicate analysis

\- Improved reconciliation

\- Better AI learning

\- Transparent transformations

\- Reliable regulatory reporting

\- Higher confidence in analytics

\#\#\#\# Scope of Lineage

The lineage framework shall apply to:

\*\*External Imports:\*\*

\- Excel

\- CSV

\- PDF \(OCR\)

\- API

\- XML

\- JSON

\- Manual uploads

\*\*Internal Transformations:\*\*

\- Validation

\- Data cleansing

\- Standardisation

\- Duplicate resolution

\- Calculated fields

\- Business rule execution

\- AI\-assisted mapping

\*\*Operational Updates:\*\*

\- Manual corrections

\- Workflow changes

\- Financial adjustments

\- Status updates

\- System\-generated values

\*\*Information Captured:\*\*

Each lineage record should capture, where applicable:

\- LineageID

\- CompanyID

\- ImportBatchID

\- SourceSystem

\- SourceFileName

\- SourceWorksheet

\- SourceTable

\- SourceRowNumber

\- SourceColumnName

\- SourceValue

\- TargetTable

\- TargetField

\- TargetRecordID

\- StoredValue

\- TransformationType

\- TransformationExpression

\- ValidationRuleApplied

\- ValidationResult

\- DuplicateCheckResult

\- AIConfidenceScore

\- UserDecision

\- ProcessingTimestamp

\- PipelineVersion

\#\#\#\# Architectural Impact

This decision establishes data lineage as a mandatory enterprise capability\.

It directly influences:

\- ETL architecture

\- AI learning

\- Audit framework

\- Validation engine

\- Duplicate detection

\- Reporting

\- Financial reconciliation

\- Metadata management

\#\#\#\# Related Architecture Principles

\- Principle 1 – Single Source of Truth

\- Principle 2 – Metadata\-Driven Architecture

\- Principle 4 – ETL\-First Data Processing

\- Principle 5 – AI\-Assisted, Human\-Governed Processing

\- Principle 6 – Audit by Design

\#\#\#\# Related ERD Entities

\- \`ETL\_DataLineage\`

\- \`ETL\_ImportBatch\`

\- \`ETL\_StagingRawData\`

\- \`ETL\_ErrorLog\`

\- \`META\_FieldMapping\`

\- \`META\_ImportTemplate\`

\- \`AI\_Mapping\`

\- \`AI\_Learning\`

\- \`SEC\_AuditTrail\`

\#\#\#\# Implementation Guidance

Implementation shall ensure that:

\- Every import receives a unique BatchID\.

\- Raw source files are preserved in their original form\.

\- Source values are never overwritten within the lineage repository\.

\- Lineage records remain immutable after successful processing\.

\- Transformations are fully documented and reproducible\.

\- Users can trace any operational value back to its originating source through the application interface\.

\- Lineage storage is optimised to support high\-volume imports without impacting operational performance\.

\-\-\-

\#\#\# 5\.10 ADR\-009: Financial Integrity and Immutable Financial Transactions

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*ADR ID\*\* | ADR\-009 |

| \*\*Title\*\* | Adoption of a Financial Integrity Architecture with Immutable Financial Transactions |

| \*\*Status\*\* | Accepted |

| \*\*Version\*\* | 1\.0 |

| \*\*Decision Date\*\* | July 2026 |

| \*\*Category\*\* | Financial Architecture / Data Governance |

| \*\*Owner\*\* | CTO |

\#\#\#\# Context

ODOS is designed to operate as the financial and operational backbone of a Direct Selling Agent \(DSA\)\. It manages the complete financial lifecycle associated with loan sourcing, including lender commissions, connector payouts, employee incentives, operational expenses, taxation, invoicing, collections, and cash flow\.

Financial information generated within ODOS serves as the basis for management reporting, profitability analysis, statutory compliance, and integration with external accounting systems such as Tally or future ERP platforms\.

Accordingly, the architecture must ensure that all financial data is accurate, traceable, auditable, and protected from unauthorised modification\.

\#\#\#\# Problem Statement

Financial systems that allow uncontrolled modification or deletion of monetary transactions expose organisations to significant risks, including:

\- Loss of financial integrity

\- Inaccurate profitability reporting

\- Difficult bank reconciliations

\- Tax computation errors

\- Commission disputes

\- Fraud

\- Regulatory non\-compliance

\- Loss of management confidence

\#\#\#\# Decision

ODOS shall adopt an \*\*Immutable Financial Transaction Architecture\*\*\.

Once a financial transaction has been posted and approved, it shall not be physically modified or deleted\.

\*\*Corrections shall be performed using controlled adjustment mechanisms such as:\*\*

\- Reversal entries

\- Adjustment vouchers

\- Credit notes

\- Debit notes

\- Corrective transactions

\- Version\-controlled amendments

\*\*The original financial record shall remain permanently preserved\.\*\*

\*\*Every financial transaction shall maintain complete traceability\*\* from business event to accounting impact\.

\#\#\#\# Scope

This decision applies to all financial entities, including:

\- Revenue

\- Commission

\- Incentives

\- Expenses

\- Vendor Payments

\- Customer Refunds

\- Invoices

\- Credit Notes

\- Debit Notes

\- GST

\- TDS

\- Payment Receipts

\- Bank Transactions

\- Working Capital Calculations

\- Financial Forecasts

\#\#\#\# Alternatives Considered

| Alternative | Description | Reason for Rejection |

|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Editable Financial Records | Allow direct modification of financial transactions | Weak auditability, high fraud risk, poor accounting practice, loss of historical integrity |

| Delete and Recreate | Delete incorrect transactions and create new ones | Breaks audit trails, invalidates reconciliations, difficult regulatory compliance |

| Immutable Financial Architecture | Retain original transactions permanently and process corrections through adjustment mechanisms | \*\*Accepted\*\* |

\#\#\#\# Rationale

The immutable financial model provides:

\- Complete auditability

\- Strong internal controls

\- Accurate profitability reporting

\- Reliable reconciliation

\- Improved fraud prevention

\- Better statutory compliance

\- Easier financial investigations

\- Trustworthy historical reporting

This approach aligns with established accounting principles and enterprise financial systems\.

\#\#\#\# Financial Posting Principles

Every financial transaction shall adhere to the following principles:

\- Every monetary event originates from a valid business event\.

\- Financial postings shall reference the originating operational transaction\.

\- Posted financial transactions shall be immutable\.

\- Adjustments shall create new records rather than overwrite existing ones\.

\- Tax calculations shall remain traceable to source transactions\.

\- Payment allocations shall preserve historical relationships\.

\- Every financial record shall support complete reconciliation\.

\#\#\#\# Architectural Impact

This decision governs the financial behaviour of:

\- \`TRN\_Revenue\`

\- \`TRN\_Commission\`

\- \`TRN\_Expense\`

\- \`TRN\_Invoice\`

\- \`TRN\_Payment\`

\- \`TRN\_TaxLiability\`

\- \`BI\_Profitability\`

\- \`BI\_Forecast\`

\- \`MST\_ChartOfAccounts\`

\- \`MST\_TallyMapping\`

\#\#\#\# Related Architecture Principles

\- Principle 1 – Single Source of Truth

\- Principle 6 – Audit by Design

\- Principle 7 – Financial Integrity

\- Principle 11 – Analytics by Design

\#\#\#\# Related ERD Entities

Primary entities affected include:

\- \`TRN\_Revenue\`

\- \`TRN\_Commission\`

\- \`TRN\_Expense\`

\- \`TRN\_Invoice\`

\- \`TRN\_Payment\`

\- \`TRN\_TaxLiability\`

\- \`MST\_ChartOfAccounts\`

\- \`MST\_TallyMapping\`

\- \`BI\_Profitability\`

\- \`BI\_Forecast\`

\- \`SEC\_AuditTrail\`

\#\#\#\# Implementation Guidance

Implementation shall ensure that:

\- Financial records are created through controlled business processes\.

\- Approved transactions become read\-only to normal users\.

\- Corrections generate linked adjustment records\.

\- Every transaction carries a unique financial reference number\.

\- Every payment is traceable to one or more invoices\.

\- Every commission is traceable to the originating loan case\.

\- Every expense is linked to an approved cost category and, where applicable, a vendor\.

\- Financial reports reconcile with operational data at all times\.

\-\-\-

\#\#\# 5\.11 ADR\-010: Working Capital and Cash Conversion Cycle Architecture

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*ADR ID\*\* | ADR\-010 |

| \*\*Title\*\* | Adoption of a Working Capital and Cash Conversion Cycle Architecture |

| \*\*Status\*\* | Accepted |

| \*\*Version\*\* | 1\.0 |

| \*\*Decision Date\*\* | July 2026 |

| \*\*Category\*\* | Financial Architecture / Business Operations |

| \*\*Owner\*\* | CTO |

\#\#\#\# Context

For a Direct Selling Agent \(DSA\), profitability depends not only on generating business but also on efficiently converting loan disbursements into realised cash\.

The period between customer acquisition, loan disbursement, invoice generation, payment collection, connector payouts, operational expenses, and final cash realisation directly affects liquidity, profitability, and business growth\.

Traditional CRM systems typically end at loan disbursement, while accounting systems begin only after invoices are raised\. Neither provides complete visibility into the Working Capital Cycle\.

ODOS is designed to bridge this operational gap by providing end\-to\-end visibility into the Cash Conversion Cycle \(CCC\)\.

\#\#\#\# Problem Statement

Without an integrated working capital framework, DSA organisations face:

\- Delayed invoicing

\- Outstanding receivables

\- Cash flow uncertainty

\- Delayed lender payments

\- Commission disputes

\- Connector payout delays

\- Difficulty forecasting working capital

\- Inability to measure collection efficiency

\- Poor financial planning

\#\#\#\# Decision

ODOS shall implement a \*\*Working Capital and Cash Conversion Cycle Architecture\*\*\.

Every loan case shall be tracked from:

\`\`\`

Lead

    ↓

Application

    ↓

Approval

    ↓

Sanction

    ↓

Disbursement

    ↓

Invoice Generation

    ↓

Invoice Submission

    ↓

Payment Due

    ↓

Payment Received

    ↓

Bank Reconciliation

    ↓

Connector Settlement

    ↓

Internal Incentive Settlement

    ↓

Case Closure

\`\`\`

The system shall calculate and monitor the complete working capital cycle for every transaction\.

\#\#\#\# Scope

This decision applies to:

\- Loan Cases

\- Disbursements

\- Revenue

\- Invoices

\- Collections

\- Payments

\- Connector Commissions

\- Employee Incentives

\- Operational Expenses

\- Tax Liabilities

\- Cash Flow Forecasting

\- Profitability Analysis

\#\#\#\# Key Working Capital Metrics

ODOS shall calculate and maintain, at minimum:

\*\*Receivable Metrics:\*\*

\- Outstanding Receivables

\- Ageing Analysis

\- Collection Efficiency

\- Days Sales Outstanding \(DSO\)

\*\*Payment Metrics:\*\*

\- Average Collection Days

\- Invoice Processing Time

\- Payment Delay

\- Collection Success Rate

\*\*Operational Metrics:\*\*

\- Case Processing Time

\- Disbursement TAT

\- Invoice Generation Lag

\- Payment Realisation Time

\*\*Working Capital Metrics:\*\*

\- Cash Conversion Cycle \(CCC\)

\- Working Capital Requirement

\- Collection Pipeline

\- Expected Cash Inflow

\- Expected Cash Outflow

\- Net Working Capital Position

\*\*Mandatory Business Dates:\*\*

Every financial case shall maintain, where applicable:

\- Lead Date

\- Login Date

\- Approval Date

\- Sanction Date

\- Disbursement Date

\- Invoice Generation Date

\- Invoice Submission Date

\- Invoice Due Date

\- Payment Received Date

\- Value Date

\- Bank Credit Date

\- Connector Payment Date

\- Employee Incentive Payment Date

\- Final Closure Date

\#\#\#\# Architectural Principles

The Working Capital Architecture shall follow these principles:

\- Every disbursement shall result in an expected revenue event\.

\- Every revenue event shall have an associated invoice lifecycle\.

\- Every invoice shall have an expected payment date\.

\- Every payment shall be reconciled to bank receipts\.

\- Every connector payout shall reference realised collections\.

\- Every employee incentive shall reference finalised revenue\.

\- Forecasts shall distinguish between expected and realised cash flows\.

\- Cash flow projections shall be continuously updated based on operational events\.

\#\#\#\# Alternatives Considered

| Alternative | Description | Reason for Rejection |

|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Financial Tracking Outside ERP | Maintain receivable tracking in Excel | Fragmented information, manual reconciliation, high operational risk, limited reporting |

| Accounting\-Only Tracking | Track receivables only after invoice generation | Ignores operational lead time, limited forecasting capability, poor management visibility |

| End\-to\-End Cash Conversion Architecture | Monitor the complete operational and financial lifecycle | \*\*Accepted\*\* |

\#\#\#\# Rationale

This architecture provides:

\- Complete cash flow visibility

\- Improved liquidity management

\- Better lender relationship management

\- Faster collections

\- Reduced working capital requirement

\- Accurate profitability measurement

\- Better forecasting

\- Improved management decision\-making

\#\#\#\# Architectural Impact

This decision directly affects:

\- \`TRN\_Case\`

\- \`TRN\_Disbursement\`

\- \`TRN\_Revenue\`

\- \`TRN\_Invoice\`

\- \`TRN\_Payment\`

\- \`TRN\_Commission\`

\- \`TRN\_IncentiveEarned\`

\- \`BI\_Forecast\`

\- \`BI\_Profitability\`

\- \`BI\_PortfolioRiskSnapshot\`

\#\#\#\# Related Architecture Principles

\- Principle 1 – Single Source of Truth

\- Principle 6 – Audit by Design

\- Principle 7 – Financial Integrity

\- Principle 11 – Analytics by Design

\#\#\#\# Related ERD Entities

Primary entities include:

\- \`TRN\_Case\`

\- \`TRN\_Disbursement\`

\- \`TRN\_Revenue\`

\- \`TRN\_Invoice\`

\- \`TRN\_Payment\`

\- \`TRN\_Commission\`

\- \`TRN\_IncentiveEarned\`

\- \`BI\_Forecast\`

\- \`BI\_Profitability\`

\- \`BI\_PortfolioRiskSnapshot\`

\- \`MST\_LenderAgreement\`

\#\#\#\# Implementation Guidance

Implementation shall ensure that:

\- Expected cash inflows and actual cash inflows are stored separately\.

\- Every lender agreement defines invoice generation timelines, credit periods, and payment terms\.

\- Alerts are generated for overdue invoices, delayed collections, and pending settlements\.

\- Cash flow forecasts are recalculated automatically whenever operational milestones change\.

\- Users can view the complete lifecycle of a case from lead generation through final cash realisation\.

\- Management dashboards present real\-time working capital and liquidity indicators at company, branch, lender, product, and employee levels\.

\-\-\-

\#\#\# 5\.12 ADR\-011: Cost Centre, Profit Centre and Enterprise Profitability Architecture

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*ADR ID\*\* | ADR\-011 |

| \*\*Title\*\* | Adoption of a Cost Centre and Profit Centre Architecture |

| \*\*Status\*\* | Accepted |

| \*\*Version\*\* | 1\.0 |

| \*\*Decision Date\*\* | July 2026 |

| \*\*Category\*\* | Financial Architecture / Management Accounting |

| \*\*Owner\*\* | CTO |

\#\#\#\# Context

As ODOS evolves into an enterprise operating system, management requires visibility not only into total revenue and expenses but also into the profitability of every organisational unit, business channel, lender, product, branch, employee, connector, and customer segment\.

Financial performance must be measurable at multiple levels to support informed decision\-making, operational efficiency, pricing strategies, resource allocation, and business expansion\.

\#\#\#\# Problem Statement

Many organisations maintain overall financial statements but cannot accurately determine:

\- Which branch is profitable

\- Which lender generates the highest margins

\- Which products consume the most resources

\- Which employees create value

\- Which connectors are profitable

\- Which expenses are controllable

\- Which customers generate sustainable profits

\#\#\#\# Decision

ODOS shall implement a \*\*Cost Centre and Profit Centre Architecture\*\* that enables allocation, tracking, and analysis of revenue and expenses across multiple business dimensions\.

Every financial transaction shall be capable of being associated with one or more analytical dimensions\.

\*\*The architecture shall support:\*\*

\- Direct cost allocation

\- Shared cost allocation

\- Revenue attribution

\- Contribution margin analysis

\- Gross profit analysis

\- Net profitability analysis

\- Multi\-dimensional reporting

\#\#\#\# Cost Centre Dimensions

The architecture shall support allocation of costs by, but not limited to:

\- Company

\- Region

\- Branch

\- Team

\- Department

\- Employee

\- Vendor

\- Cost Category

\- Expense Head

\- Project

\- Campaign

\- Business Function

\#\#\#\# Profit Centre Dimensions

Revenue and profitability shall be analysed across:

\- Company

\- Region

\- Branch

\- Team

\- Employee

\- Connector

\- Lender

\- Lender Branch

\- Product

\- Loan Scheme

\- Customer Segment

\- Campaign

\- Channel

\- Relationship Manager

\- Financial Year

\- Month

\- Quarter

\#\#\#\# Profitability Measurements

ODOS shall support calculation of:

\- Gross Revenue

\- Net Revenue

\- Direct Costs

\- Indirect Costs

\- Contribution Margin

\- Gross Profit

\- Operating Profit

\- Net Profit

\- Profit Margin %

\- Cost\-to\-Income Ratio

\- Revenue per Employee

\- Revenue per Branch

\- Revenue per Connector

\- Revenue per Lender

\- Revenue per Product

\#\#\#\# Alternatives Considered

| Alternative | Description | Reason for Rejection |

|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Company\-Level Profitability Only | Maintain overall financial reporting without analytical allocation | Limited decision support, no branch\-level visibility, poor resource optimisation |

| Manual Cost Allocation | Perform profitability analysis using spreadsheets | Error\-prone, time\-consuming, difficult to audit, not scalable |

| Integrated Profitability Architecture | Embed cost and profit analysis within the enterprise data model | \*\*Accepted\*\* |

\#\#\#\# Rationale

The selected architecture provides:

\- Better management decisions

\- Improved operational efficiency

\- Enhanced pricing strategies

\- Better resource allocation

\- Improved branch performance monitoring

\- Lender profitability analysis

\- Employee productivity measurement

\- Improved forecasting

\- Support for strategic planning

\#\#\#\# Architectural Impact

This decision influences:

\- \`TRN\_Revenue\`

\- \`TRN\_Commission\`

\- \`TRN\_Expense\`

\- \`TRN\_IncentiveEarned\`

\- \`TRN\_CampaignIncentive\`

\- \`BI\_Profitability\`

\- \`BI\_DailySnapshot\`

\- \`BI\_MonthlySnapshot\`

\- \`BI\_Forecast\`

\- \`MST\_ChartOfAccounts\`

\- \`MST\_Vendor\`

\- \`MST\_InternalBranch\`

\- \`MST\_Team\`

\- \`MST\_Employee\`

\#\#\#\# Related Architecture Principles

\- Principle 1 – Single Source of Truth

\- Principle 3 – Configuration over Hardcoding

\- Principle 7 – Financial Integrity

\- Principle 11 – Analytics by Design

\#\#\#\# Related ERD Entities

Primary entities include:

\- \`TRN\_Revenue\`

\- \`TRN\_Expense\`

\- \`TRN\_Commission\`

\- \`TRN\_IncentiveEarned\`

\- \`TRN\_CampaignIncentive\`

\- \`BI\_Profitability\`

\- \`BI\_Forecast\`

\- \`MST\_Vendor\`

\- \`MST\_ChartOfAccounts\`

\- \`MST\_InternalBranch\`

\- \`MST\_Team\`

\- \`MST\_Employee\`

\- \`MST\_Lender\`

\- \`MST\_Product\`

\- \`MST\_Connector\`

\#\#\#\# Implementation Guidance

Implementation shall ensure that:

\- Every expense is classified using a standardised Chart of Accounts\.

\- Every expense can be linked to one or more cost centres\.

\- Every revenue transaction can be attributed to one or more profit centres\.

\- Allocation rules are configurable and version\-controlled\.

\- Profitability reports support drill\-down from summary to transaction level\.

\- Shared cost allocations are transparent, reproducible, and fully auditable\.

\- Management dashboards present profitability across all supported analytical dimensions\.

\-\-\-

\#\#\# 5\.13 ADR\-012: Commission, Incentive and Compensation Engine Architecture

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*ADR ID\*\* | ADR\-012 |

| \*\*Title\*\* | Adoption of a Configurable Commission, Incentive and Compensation Engine |

| \*\*Status\*\* | Accepted |

| \*\*Version\*\* | 1\.0 |

| \*\*Decision Date\*\* | July 2026 |

| \*\*Category\*\* | Financial Architecture / Business Rules |

| \*\*Owner\*\* | CTO |

\#\#\#\# Context

The primary source of revenue for a Direct Selling Agent \(DSA\) is commission earned from lenders for successfully sourced and disbursed loans\. This revenue is subsequently distributed across connectors, referral partners, employees, sales managers, and incentive programs according to business\-defined rules\.

Commission structures vary significantly across lenders, products, campaigns, branches, regions, and time periods\. They are also subject to frequent revisions due to contractual negotiations and promotional campaigns\.

ODOS requires a flexible and auditable compensation framework capable of supporting complex and evolving business arrangements without requiring application redesign\.

\#\#\#\# Problem Statement

Traditional commission management often relies on spreadsheets or hardcoded logic, leading to:

\- Calculation errors

\- Disputes with connectors and employees

\- Manual effort

\- Delayed payouts

\- Lack of transparency

\- Difficulty implementing new incentive schemes

\- Poor auditability

\- Limited forecasting capability

\#\#\#\# Decision

ODOS shall implement a \*\*Configurable Commission, Incentive and Compensation Engine\*\*\.

The engine shall support calculation, approval, payment, adjustment, and reporting of all commission and incentive\-related transactions through configurable business rules\.

\*\*No lender\-specific or employee\-specific compensation logic shall be hardcoded\*\* within the application\.

\*\*All calculations shall be driven through metadata and rule configuration\.\*\*

\#\#\#\# Scope

\*\*Revenue:\*\*

\- Lender commissions

\- Processing fees

\- Referral income

\- Campaign incentives

\- Bonus income

\- Other business income

\*\*Connector Compensation:\*\*

\- Flat amount

\- Percentage of loan amount

\- Percentage of revenue

\- Slab\-based commission

\- Multi\-level hierarchy payouts

\- Override commissions

\- Special campaign bonuses

\*\*Employee Compensation:\*\*

\- Sales incentives

\- Collection incentives

\- Operations incentives

\- Team incentives

\- Branch incentives

\- Quarterly bonuses

\- Annual performance incentives

\*\*Management Compensation:\*\*

\- Branch Manager incentives

\- Regional Manager overrides

\- National performance incentives

\- Leadership bonuses

\#\#\#\# Compensation Principles

The architecture shall adhere to the following principles:

\- Every commission shall originate from a valid business transaction\.

\- Every calculation shall reference an approved business rule\.

\- Historical rules shall remain preserved after revision\.

\- Changes to future commission structures shall not affect historical calculations\.

\- Multiple compensation models may coexist\.

\- Compensation shall remain fully auditable\.

\- Payment status shall be tracked independently from earned status\.

\#\#\#\# Supported Calculation Models

The engine shall support:

\- Fixed Amount

\- Percentage

\- Slab Based

\- Tier Based

\- Product Based

\- Lender Specific

\- Campaign Specific

\- Branch Specific

\- Region Specific

\- Employee Specific

\- Connector Specific

\- Hybrid Calculations

\- Formula Based

\#\#\#\# Adjustments

The architecture shall support:

\- Clawbacks

\- Negative commissions

\- Reversals

\- Incentive adjustments

\- Bonus corrections

\- Campaign revisions

\- Manual approvals

\- Exceptional payouts

\*\*Original earnings shall always remain preserved\.\*\*

\#\#\#\# Alternatives Considered

| Alternative | Description | Reason for Rejection |

|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Spreadsheet\-Based Compensation | Manual calculations outside the system | Error\-prone, poor governance, difficult reconciliation, limited scalability |

| Hardcoded Compensation Logic | Business rules embedded in software | Difficult to maintain, frequent software releases, poor adaptability |

| Rule\-Based Compensation Engine | Business rules stored as configurable metadata | \*\*Accepted\*\* |

\#\#\#\# Rationale

The selected architecture provides:

\- Flexibility

\- Transparency

\- Reduced disputes

\- Faster payout processing

\- Better forecasting

\- Improved governance

\- Better auditability

\- Easier onboarding of new lenders

\- Improved productization for future tenants

\#\#\#\# Architectural Impact

This decision directly affects:

\- \`RUL\_CommissionRule\`

\- \`RUL\_CommissionSlab\`

\- \`RUL\_InternalIncentiveScheme\`

\- \`RUL\_BusinessRule\`

\- \`TRN\_Revenue\`

\- \`TRN\_Commission\`

\- \`TRN\_CampaignIncentive\`

\- \`TRN\_IncentiveEarned\`

\- \`BI\_Profitability\`

\- \`BI\_Forecast\`

\#\#\#\# Related Architecture Principles

\- Principle 2 – Metadata\-Driven Architecture

\- Principle 3 – Configuration over Hardcoding

\- Principle 6 – Audit by Design

\- Principle 7 – Financial Integrity

\- Principle 11 – Analytics by Design

\#\#\#\# Related ERD Entities

Primary entities include:

\- \`RUL\_CommissionRule\`

\- \`RUL\_CommissionSlab\`

\- \`RUL\_InternalIncentiveScheme\`

\- \`RUL\_BusinessRule\`

\- \`MST\_LenderAgreement\`

\- \`MST\_LenderCampaign\`

\- \`MST\_Product\`

\- \`MST\_Connector\`

\- \`MST\_Employee\`

\- \`TRN\_Case\`

\- \`TRN\_Revenue\`

\- \`TRN\_Commission\`

\- \`TRN\_CampaignIncentive\`

\- \`TRN\_IncentiveEarned\`

\- \`BI\_Profitability\`

\#\#\#\# Implementation Guidance

Implementation shall ensure that:

\- Every commission rule has an effective start and end date\.

\- Historical commission calculations are reproducible\.

\- Rule changes are version\-controlled and audited\.

\- Commission calculations generate detailed calculation logs\.

\- Users can simulate commission outcomes before activating new rules\.

\- Payout approvals follow configurable workflows\.

\- The system supports bulk recalculation where authorised without altering historical approved transactions\.

\- Dashboards provide visibility into earned, approved, payable, paid, reversed, and clawed\-back commissions\.

\-\-\-

\#\#\# 5\.14 ADR\-013: Enterprise Master Data Management Architecture

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*ADR ID\*\* | ADR\-013 |

| \*\*Title\*\* | Adoption of an Enterprise Master Data Management \(MDM\) Architecture |

| \*\*Status\*\* | Accepted |

| \*\*Version\*\* | 1\.0 |

| \*\*Decision Date\*\* | July 2026 |

| \*\*Category\*\* | Data Architecture / Enterprise Governance |

| \*\*Owner\*\* | CTO |

\#\#\#\# Context

ODOS integrates data from multiple internal and external sources, including lender MIS files, connector uploads, manually entered records, APIs, OCR documents, and future integrations\. These sources often contain inconsistent, incomplete, or duplicate information for the same business entities\.

As the enterprise system of record, ODOS must maintain a single, trusted, and governed version of every core business entity to ensure operational consistency, reporting accuracy, and analytical reliability\.

Master Data Management \(MDM\) provides the governance framework necessary to establish and maintain this Single Source of Truth\.

\#\#\#\# Problem Statement

Without a structured Master Data Management framework, organisations experience:

\- Duplicate customer records

\- Multiple spellings of the same lender or connector

\- Inconsistent branch and employee information

\- Reporting discrepancies

\- Duplicate payments

\- Incorrect commission calculations

\- Poor AI learning

\- Difficult integrations

\- Reduced confidence in analytics

\#\#\#\# Decision

ODOS shall implement an \*\*Enterprise Master Data Management \(MDM\) Architecture\*\*\.

Core business entities shall exist only once within the operational database\.

Operational transactions shall reference master records through unique identifiers rather than storing duplicate descriptive information\.

Master records shall be governed through validation, approval, versioning, and controlled update processes\.

\#\#\#\# Scope

\*\*Organisation:\*\*

\- Company

\- Region

\- Branch

\- Team

\- Department

\*\*People:\*\*

\- Customer

\- Employee

\- Connector

\- Vendor

\- Lender Relationship Manager

\*\*Institutions:\*\*

\- Lender

\- Lender Branch

\- Financial Institution

\*\*Products:\*\*

\- Loan Products

\- Schemes

\- Campaigns

\*\*Financial:\*\*

\- Chart of Accounts

\- Cost Centres

\- Profit Centres

\- Tax Codes

\- Bank Accounts

\*\*Reference Data:\*\*

\- Status Codes

\- Workflow Stages

\- Validation Rules

\- Configuration Values

\- Business Rules

\#\#\#\# Master Data Principles

The MDM framework shall adhere to the following principles:

\- Every master entity shall have a unique system\-generated identifier\.

\- Master records shall be reusable across all business processes\.

\- Duplicate master records shall be prevented wherever possible\.

\- Business keys \(e\.g\., PAN, GSTIN, CIN, Account Number\) shall be validated according to applicable standards\.

\- Changes to master data shall be audited\.

\- Master data ownership shall be clearly defined\.

\- Historical references shall remain valid even after master data updates\.

\- Master records shall support logical activation and deactivation rather than physical deletion\.

\#\#\#\# Duplicate Management

ODOS shall include automated duplicate detection based on configurable matching rules\.

Duplicate analysis may consider:

\- PAN

\- Aadhaar \(where legally appropriate and securely handled\)

\- GSTIN

\- CIN

\- Mobile Number

\- Email Address

\- Bank Account

\- IFSC

\- Customer Name

\- Date of Birth

\- Address

\- Lender Code

\- Vendor Code

\#\#\#\# Data Stewardship

Each master entity shall have an identified business owner responsible for:

\- Data quality

\- Approval of changes

\- Duplicate resolution

\- Periodic review

\- Compliance with governance policies

\#\#\#\# Alternatives Considered

| Alternative | Description | Reason for Rejection |

|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Distributed Master Data | Allow each module to maintain its own master records | High duplication, inconsistent reporting, complex maintenance, poor governance |

| Manual Spreadsheet Masters | Maintain master records outside the application | Lack of control, version conflicts, manual errors, limited scalability |

| Centralised Enterprise MDM | Maintain a governed master repository shared by all modules | \*\*Accepted\*\* |

\#\#\#\# Rationale

The selected architecture provides:

\- Single Source of Truth

\- Improved operational consistency

\- Better reporting accuracy

\- Simplified integrations

\- Reduced duplicate records

\- Better AI learning

\- Easier regulatory compliance

\- Improved enterprise governance

\#\#\#\# Architectural Impact

This decision governs all master entities, including:

\- \`MST\_Company\`

\- \`MST\_InternalRegion\`

\- \`MST\_InternalBranch\`

\- \`MST\_Team\`

\- \`MST\_Employee\`

\- \`MST\_Customer\`

\- \`MST\_Lender\`

\- \`MST\_LenderBranch\`

\- \`MST\_LenderRM\`

\- \`MST\_Product\`

\- \`MST\_Connector\`

\- \`MST\_Vendor\`

\- \`MST\_CompanyBankAccount\`

\- \`MST\_ChartOfAccounts\`

\#\#\#\# Related Architecture Principles

\- Principle 1 – Single Source of Truth

\- Principle 2 – Metadata\-Driven Architecture

\- Principle 5 – AI\-Assisted, Human\-Governed Processing

\- Principle 6 – Audit by Design

\#\#\#\# Related ERD Entities

Primary entities include:

\- All \`MST\_\*\` tables

\- \`META\_FieldDefinition\`

\- \`META\_FieldMapping\`

\- \`ETL\_DuplicateQueue\`

\- \`ETL\_DataQualityScore\`

\- \`AI\_Mapping\`

\- \`AI\_Learning\`

\- \`SEC\_AuditTrail\`

\#\#\#\# Implementation Guidance

Implementation shall ensure that:

\- Every master record is assigned a globally unique identifier\.

\- Business key validation is performed before record creation\.

\- Duplicate detection rules are configurable and continuously refined\.

\- Changes to master records follow approval workflows where required\.

\- Master records support effective dating and version history where business\-critical\.

\- Soft deletion \(\`IsActive\`, \`IsDeleted\`\) is used in preference to physical deletion\.

\- Master data quality metrics are monitored and reported through dashboards\.

\- Import processes attempt to match existing master records before creating new ones\.

\-\-\-

\#\#\# 5\.15 ADR\-014: Enterprise Data Quality and Validation Framework

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*ADR ID\*\* | ADR\-014 |

| \*\*Title\*\* | Adoption of an Enterprise Data Quality and Validation Framework |

| \*\*Status\*\* | Accepted |

| \*\*Version\*\* | 1\.0 |

| \*\*Decision Date\*\* | July 2026 |

| \*\*Category\*\* | Data Governance / ETL / Quality Assurance |

| \*\*Owner\*\* | CTO |

\#\#\#\# Context

ODOS is designed as a metadata\-driven enterprise platform where operational data is ingested from multiple heterogeneous sources, including lender MIS files, connector reports, manually maintained Excel workbooks, OCR outputs, APIs, and direct user entry\.

The quality of enterprise decisions depends entirely upon the quality of underlying data\. Therefore, data validation cannot be treated as a one\-time import activity but must be an ongoing governance process throughout the data lifecycle\.

\#\#\#\# Problem Statement

Incoming data frequently contains:

\- Missing mandatory fields

\- Invalid PAN/GSTIN/IFSC

\- Duplicate customers

\- Duplicate loan cases

\- Incorrect lender codes

\- Invalid dates

\- Incorrect numeric values

\- Inconsistent product names

\- Typographical errors

\- Different naming conventions

\- Incomplete financial information

\- Contradictory values across uploads

Without systematic validation, these issues propagate into:

\- Incorrect commissions

\- Wrong profitability

\- Cash\-flow errors

\- Poor analytics

\- AI learning failures

\- Management mistrust

\#\#\#\# Decision

ODOS shall implement a \*\*multi\-stage enterprise data quality framework\*\*\.

Validation shall occur before, during, and after data ingestion\.

No operational transaction shall enter the production database without passing mandatory validation checks or being explicitly approved through an exception workflow\.

\#\#\#\# Validation Pipeline

\*\*Stage 1 – File Validation:\*\*

\- File type

\- Sheet structure

\- Mandatory worksheets

\- Duplicate upload detection

\- Version identification

\*\*Stage 2 – Structural Validation:\*\*

\- Header mapping

\- Required columns

\- Data type verification

\- Column count

\- Template recognition

\*\*Stage 3 – Business Validation:\*\*

\- Mandatory fields

\- Referential integrity

\- Master lookup

\- Financial consistency

\- Business rule validation

\*\*Stage 4 – Duplicate Detection:\*\*

\- Customer duplicates

\- Case duplicates

\- Invoice duplicates

\- Payment duplicates

\- Document duplicates

\*\*Stage 5 – Data Quality Scoring:\*\*

\- Each batch receives a quality score

\*\*Stage 6 – Exception Review:\*\*

\- User reviews unresolved issues

\*\*Stage 7 – Production Import:\*\*

\- Validated data moves into operational tables

\#\#\#\# Data Quality Dimensions

ODOS shall evaluate:

\- Completeness

\- Accuracy

\- Consistency

\- Validity

\- Uniqueness

\- Timeliness

\- Integrity

\- Traceability

\#\#\#\# Severity Levels

Validation issues shall be classified as:

\*\*Critical \(Import blocked\):\*\*

\- Missing Customer

\- Invalid PAN

\- Missing Loan Amount

\- Unknown Lender

\*\*High \(Requires approval\):\*\*

\- Duplicate customer

\- Duplicate invoice

\- Missing branch

\*\*Medium \(Imported with warning\):\*\*

\- Missing email

\- Missing alternate phone

\*\*Low \(Informational only\):\*\*

\- Optional remarks missing

\#\#\#\# Data Quality Score

Each import batch shall receive:

\- Overall Score

\- Completeness Score

\- Validation Score

\- Duplicate Score

\- Master Match Score

\- Financial Score

\#\#\#\# Exception Management

Failed records shall never disappear\. They shall remain within:

\- \`ETL\_ErrorLog\`

\- \`ETL\_DuplicateQueue\`

\- \`ETL\_DataQualityScore\`

Users may:

\- Correct

\- Approve

\- Reject

\- Reprocess

\#\#\#\# Architectural Impact

This decision directly affects:

\- \`ETL\_ImportBatch\`

\- \`ETL\_StagingRawData\`

\- \`ETL\_ErrorLog\`

\- \`ETL\_DuplicateQueue\`

\- \`ETL\_DataQualityScore\`

\- \`META\_FieldMapping\`

\- \`META\_ValidationRule\`

\- \`AI\_Mapping\`

\- \`AI\_Learning\`

\#\#\#\# Related Architecture Principles

\- Principle 1 – Single Source of Truth

\- Principle 2 – Metadata\-Driven Architecture

\- Principle 4 – ETL\-First Data Processing

\- Principle 5 – AI\-Assisted, Human\-Governed Processing

\- Principle 6 – Audit by Design

\#\#\#\# Implementation Guidance

Implementation shall ensure:

\- Validation rules are metadata\-driven\.

\- Rules are configurable without code changes\.

\- Validation results are explainable\.

\- Imports are repeatable\.

\- Failed records can be corrected and reprocessed\.

\- Data quality improves through AI learning and user feedback\.

\-\-\-

\#\#\# 5\.16 ADR\-015: AI\-Assisted Data Mapping and Continuous Learning Architecture

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*ADR ID\*\* | ADR\-015 |

| \*\*Title\*\* | Adoption of an AI\-Assisted Data Mapping and Continuous Learning Architecture |

| \*\*Status\*\* | Accepted |

| \*\*Version\*\* | 1\.0 |

| \*\*Decision Date\*\* | July 2026 |

| \*\*Category\*\* | Artificial Intelligence / Data Integration / Metadata Architecture |

| \*\*Owner\*\* | CTO |

\#\#\#\# Context

One of the primary objectives of ODOS is to simplify the ingestion of operational data from diverse external sources without requiring users to repeatedly redesign import templates or manually map columns\.

Lender MIS files, connector reports, customer spreadsheets, and operational workbooks vary significantly in structure, naming conventions, data quality, and format\. These differences make traditional fixed\-template import processes inefficient and difficult to maintain\.

ODOS shall therefore incorporate an AI\-assisted learning framework that continuously improves its ability to recognise file structures, map fields, detect patterns, and recommend import actions while ensuring that final business decisions remain under human control\.

\#\#\#\# Problem Statement

Traditional import systems suffer from several limitations:

\- Every new lender template requires manual mapping\.

\- Small header changes break imports\.

\- Users repeatedly answer the same mapping questions\.

\- Duplicate detection is inconsistent\.

\- Business knowledge is not retained\.

\- Improvements depend on software updates\.

\- Import quality varies between users\.

\#\#\#\# Decision

ODOS shall implement an \*\*AI\-Assisted Data Mapping and Continuous Learning Architecture\*\*\.

\*\*The system shall:\*\*

\- Learn file structures over time

\- Learn successful mappings

\- Learn user corrections

\- Learn duplicate resolution decisions

\- Learn validation exceptions

\- Recommend mappings automatically

\- Continuously improve mapping confidence

\*\*Final acceptance of mappings and business decisions shall always require human approval\*\* where material business impact exists\.

\#\#\#\# Learning Objectives

\*\*File Recognition:\*\*

\- Lender identification

\- Connector identification

\- Template recognition

\- Version detection

\*\*Column Mapping:\*\*

\- Recognise equivalent fields:

  \- "Loan No" → "Application Number" → "Case ID" → "Proposal No" → "Reference Number" → "Internal Case Number"

\*\*Value Standardisation:\*\*

\- "HDFC" → "HDFC Bank" → "HDFC Ltd" → Standardised Master Record

\*\*Duplicate Detection:\*\*

\- Learn duplicate resolution decisions based on:

  \- Customer

  \- Loan

  \- PAN

  \- Mobile

  \- Invoice

  \- Payment

  \- Document

\*\*Validation Behaviour:\*\*

\- Learn common corrections made by users

\*\*Import Preferences:\*\*

\- Remember organisation\-specific mapping behaviour

\#\#\#\# Human Governance

ODOS shall follow a \*\*Human\-in\-the\-Loop model\*\*\.

\*\*AI May:\*\*

\- Recommend

\- Predict

\- Suggest

\- Rank

\- Flag

\*\*AI Shall Not:\*\*

\- Approve financial postings

\- Merge master records automatically

\- Delete operational records

\- Override business rules

\- Modify approved transactions

\*\*Final authority always remains with authorised users\.\*\*

\#\#\#\# Knowledge Repository

The learning engine shall maintain knowledge regarding:

\- File Signatures

\- Header Variations

\- Mapping History

\- Successful Imports

\- Duplicate Decisions

\- User Corrections

\- Validation Overrides

\- Confidence Scores

\- Import Statistics

\#\#\#\# Confidence Scoring

Every recommendation shall include a confidence score\.

\*\*Example:\*\*

\`\`\`

Header Mapping: "Customer Name" → "Borrower Name"

Confidence: 98%

Duplicate Detection: Customer A → Customer B

Confidence: 94%

\`\`\`

Users shall be able to accept, modify, or reject recommendations\.

\#\#\#\# Learning Lifecycle

\`\`\`

File Upload

    ↓

Metadata Recognition

    ↓

Template Matching

    ↓

AI Mapping

    ↓

Validation

    ↓

User Review

    ↓

Corrections

    ↓

Knowledge Update

    ↓

Future Improvement

\`\`\`

\#\#\#\# Architectural Impact

This decision directly affects:

\- \`AI\_Metadata\`

\- \`AI\_Mapping\`

\- \`AI\_Learning\`

\- \`AI\_Feedback\`

\- \`META\_FieldMapping\`

\- \`META\_ImportTemplate\`

\- \`ETL\_ImportBatch\`

\- \`ETL\_DataLineage\`

\- \`ETL\_DuplicateQueue\`

\- \`ETL\_DataQualityScore\`

\#\#\#\# Related Architecture Principles

\- Principle 2 – Metadata\-Driven Architecture

\- Principle 3 – Configuration over Hardcoding

\- Principle 5 – AI\-Assisted, Human\-Governed Processing

\- Principle 6 – Audit by Design

\#\#\#\# Implementation Guidance

Implementation shall ensure:

\- AI recommendations are explainable\.

\- Learning is tenant\-specific by default\.

\- Confidence scores are recorded\.

\- User decisions become training inputs\.

\- AI never modifies approved data without authorisation\.

\- Every recommendation is auditable\.

\- Learning models can be reset or retrained when required\.

\-\-\-

\#\#\# 5\.17 ADR\-016: Enterprise Document Management and OCR Architecture

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*ADR ID\*\* | ADR\-016 |

| \*\*Title\*\* | Adoption of an Enterprise Document Management and OCR Architecture |

| \*\*Status\*\* | Accepted |

| \*\*Version\*\* | 1\.0 |

| \*\*Decision Date\*\* | July 2026 |

| \*\*Category\*\* | Document Management / Enterprise Content Management |

| \*\*Owner\*\* | CTO |

\#\#\#\# Context

ODOS manages a wide range of business documents generated throughout the DSA lifecycle\. These include customer KYC documents, loan application forms, sanction letters, invoices, lender statements, payment proofs, agreements, operational correspondence, and uploaded MIS files\.

Traditionally, these documents are stored in disparate folders or email systems, making retrieval, verification, auditing, and reconciliation difficult\.

To support paperless operations, enterprise governance, and AI\-assisted processing, ODOS shall provide an integrated document management architecture\.

\#\#\#\# Problem Statement

Without a structured document architecture, organisations face:

\- Lost documents

\- Duplicate document storage

\- Manual searching

\- Version confusion

\- Poor auditability

\- Missing compliance evidence

\- Difficulty linking documents to transactions

\- Limited automation

\- Inconsistent document naming

\#\#\#\# Decision

ODOS shall implement a centralised \*\*Enterprise Document Management Architecture\*\*\.

Every business document shall be registered, classified, version\-controlled, and linked to its relevant business entities\.

Documents shall be treated as enterprise assets rather than external file attachments\.

\#\#\#\# Scope

\*\*Customer:\*\*

\- PAN

\- Aadhaar

\- Photograph

\- Address Proof

\- Bank Statements

\- Salary Slips

\- Income Tax Returns

\- KYC Forms

\*\*Loan Processing:\*\*

\- Application Forms

\- Sanction Letters

\- Offer Letters

\- Disbursement Advice

\- Agreement Copies

\- Insurance Documents

\*\*Financial:\*\*

\- Invoices

\- Payment Advice

\- Bank Statements

\- UTR Confirmations

\- GST Documents

\- TDS Certificates

\*\*Operations:\*\*

\- MIS Files

\- Excel Uploads

\- CSV Files

\- PDF Reports

\- Email Attachments

\*\*Internal:\*\*

\- Policies

\- SOPs

\- Circulars

\- Contracts

\- Vendor Agreements

\#\#\#\# Document Principles

The architecture shall ensure:

\- Every document has a unique identifier\.

\- Every document is linked to one or more business entities\.

\- Original files remain preserved\.

\- Multiple document versions are supported\.

\- Duplicate files are detected using cryptographic hashing\.

\- Document metadata is searchable\.

\- Access is controlled through role\-based security\.

\- Document history is auditable\.

\#\#\#\# OCR Integration

Where applicable, documents shall undergo OCR processing to extract searchable text\.

\*\*Extracted information may include:\*\*

\- PAN Number

\- Customer Name

\- Loan Number

\- Invoice Number

\- Account Number

\- Amount

\- Dates

\- GSTIN

\- UTR Number

\*\*Rules:\*\*

\- OCR results shall never overwrite original documents\.

\- Extracted values shall be subject to validation before operational use\.

\#\#\#\# Document Classification

Documents shall be classified using configurable metadata, including:

\- Document Type

\- Category

\- Business Entity

\- Company

\- Branch

\- Customer

\- Case

\- Lender

\- Vendor

\- Financial Year

\- Confidentiality Level

\- Expiry Date

\- Verification Status

\#\#\#\# Version Management

ODOS shall maintain:

\- Original Version

\- Current Version

\- Version History

\- Upload Date

\- Uploaded By

\- Approval Status

\- Verification Status

\*\*Historical versions shall remain accessible\*\* for audit purposes\.

\#\#\#\# Architectural Impact

This decision directly affects:

\- \`AUD\_Document\`

\- \`AUD\_FileRepository\`

\- \`ETL\_ImportBatch\`

\- \`ETL\_StagingRawData\`

\- \`ETL\_DataLineage\`

\- \`AI\_Metadata\`

\- \`AI\_Learning\`

\- \`SEC\_AuditTrail\`

\#\#\#\# Related Architecture Principles

\- Principle 1 – Single Source of Truth

\- Principle 6 – Audit by Design

\- Principle 5 – AI\-Assisted, Human\-Governed Processing

\- Principle 2 – Metadata\-Driven Architecture

\#\#\#\# Implementation Guidance

Implementation shall ensure:

\- Files are stored outside the database where practical, with the database storing metadata and secure references\.

\- Each file is identified by a cryptographic hash \(e\.g\., SHA\-256\) to detect duplicates and verify integrity\.

\- Role\-based permissions control document access\.

\- OCR extraction results are stored separately from the original document\.

\- Every upload is linked to an ImportBatch where applicable\.

\- Retention and archival policies are configurable\.

\- Deleted documents are soft\-deleted and remain recoverable until retention policies permit permanent removal\.

\-\-\-

\#\#\# 5\.18 ADR\-017: Enterprise Analytics, Business Intelligence and Decision Intelligence Architecture

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*ADR ID\*\* | ADR\-017 |

| \*\*Title\*\* | Adoption of an Enterprise Analytics, Business Intelligence and Decision Intelligence Architecture |

| \*\*Status\*\* | Accepted |

| \*\*Version\*\* | 1\.0 |

| \*\*Decision Date\*\* | July 2026 |

| \*\*Category\*\* | Business Intelligence / Enterprise Analytics |

| \*\*Owner\*\* | CTO |

\#\#\#\# Context

ODOS is intended to be the enterprise operating system for Direct Selling Agents \(DSAs\), supporting operational execution, financial management, compliance, and strategic decision\-making\.

Operational data alone has limited value unless it can be transformed into timely, accurate, and actionable insights\. The architecture must therefore provide a comprehensive analytics framework that enables users at all organisational levels to monitor performance, identify trends, detect risks, and make informed decisions\.

Analytics shall be an integral capability of the platform rather than a separate reporting layer\.

\#\#\#\# Problem Statement

Organisations relying on spreadsheets and disconnected reports often experience:

\- Delayed management information

\- Inconsistent KPIs

\- Multiple versions of the truth

\- Manual report preparation

\- Poor visibility into profitability

\- Limited forecasting

\- Reactive decision\-making

\- Difficulty identifying operational bottlenecks

\#\#\#\# Decision

ODOS shall implement an \*\*Enterprise Analytics and Decision Intelligence Architecture\*\*\.

Analytics shall be generated from governed operational data and presented through configurable dashboards, reports, scorecards, and forecasting models\.

The architecture shall support descriptive, diagnostic, predictive, and prescriptive analytics while maintaining complete traceability to source transactions\.

\#\#\#\# Analytics Principles

The analytics framework shall adhere to the following principles:

\- All reports shall use governed enterprise data\.

\- KPIs shall have standardised definitions\.

\- Every metric shall be traceable to source transactions\.

\- Dashboards shall refresh automatically\.

\- Analytics shall support drill\-down to transaction level\.

\- Historical snapshots shall be preserved\.

\- Forecasts shall distinguish between actual and projected values\.

\- AI\-generated insights shall be explainable\.

\#\#\#\# Scope

\*\*Executive Analytics:\*\*

\- Revenue

\- Profitability

\- Cash Flow

\- Working Capital

\- Business Growth

\- Forecast Accuracy

\*\*Sales Analytics:\*\*

\- Leads

\- Conversion Ratios

\- Pipeline

\- Disbursement

\- Product Mix

\- Lender Performance

\*\*Financial Analytics:\*\*

\- Revenue

\- Expenses

\- Gross Margin

\- Net Margin

\- Cost\-to\-Income Ratio

\- Branch Profitability

\- Collection Efficiency

\*\*Operational Analytics:\*\*

\- TAT

\- Pending Cases

\- SLA Compliance

\- Productivity

\- Workload

\- Exception Management

\*\*Customer Analytics:\*\*

\- Customer Segmentation

\- Repeat Business

\- Geographic Distribution

\*\*Risk Analytics:\*\*

\- Lender Risk

\- Concentration Risk

\- Portfolio Risk

\- Working Capital Exposure

\- Payment Delays

\- Outstanding Receivables

\*\*AI Analytics:\*\*

\- Mapping Accuracy

\- Learning Progress

\- Validation Accuracy

\- Duplicate Detection Performance

\- User Acceptance Rate

\#\#\#\# KPI Framework

Every KPI shall define:

\- KPI Code

\- Name

\- Business Definition

\- Formula

\- Frequency

\- Target

\- Thresholds

\- Owner

\- Source Tables

\- Reporting Level

\- Version

\*\*KPIs shall be centrally managed\*\* to ensure consistency across reports\.

\#\#\#\# Dashboard Architecture

Dashboards shall be role\-based and configurable\.

\*\*Examples:\*\*

\- Executive Dashboard

\- CEO Dashboard

\- Branch Manager Dashboard

\- Sales Dashboard

\- Operations Dashboard

\- Finance Dashboard

\- Collections Dashboard

\- Compliance Dashboard

\- AI Learning Dashboard

\*\*Each dashboard shall support filtering by:\*\*

\- Company

\- Region

\- Branch

\- Lender

\- Product

\- Employee

\- Connector

\- Time Period

\#\#\#\# Forecasting

ODOS shall support forecasting for:

\- Revenue

\- Cash Flow

\- Collections

\- Disbursements

\- Expenses

\- Working Capital

\- Incentive Liability

\- Branch Performance

\*\*Forecasts shall clearly distinguish projected values from actual results\.\*\*

\#\#\#\# Architectural Impact

This decision directly affects:

\- \`BI\_DailySnapshot\`

\- \`BI\_MonthlySnapshot\`

\- \`BI\_Profitability\`

\- \`BI\_PortfolioRiskSnapshot\`

\- \`BI\_Forecast\`

\- \`BI\_KPI\`

\- \`META\_ReportDefinition\`

\- \`META\_DashboardDefinition\`

\- \`AI\_Learning\`

\- \`ETL\_DataQualityScore\`

\#\#\#\# Related Architecture Principles

\- Principle 1 – Single Source of Truth

\- Principle 2 – Metadata\-Driven Architecture

\- Principle 7 – Financial Integrity

\- Principle 6 – Audit by Design

\- Principle 11 – Analytics by Design

\#\#\#\# Implementation Guidance

Implementation shall ensure:

\- Dashboards use pre\-aggregated snapshot tables where appropriate\.

\- Complex calculations are centralised to ensure consistency\.

\- Reports support export to Excel, PDF, and other common formats\.

\- Historical snapshots are retained to support trend analysis\.

\- Drill\-down from summary metrics to underlying transactions is available\.

\- Data quality indicators accompany analytical outputs where appropriate\.

\-\-\-

\#\#\# 5\.19 ADR\-018: Platform Evolution, Scalability and Technology Strategy

| Field | Detail |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| \*\*ADR ID\*\* | ADR\-018 |

| \*\*Title\*\* | Adoption of a Platform Evolution, Scalability and Technology Strategy |

| \*\*Status\*\* | Accepted |

| \*\*Version\*\* | 1\.0 |

| \*\*Decision Date\*\* | July 2026 |

| \*\*Category\*\* | Enterprise Technology Architecture |

| \*\*Owner\*\* | CTO |

\#\#\#\# Context

ODOS is initially being developed as an internal operating system for a single Direct Selling Agent \(DSA\)\. The long\-term vision is to evolve it into a commercial enterprise platform that can serve multiple DSAs, financial intermediaries, and potentially adjacent financial services organisations\.

The architecture must therefore support phased growth without requiring fundamental redesign\.

Technology choices shall balance simplicity for the initial implementation with a clear migration path to enterprise\-scale deployment\.

\#\#\#\# Problem Statement

Many business applications become difficult to scale because early architectural decisions assume:

\- Single user operation

\- Single organisation

\- Limited data volume

\- Desktop\-only deployment

\- Tight coupling between components

\- Database\-specific implementation

These assumptions create significant technical debt as the application grows\.

ODOS shall avoid such constraints by adopting an evolution\-oriented architecture from inception\.

\#\#\#\# Decision

ODOS shall adopt a \*\*Progressive Evolution Strategy\*\*, whereby the initial implementation prioritises simplicity and rapid delivery while preserving the ability to scale into an enterprise\-grade, multi\-tenant platform\.

The architecture shall be technology\-agnostic wherever practical, with clear separation between business logic, data, presentation, and integration layers\.

\#\#\#\# Platform Evolution Roadmap

\*\*Phase 1 – Internal Desktop Application:\*\*

\- Single organisation deployment

\- SQLite database \(initial\)

\- Python backend

\- Visual Studio\-based development

\- Excel\-driven ETL

\- AI\-assisted data mapping

\*\*Phase 2 – Enterprise Internal Platform:\*\*

\- Multi\-user access

\- Enhanced security

\- Scheduled ETL

\- API integrations

\- Improved reporting

\- Performance optimisation

\*\*Phase 3 – Commercial SaaS Platform:\*\*

\- Multi\-tenancy

\- PostgreSQL or equivalent enterprise database

\- Web\-based user interface

\- Cloud deployment

\- Customer self\-service

\- Subscription management

\#\#\#\# Scalability Principles

ODOS shall be designed to scale across:

\- Users

\- Companies

\- Branches

\- Lenders

\- Products

\- Cases

\- Documents

\- Import volumes

\- Analytics workloads

\- AI models

\*\*Scalability shall be achieved through architectural evolution rather than redesign\.\*\*

\#\#\#\# Technology Principles

Technology choices shall adhere to the following principles:

\- Business logic shall remain independent of the database platform\.

\- Database access shall be abstracted through a repository or service layer\.

\- Configuration shall be metadata\-driven\.

\- Business rules shall not be hardcoded\.

\- Components shall be modular and loosely coupled\.

\- External integrations shall use standard interfaces where possible\.

\- Open standards shall be preferred over proprietary technologies\.

\#\#\#\# Database Evolution Strategy

The platform shall support migration through progressively larger database platforms\.

\*\*Expected path:\*\*

\`\`\`

SQLite

    ↓

PostgreSQL

    ↓

Enterprise RDBMS \(if required\)

\`\`\`

\*\*The data model shall remain portable\*\* to minimise migration effort\.

\#\#\#\# Deployment Strategy

The architecture shall support:

\- Local desktop deployment

\- Shared network deployment

\- On\-premises server deployment

\- Private cloud deployment

\- Public cloud deployment

\- SaaS deployment

\*\*Deployment shall not require changes to the underlying business model\.\*\*

\#\#\#\# Security and Resilience

The platform shall support:

\- Role\-based access control

\- Encryption of sensitive data

\- Secure authentication

\- Backup and recovery

\- Disaster recovery planning

\- Audit logging

\- Secure configuration management

\- High availability in future deployments

\#\#\#\# Architectural Impact

This decision influences all architectural layers, including:

\- Metadata

\- Configuration

\- Security

\- Masters

\- Rules

\- Transactions

\- ETL

\- Audit

\- Analytics

\- AI

\*\*All future enhancements shall preserve compatibility with this evolution strategy\.\*\*

\#\#\#\# Related Architecture Principles

\- Principle 2 – Metadata\-Driven Architecture

\- Principle 3 – Configuration over Hardcoding

\- Principle 8 – Multi\-Tenant by Design

\- Principle 6 – Audit by Design

\- Principle 5 – AI\-Assisted, Human\-Governed Processing

\#\#\#\# Implementation Guidance

Implementation shall ensure that:

\- SQL remains portable and standards\-compliant where practical\.

\- Database\-specific features are isolated\.

\- File storage is abstracted to support local or cloud repositories\.

\- Configuration values are externalised\.

\- APIs are designed with versioning in mind\.

\- Performance metrics are monitored as the platform grows\.

\- Backup, restore, and migration procedures are documented and tested\.

\-\-\-

\#\# 6\. Architecture Gap Analysis & Resolution Register

\#\#\# 6\.1 Purpose

This section documents all identified architectural gaps from the legacy documentation review and provides their resolution status\. This ensures that no important knowledge is lost and all gaps are either addressed or formally deferred\.

\#\#\# 6\.2 Gap Identification Methodology

Gaps were identified through:

1\. \*\*Document Review\*\* – Comparison of legacy documentation against the new repository structure

2\. \*\*Completeness Assessment\*\* – Verification that all required architectural domains are covered

3\. \*\*Consistency Check\*\* – Validation that no contradictions exist across documents

4\. \*\*Traceability Validation\*\* – Ensuring all decisions trace to business requirements

\#\#\# 6\.3 Gap Resolution Register

| ID | Area | Gap Description | Impact | Status | Resolution |

|\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|

| \*\*GAP\-001\*\* | Repository Governance | Repository governance not explicitly stated in DOC\-001 | Medium | ✅ Resolved | Added governance section to DOC\-001 |

| \*\*GAP\-002\*\* | Master Index | No complete master index in legacy | High | ✅ Resolved | DOC\-003 created |

| \*\*GAP\-003\*\* | Dependency Matrix | Cross\-document dependencies not fully documented | High | ✅ Resolved | DOC\-002 created |

| \*\*GAP\-004\*\* | AI Context Loading | AI context loading protocol not fully defined | Medium | ✅ Resolved | DOC\-004 includes context loading |

| \*\*GAP\-005\*\* | Implementation Pack Template | Implementation Pack structure not fully defined | High | ✅ Resolved | DOC\-008 created |

| \*\*GAP\-006\*\* | Glossary Versioning | Glossary versioning strategy not explicitly defined | Medium | ✅ Resolved | Added to DOC\-009 |

| \*\*GAP\-007\*\* | ADR Versioning | ADR versioning strategy not explicitly defined | Medium | ✅ Resolved | Added to DOC\-009 |

| \*\*GAP\-008\*\* | Change Management | Change management process detailed | High | ✅ Resolved | DOC\-007 includes change management |

| \*\*GAP\-009\*\* | Sprint Retrospective | Sprint retrospective process detailed | Medium | ✅ Resolved | DOC\-007 includes retrospective |

| \*\*GAP\-010\*\* | Knowledge Base Update | Knowledge Base update process defined | Medium | ✅ Resolved | Added to DOC\-004 |

\#\#\# 6\.4 Deferred Gaps \(Future Versions\)

| ID | Area | Gap Description | Target Version | Rationale |

|\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|

| \*\*GAP\-011\*\* | LLM Integration | LLM integration strategy not fully defined | V2\.0 | Requires further research and market analysis |

| \*\*GAP\-012\*\* | Mobile Offline Sync | Mobile offline synchronisation strategy not defined | V2\.0 | Outside initial scope |

| \*\*GAP\-013\*\* | Digital Signatures | Digital signature integration strategy not defined | V1\.1 | External dependency, requires vendor evaluation |

| \*\*GAP\-014\*\* | Collections Module | Collections and recovery module not defined | V1\.1\+ | Outside initial DSA scope |

| \*\*GAP\-015\*\* | Microservices | Microservices architecture strategy not defined | V3\.0 | Not required for initial deployment |

| \*\*GAP\-016\*\* | Cross\-Tenant AI Learning | Cross\-tenant AI learning strategy not defined | V3\.0 | Requires privacy and consent framework |

| \*\*GAP\-017\*\* | Event Sourcing | Event sourcing / CDC strategy not defined | V3\.0 | Not required for initial deployment |

| \*\*GAP\-018\*\* | Message Queue | Message queue / async processing strategy not defined | V2\.0 | Batch processing sufficient for initial scope |

\#\#\# 6\.5 Gap Resolution Summary

| Category | Gaps Identified | Resolved | Deferred |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|

| Repository Governance | 5 | 5 | 0 |

| AI Governance | 2 | 2 | 0 |

| Implementation | 3 | 3 | 0 |

| Future Enhancements | 8 | 0 | 8 |

| \*\*Total\*\* | \*\*18\*\* | \*\*10\*\* | \*\*8\*\* |

\-\-\-

\#\# 7\. Architecture Addendum – Industry\-Agnostic Core & Configurable Industry Layer

\#\#\# 7\.1 Purpose

This addendum supplements the approved ODOS Enterprise Architecture by clarifying the operational philosophy for enterprise data acquisition, processing, governance, and long\-term evolution across multiple industries\.

It does not modify the approved architecture but clarifies the architectural boundary between the Core Engine and the Configurable Layer\.

\#\#\# 7\.2 Core Architectural Principle

\*\*ODOS is not an Excel import application\.\*\*

\*\*ODOS is an AI\-assisted, metadata\-driven Enterprise Operating System\*\* whose primary objective is to establish and continuously maintain a trusted Enterprise Source of Truth\.

External data sources are acquisition channels only\.

\*\*The Source of Truth is the governed enterprise database\.\*\*

\#\#\# 7\.3 Enterprise Data Source Independence

The architecture is intentionally independent of the origin of data\.

\*\*Supported acquisition channels include:\*\*

\- Excel

\- CSV

\- PDF / OCR

\- Manual Data Entry

\- API Integrations

\- Database Connections

\- Email Attachments

\- LOS Exports

\- CRM Systems

\- Future Connectors

\*\*Every acquisition channel shall use the same enterprise processing framework\.\*\*

\*\*No acquisition channel shall bypass governance\.\*\*

\#\#\# 7\.4 Enterprise Processing Pipeline

Every record entering ODOS shall pass through the following logical processing stages:

\`\`\`

Data Acquisition

File Identification

Metadata Recognition

Field Mapping

Data Standardization \(Scrubbing\)

Validation

Duplicate Detection

Business Rule Processing

Confidence Scoring

Human Review \(where required\)

Approval

Posting to Enterprise Source of Truth

Audit Logging

Data Lineage Capture

AI Learning

Analytics & Reporting

\`\`\`

\*\*This pipeline is mandatory regardless of the acquisition source\.\*\*

\#\#\# 7\.5 Source of Truth Principle

\- Only validated and approved data shall populate enterprise master and transaction tables\.

\- Raw imported data shall remain available within ETL staging tables for traceability and audit\.

\- No dashboard, report, KPI, forecast, or AI model shall consume unvalidated staging data\.

\#\#\# 7\.6 Progressive Digital Transformation

The architecture supports three implementation phases without structural changes\.

\*\*Phase 1 – Legacy Integration:\*\*

\- Primary acquisition through existing MIS files

\- Objective: Rapid implementation using current business processes

\*\*Phase 2 – Hybrid Operations:\*\*

\- Business users gradually begin entering operational data directly into ODOS while external MIS imports continue

\- Both acquisition methods feed the same enterprise processing pipeline

\*\*Phase 3 – Native Digital Enterprise:\*\*

\- Operational data originates primarily within ODOS

\- External integrations remain supported for lenders, accounting systems, regulators, and partners

\- The processing pipeline remains unchanged

\#\#\# 7\.7 AI Learning Framework

Artificial Intelligence shall be embedded from the initial implementation\.

\*\*AI shall continuously learn from:\*\*

\- Mapping corrections

\- Duplicate resolutions

\- Validation overrides

\- User feedback

\- Import history

\- File structures

\- Metadata evolution

\*\*Learning shall improve automation while maintaining mandatory human governance\.\*\*

\#\#\# 7\.8 Confidence\-Driven Governance

Each processing stage shall generate measurable confidence indicators\.

\*\*Examples:\*\*

\- File Recognition Confidence

\- Mapping Confidence

\- Validation Score

\- Duplicate Confidence

\- Data Quality Score

\- Overall Import Confidence

\*\*Dashboards may expose these confidence measures\*\* to enable informed business decisions\.

\#\#\# 7\.9 Metadata\-Driven Design

Business rules, mappings, validation logic, and processing behaviour shall be configurable through metadata wherever practical\.

\*\*Hardcoded business logic shall be minimised\.\*\*

\#\#\# 7\.10 Rule Engine Principle

Financial calculations shall be executed through configurable business rules rather than embedded application logic\.

\*\*Examples:\*\*

\- Commission

\- GST

\- TDS

\- Incentives

\- Working Capital

\- Campaign Benefits

\- SLA Calculations

\- Risk Scoring

\*\*This enables changes without requiring software redevelopment\.\*\*

\#\#\# 7\.11 Data Governance

Every enterprise record shall support:

\- Audit Trail

\- Data Lineage

\- Source Identification

\- Import Batch Traceability

\- Version Control

\- User Accountability

\*\*The complete lifecycle of every business record shall remain traceable\.\*\*

\#\#\# 7\.12 Architectural Outcome

ODOS shall evolve from:

\`\`\`

Legacy MIS Import

    → Hybrid Enterprise Platform

    → Native Digital Operating System

\`\`\`

\*\*without requiring redesign of the enterprise data model\.\*\*

\*\*The Enterprise Source of Truth shall remain the single authoritative repository\*\* throughout every stage of organisational maturity\.

\#\#\# 7\.13 Impact Assessment

This addendum introduces \*\*no structural changes to the approved architecture\*\*\.

No table additions or removals are required\.

\*\*The document clarifies the intended operational use\*\* of the approved architecture and serves as implementation guidance for ETL, Rule Engine, AI Learning, and Dashboard development\.

\-\-\-

\#\# 8\. Document Status & Approval

\#\#\# 8\.1 Document Status

| Status | Approved / Frozen |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \*\*Version\*\* | 1\.0 |

| \*\*Date\*\* | July 2026 |

| \*\*Next Review\*\* | Annual or before major architectural change |

| \*\*Owner\*\* | CTO |

\#\#\# 8\.2 Document Freeze Notice

\*\*This document is designated as an Architecture Baseline Artefact\.\*\*

\*\*Following approval:\*\*

\- Structural changes to the Enterprise Architecture require a new Architecture Decision Record \(ADR\)\.

\- Structural changes to the Architecture Principles require Architecture Review Board \(ARB\) approval\.

\- All implementation shall use this document as the governing architecture baseline\.

\- All implementation teams shall treat this document as frozen unless superseded by a formally approved revision\.

\*\*Freeze Status:\*\* ✅ \*\*FROZEN\*\*

\#\#\# 8\.3 Approval Sign\-Off

| Role | Name | Signature | Date |

|\-\-\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-|

| Enterprise Architect | Architecture Review Board | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

| Solution Architect | \_\[Name\]\_ | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

| CTO | \_\[ChatGPT\]\_ | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

| Technical Programme Manager | \_\[DeepSeek\]\_ | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

| Development Lead | \_\[Aniket\]\_ | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

| Business Owner | \_\[Name\]\_ | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

\#\#\# 8\.4 Cross\-Reference to Repository Documents

| Document | Relationship |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| DOC\-000 | Repository structure referencing this document |

| DOC\-001 | Repository guide referencing this document |

| DOC\-002 | Dependency matrix including this document |

| DOC\-003 | Master index including this document |

| DOC\-004 | Vision & Strategy aligned with this document |

| DOC\-005 | AI Team Handbook referencing ADR\-015 |

| DOC\-006 | Architecture Catalogue including this document |

| DOC\-007 | Delivery Governance referencing this document |

| DOC\-008 | Compliance Matrix referencing this document |

| DOC\-009 | ADR Register containing ADR\-001 to ADR\-018 |

\-\-\-

\#\# End of Document

\*\*Document ID:\*\* DOC\-010  

\*\*Document Name:\*\* \*Enterprise Architecture & ADRs Consolidated\*  

\*\*Version:\*\* 1\.0  

\*\*Status:\*\* Approved / Frozen  

\*\*Owner:\*\* CTO

