# DOC-023 FCPL Rule Engine Translation Guide

\# DOC\-023: FCPL Rule Engine Translation Guide

\*\*Document ID:\*\* DOC\-023  

\*\*Version:\*\* 1\.0  

\*\*Status:\*\* Approved / Frozen  

\*\*Owner:\*\* CTO \(ChatGPT\)  

\*\*Classification:\*\* Rule Engine Translation Guide  

\*\*Purpose:\*\* Document how Excel formulas become configurable RUL\_ rules\. This guide provides the authoritative mapping from FCPL’s spreadsheet\-based business logic to the ODOS Rule Engine tables \(RUL\_CommissionRule, RUL\_GSTRule, RUL\_TDSRule, RUL\_ValidationRule, RUL\_Workflow, etc\.\)\.

\-\-\-

\#\# Table of Contents

1\. Executive Summary

2\. Commission Calculation Rules

3\. GST Calculation Rules

4\. TDS Calculation Rules

5\. Validation Rules

6\. Workflow Rules

7\. Rule Dependencies & Execution Order

8\. Rule Governance & Versioning

9\. Document Status & Approval

\-\-\-

\#\# 1\. Executive Summary

\#\#\# 1\.1 Purpose

This document defines the translation of FCPL’s Excel\-based business logic into configurable rules within the ODOS Rule Engine\. It provides explicit mappings from spreadsheet formulas, conditional logic, and business policies to the corresponding RUL\_ tables as defined in the canonical data model \(DOC\-011\)\.

\#\#\# 1\.2 Rule Engine Philosophy

| Principle | Description |

|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \*\*Metadata\-Driven\*\* | Rules are stored as metadata, not hardcoded |

| \*\*Configuration over Code\*\* | Business logic changes via configuration, not software releases |

| \*\*Auditable\*\* | Every rule execution is logged and traceable |

| \*\*Versioned\*\* | Rules are versioned; historical rules remain for audit |

| \*\*AI\-Ready\*\* | Rules support AI\-assisted execution and learning |

\#\#\# 1\.3 Scope of Coverage

| Rule Category | Source Logic | Target Tables |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Commission | Base %, Connector %, Effective %, slabs | RUL\_CommissionRule, RUL\_CommissionSlab |

| GST | Rate, applicability, reverse charge | RUL\_GSTRule |

| TDS | Rate, section, threshold | RUL\_TDSRule |

| Validation | PAN, amount, dates, profiles | RUL\_ValidationRule |

| Workflow | Case status transitions, approvals | RUL\_Workflow |

\#\#\# 1\.4 Relationship to Other Repository Documents

| Document | Relationship |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| DOC\-010 | Architecture foundation for rule engine |

| DOC\-011 | Canonical data model for rule tables |

| DOC\-014 | Finance & Operations Specifications |

| DOC\-017 | Core Module Specifications for rule execution |

| DOC\-021 | FCPL Industry Configuration for reference data |

| DOC\-022 | FCPL Source\-to\-Canonical Mapping Guide for source formulas |

\-\-\-

\#\# 2\. Commission Calculation Rules

\#\#\# 2\.1 Core Commission Formula

\#\#\#\# 2\.1\.1 Formula Translation

| Excel Formula | Business Logic | RUL\_CommissionRule Field |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \`=Base % × Connector %\` | Effective commission rate | \`EffectiveRate = BaseRate \* ConnectorShare\` |

| \`=Total Disb Amount × Effective Rate\` | Commission amount | \`CommissionAmount = DisbursementAmount \* EffectiveRate\` |

\#\#\#\# 2\.1\.2 Rule Structure

\`\`\`sql

\-\- Example rule for a specific lender and product

INSERT INTO RUL\_CommissionRule \(

    RuleCode,

    RuleName,

    LenderID,

    ProductID,

    ConnectorID,

    BasisType,

    CalculationType,

    BaseRate,

    ConnectorShare,

    EffectiveRate,

    SlabType,

    EffectiveFrom,

    EffectiveTo,

    IsActive

\)

VALUES \(

    'COMM\-FTCPL\-BL\-001',

    'FCPL BL Commission \- Base',

    1, \-\- LenderID for FT Cash

    1, \-\- ProductID for BL

    NULL, \-\- ConnectorID \(global\)

    'DISBURSEMENT',

    'SLAB',

    0\.03, \-\- Base Rate

    0\.70, \-\- Connector Share \(70%\)

    0\.021, \-\- Effective Rate \(3% \* 70%\)

    'LOAN\_AMOUNT',

    '2026\-04\-01',

    NULL,

    TRUE

\);

\`\`\`

\#\#\# 2\.2 Slab\-Based Commission \(RUL\_CommissionSlab\)

\#\#\#\# 2\.2\.1 Bucket Mapping

FCPL’s 10\-tier slab structure translates to multiple rows in \`RUL\_CommissionSlab\`:

| Tier | Min Amount | Max Amount | Slab Rate | RuleCode |

|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|

| 1 | 0 | 50,00,000 | 0\.031 | COMM\-FTCPL\-001 |

| 2 | 50,00,000 | 1,00,00,000 | 0\.031 | COMM\-FTCPL\-001 |

| 3 | 1,00,00,000 | 2,00,00,000 | 0\.0325 | COMM\-FTCPL\-001 |

| 4 | 2,00,00,000 | 3,00,00,000 | 0\.035 | COMM\-FTCPL\-001 |

| 5 | 3,00,00,000 | 5,00,00,000 | 0\.035 | COMM\-FTCPL\-001 |

| 6 | 5,00,00,000 | 10,00,00,000 | 0\.035 | COMM\-FTCPL\-001 |

| 7 | 10,00,00,000 | 25,00,00,000 | 0\.036 | COMM\-FTCPL\-001 |

| 8 | 25,00,00,000 | 50,00,00,000 | 0\.037 | COMM\-FTCPL\-001 |

| 9 | 50,00,00,000 | 100,00,00,000 | 0\.037 | COMM\-FTCPL\-001 |

| 10 | 100,00,00,000 | NULL | 0\.037 | COMM\-FTCPL\-001 |

\#\#\#\# 2\.2\.2 Slab Type Logic

| Slab Type | Logic | Excel Equivalent |

|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \`FLAT\` | Single rate regardless of amount | \`=Base% \* Connector%\` |

| \`LOAN\_AMOUNT\` | Rate varies by disbursement amount | VLOOKUP on amount tier |

| \`ACHIEVEMENT\_VOLUME\` | Rate varies by cumulative achievement | \`=SUMIFS\(\.\.\.\)\` |

\#\#\# 2\.3 Connector\-Specific Commission Rules

\#\#\#\# 2\.3\.1 Rule Resolution Priority

| Priority | Scope | Example |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|

| 1 | Connector \+ Lender \+ Product | Specific connector, specific lender, specific product |

| 2 | Connector \+ Lender | Specific connector, specific lender \(all products\) |

| 3 | Connector \+ Product | Specific connector, all lenders, specific product |

| 4 | Lender \+ Product | All connectors, specific lender, specific product |

| 5 | Global \(NULL\) | All connectors, all lenders, all products |

\#\#\#\# 2\.3\.2 Connector Rate Override

\`\`\`sql

\-\- Connector\-specific rate override

INSERT INTO RUL\_CommissionRule \(

    RuleCode,

    RuleName,

    ConnectorID,

    LenderID,

    ProductID,

    BaseRate,

    ConnectorShare,

    EffectiveRate

\)

VALUES \(

    'COMM\-FTCPL\-CON\-123',

    'Connector 123 \- Special Rate',

    123, \-\- ConnectorID

    1,   \-\- FT Cash

    1,   \-\- BL

    0\.035, \-\- Higher Base Rate

    0\.75,   \-\- Higher Share

    0\.02625 \-\- Effective Rate

\);

\`\`\`

\#\#\# 2\.4 Campaign/Contest Bonus Rules

| Excel Logic | Rule Translation |

|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Contest Target: ₹1\.7 Cr | \`RUL\_Contest\.TargetAmount = 170000000\` |

| Bonus %: 0\.50% | \`RUL\_Contest\.BonusPercent = 0\.005\` |

| Frequency: Monthly | \`RUL\_Contest\.Frequency = 'MONTHLY'\` |

| Period: Apr\-Jun | \`RUL\_Contest\.PeriodStart = '2026\-04\-01', PeriodEnd = '2026\-06\-30'\` |

\#\#\#\# 2\.4\.1 Contest Rule Application

\`\`\`sql

\-\- Contest bonus applied on top of standard commission

\-\- When a case meets the contest criteria, bonus is added

UPDATE RUL\_CommissionRule

SET BonusPercent = 0\.005

WHERE RuleCode = 'COMM\-FTCPL\-CONTEST\-001'

  AND ContestID = 1;

\`\`\`

\-\-\-

\#\# 3\. GST Calculation Rules

\#\#\# 3\.1 GST Rate Rules \(RUL\_GSTRule\)

\#\#\#\# 3\.1\.1 Standard GST \(18%\)

| RuleCode | RuleName | Rate | Applicability | EffectiveFrom |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| GST\-18\-STD | Standard GST 18% | 0\.18 | All commercial rent, commission | 2017\-07\-01 |

\#\#\#\# 3\.1\.2 Exempt/Zero GST

| RuleCode | RuleName | Rate | Applicability |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| GST\-0\-EXEMPT | GST Exempt | 0\.0 | Residential rent, exempt services |

\#\#\#\# 3\.1\.3 Reverse Charge GST

| RuleCode | RuleName | Rate | Applicability |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| GST\-RC\-18 | Reverse Charge 18% | 0\.18 | Services from unregistered dealers |

\#\#\#\# 3\.1\.4 GST Applicability Logic

| Source Logic | Rule Translation |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| If rent is commercial and property is in Maharashtra | Apply 18% GST |

| If rent is residential | Apply 0% GST |

| If landlord is unregistered and service is taxable | Apply Reverse Charge |

\*\*Rule Example:\*\*

\`\`\`sql

INSERT INTO RUL\_GSTRule \(

    RuleCode,

    RuleName,

    Rate,

    ApplicabilityCondition,

    IsReverseCharge,

    EffectiveFrom

\)

VALUES \(

    'GST\-RC\-001',

    'Reverse Charge for Unregistered Landlord',

    0\.18,

    'Landlord\.GSTIN IS NULL AND PropertyType = ''COMMERCIAL''',

    TRUE,

    '2026\-04\-01'

\);

\`\`\`

\#\#\# 3\.2 GST Calculation Logic

| Excel Formula | Business Rule | RUL\_GSTRule Field |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \`=GrossAmount \* 18%\` | GST = Gross × 18% | \`GSTAmount = GrossAmount \* Rate\` |

| \`=IF\(TDSRate>0, GrossAmount\*18%, 0\)\` | GST only if TDS applies | Conditional logic |

\-\-\-

\#\# 4\. TDS Calculation Rules

\#\#\# 4\.1 TDS Rate Rules \(RUL\_TDSRule\)

\#\#\#\# 4\.1\.1 Section 194H – Commission

| Section | Rate | Threshold | Applicability |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| 194H | 5% | ₹15,000 | Commission payments |

| 194H \(individual\) | 5% | ₹15,000 | Individual payees |

\*\*FCPL\-specific:\*\* TDS on connector payouts is 2% \(as per internal policy\) – configurable override\.

\`\`\`sql

INSERT INTO RUL\_TDSRule \(

    RuleCode,

    RuleName,

    SectionCode,

    Rate,

    ThresholdAmount,

    ApplicabilityCondition,

    EffectiveFrom

\)

VALUES \(

    'TDS\-194H\-2PCT',

    'TDS on Connector Payouts \(2%\)',

    '194H',

    0\.02,

    15000,

    'PayeeType = ''CONNECTOR''',

    '2026\-04\-01'

\);

\`\`\`

\#\#\#\# 4\.1\.2 Section 194I – Rent

| RuleCode | Section | Rate | Applicability |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| TDS\-194I\-10PCT | 194I | 10% | Rent payments \(Plant & Machinery\) |

| TDS\-194I\-10PCT\-LAND | 194I | 10% | Rent payments \(Land/Building\) |

\#\#\#\# 4\.1\.3 TDS on Salary – Section 192

| RuleCode | Rate | Applicability |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| TDS\-192\-SALARY | Calculated on slab | Salary payments > ₹2\.5 L |

\#\#\# 4\.2 TDS Variation Logic \(Special Cases\)

| Source Data | Rule Translation |

|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| TDS 0% \(e\.g\., UP New, PUNE NEW\) | \`RUL\_TDSRule\.Rate = 0\` for those entities |

| TDS 10% \(standard\) | \`RUL\_TDSRule\.Rate = 0\.10\` |

| TDS 20% \(rare\) | \`RUL\_TDSRule\.Rate = 0\.20\` |

| TDS 40% \(one\-off\) | \`RUL\_TDSRule\.Rate = 0\.40\` with exception flag |

\*\*Override Logic:\*\*

\`\`\`sql

INSERT INTO RUL\_TDSRule \(

    RuleCode,

    RuleName,

    SectionCode,

    Rate,

    ApplicabilityCondition,

    IsOverride

\)

VALUES \(

    'TDS\-OVERRIDE\-609\-001',

    'TDS Override for Office 609 \(40%\)',

    '194H',

    0\.40,

    'PropertyID = 609',

    TRUE

\);

\`\`\`

\-\-\-

\#\# 5\. Validation Rules

\#\#\# 5\.1 PAN Validation \(RUL\_ValidationRule\)

| RuleCode | RuleName | Validation Logic | Error Message |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| VAL\-PAN\-001 | PAN Format | \`REGEX: ^\[A\-Z\]\{5\}\[0\-9\]\{4\}\[A\-Z\]\{1\}$\` | Invalid PAN format |

\*\*Implementation:\*\*

\`\`\`sql

INSERT INTO RUL\_ValidationRule \(

    RuleCode,

    RuleName,

    ValidationType,

    ValidationExpression,

    ErrorMessage,

    Severity

\)

VALUES \(

    'VAL\-PAN\-001',

    'PAN Format Validation',

    'REGEX',

    '^\[A\-Z\]\{5\}\[0\-9\]\{4\}\[A\-Z\]\{1\}$',

    'PAN must be 10 characters: 5 letters, 4 digits, 1 letter',

    'CRITICAL'

\);

\`\`\`

\#\#\# 5\.2 Amount Validation

| RuleCode | RuleName | Validation Logic | Severity |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|

| VAL\-AMT\-001 | Amount Positive | \`Amount > 0\` | CRITICAL |

| VAL\-AMT\-002 | Max Amount | \`Amount <= 100,00,00,000\` | HIGH |

| VAL\-AMT\-003 | Sanction <= Login | \`SanctionAmount <= LoginAmount\` | HIGH |

| VAL\-AMT\-004 | Disbursement <= Sanction | \`DisbursementAmount <= SanctionAmount\` | CRITICAL |

\#\#\# 5\.3 Date Order Validation

| RuleCode | RuleName | Validation Logic | Severity |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|

| VAL\-DATE\-001 | Login Date <= Sanction Date | \`LoginDate <= SanctionDate\` | CRITICAL |

| VAL\-DATE\-002 | Sanction Date <= Disbursement Date | \`SanctionDate <= DisbursementDate\` | CRITICAL |

| VAL\-DATE\-003 | Invoice Date <= Payment Date | \`InvoiceDate <= PaymentDate\` | HIGH |

\#\#\# 5\.4 Cross\-Field Validation

| RuleCode | RuleName | Validation Logic |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| VAL\-CROSS\-001 | Connector2 only if Connector1 exists | \`Connector2ID IS NULL OR Connector1ID IS NOT NULL\` |

| VAL\-CROSS\-002 | Profile must match product | \`IF Product = 'HL' THEN Profile IN \('SENP','SALARIED'\)\` |

\#\#\# 5\.5 Data Quality Score Rules

| Rule | Weight | Target |

|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|

| Completeness | 15% | ≥95% |

| Accuracy | 15% | ≥98% |

| Validity | 12% | ≥99% |

| Consistency | 10% | ≥95% |

\-\-\-

\#\# 6\. Workflow Rules

\#\#\# 6\.1 Case Workflow \(RUL\_Workflow\)

\#\#\#\# 6\.1\.1 Case Status Transitions

| From State | To State | Transition Condition |

|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| LEAD | APPLICATION | Documents collected |

| APPLICATION | SANCTIONED | Lender approval |

| SANCTIONED | DISBURSED | Disbursement recorded |

| DISBURSED | CLOSED | All payouts made |

| ANY | CANCELLED | User cancels |

| APPLICATION | REJECTED | Lender rejection |

| DISBURSED | PART\_DISBURSED | Partial disbursement |

\*\*Workflow Definition Example:\*\*

\`\`\`sql

INSERT INTO RUL\_Workflow \(

    WorkflowCode,

    WorkflowName,

    EntityType,

    FromState,

    ToState,

    TransitionCondition,

    IsAuto,

    ApprovalRequired

\)

VALUES

\('WF\-CASE\-001', 'Lead to Application', 'CASE', 'LEAD', 'APPLICATION', 'DocumentsComplete = TRUE', TRUE, FALSE\),

\('WF\-CASE\-002', 'Application to Sanctioned', 'CASE', 'APPLICATION', 'SANCTIONED', 'LenderApproval = TRUE', FALSE, TRUE\),

\('WF\-CASE\-003', 'Sanctioned to Disbursed', 'CASE', 'SANCTIONED', 'DISBURSED', 'DisbursementAmount > 0', FALSE, TRUE\);

\`\`\`

\#\#\# 6\.2 Approval Workflow \(Maker\-Checker\)

| Activity | Maker | Checker | Approval Rule |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Commission Approval | Finance Team | Finance Head | \`CommissionAmount > 50000\` |

| Expense Approval | Employee | Manager | \`ExpenseAmount > 10000\` |

| Payment Approval | Finance | CTO | \`PaymentAmount > 1000000\` |

\#\#\# 6\.3 SLA Escalation Workflow

| Condition | Action | Escalation |

|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|

| Payment not reconciled within 48 hours | Flag for review | Operations Lead |

| Case status unchanged for 7 days | Auto\-reminder | Sales Manager |

| Invoice overdue > 15 days | Alert | Collections Team |

\-\-\-

\#\# 7\. Rule Dependencies & Execution Order

\#\#\# 7\.1 Dependency Hierarchy

\`\`\`

┌─────────────────────────────────────────────────────────────────┐

│                    RULE EXECUTION ORDER                         │

├─────────────────────────────────────────────────────────────────┤

│                                                                 │

│  1\. Data Validation Rules \(RUL\_ValidationRule\)                 │

│     \- PAN format, amount ranges, date order                    │

│                                                                 │

│  2\. Master Data Lookup \(MST\_\* tables\)                          │

│                                                                 │

│  3\. Commission Calculation \(RUL\_CommissionRule\)                │

│     \- Base Rate → Connector Share → Effective Rate             │

│     \- Apply slab logic if configured                          │

│                                                                 │

│  4\. GST Calculation \(RUL\_GSTRule\)                              │

│     \- Apply applicable GST rate                                │

│                                                                 │

│  5\. TDS Calculation \(RUL\_TDSRule\)                              │

│     \- Apply TDS rate based on section and thresholds          │

│                                                                 │

│  6\. Net Payable Calculation                                    │

│     \- Amount \- TDS \+ GST                                       │

│                                                                 │

│  7\. Workflow Transition \(RUL\_Workflow\)                         │

│     \- Move to next state if conditions met                    │

│                                                                 │

└─────────────────────────────────────────────────────────────────┘

\`\`\`

\#\#\# 7\.2 Rule Dependencies Table

| Rule Type | Depends On | Used By |

|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|

| Validation | Reference Data | ETL, UI |

| Commission | Lender Agreement | Revenue, Commission |

| GST | Product Type | Revenue, Expense |

| TDS | Payee Type, Amount | Payment |

| Workflow | Case Status | UI, Notifications |

\-\-\-

\#\# 8\. Rule Governance & Versioning

\#\#\# 8\.1 Rule Lifecycle

\`\`\`

Draft → Under Review → Approved → Active → Deprecated → Retired → Archived

\`\`\`

\#\#\# 8\.2 Rule Versioning Strategy

| Version Component | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Major | Breaking changes \(e\.g\., new commission structure\) |

| Minor | Non\-breaking changes \(e\.g\., rate adjustments\) |

| Patch | Bug fixes |

\*\*Format:\*\* \`v<major>\.<minor>\.<patch>\` \(e\.g\., \`v1\.0\.0\`\)

\#\#\# 8\.3 Rule Audit Requirements

| Audit Field | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| CreatedBy | User/System who created the rule |

| CreatedDateTime | Timestamp of creation |

| LastModifiedBy | User/System who last modified |

| LastModifiedDateTime | Timestamp of last modification |

| ApprovedBy | Approver of the rule |

| ApprovedDateTime | Approval timestamp |

| EffectiveFrom | Date when rule becomes active |

| EffectiveTo | Date when rule expires |

\#\#\# 8\.4 AI\-Ready Rule Classification

| Classification | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Static | Cannot be learned \(e\.g\., regulatory rates\) |

| Configurable | Can be configured by business \(e\.g\., commission rates\) |

| Learnable | AI can learn patterns \(e\.g\., anomaly detection\) |

| AI Assisted | AI assists in decision\-making \(e\.g\., recommendation\) |

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

\*\*This document is designated as a Rule Engine Baseline Artefact\.\*\*

\*\*Following approval:\*\*

\- Structural changes to rule definitions require a new Architecture Decision Record \(ADR\)\.

\- Changes to rule logic require Architecture Review Board \(ARB\) approval\.

\- All rule engine implementation shall use this document as the governing baseline\.

\*\*Freeze Status:\*\* ✅ \*\*FROZEN\*\*

\#\#\# 9\.3 Approval Sign\-Off

| Role | Name | Signature | Date |

|\-\-\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-|

| Enterprise Architect | Architecture Review Board | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

| Rule Engine Lead | \[Name\] | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

| Finance Lead | \[Name\] | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

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

| DOC\-010 | Architecture & ADRs referencing rule engine |

| DOC\-011 | Data Model referencing RUL\_ tables |

| DOC\-014 | Finance & Operations referencing rule logic |

| DOC\-017 | Core Modules referencing rule execution |

| DOC\-021 | FCPL Industry Configuration for rule context |

| DOC\-022 | Source\-to\-Canonical Mapping for formula mapping |

\-\-\-

\#\# End of Document

\*\*Document ID:\*\* DOC\-023  

\*\*Document Name:\*\* \*FCPL Rule Engine Translation Guide\*  

\*\*Version:\*\* 1\.0  

\*\*Status:\*\* Approved / Frozen  

\*\*Owner:\*\* CTO

