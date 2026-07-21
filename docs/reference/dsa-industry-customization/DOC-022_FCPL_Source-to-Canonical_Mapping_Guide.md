# DOC-022 FCPL Source-to-Canonical Mapping Guide

\# DOC\-022: FCPL Source\-to\-Canonical Mapping Guide

\*\*Document ID:\*\* DOC\-022  

\*\*Version:\*\* 1\.0  

\*\*Status:\*\* Approved / Frozen  

\*\*Owner:\*\* CTO \(ChatGPT\)  

\*\*Classification:\*\* Source\-to\-Canonical Mapping Guide  

\*\*Purpose:\*\* Define the explicit mapping from FCPL Excel sources to ODOS canonical tables \(DOC\-011\)\. This document serves as the authoritative reference for ETL development and data migration\.

\-\-\-

\#\# Table of Contents

1\. Executive Summary

2\. Secured Tracker Mapping

3\. Connector Master Mapping

4\. Lender Payout Data Mapping

5\. Salary Data Mapping

6\. Rent & Property Data Mapping

7\. Loan Application \(DSR\) Mapping

8\. Mapping Cross\-Reference

9\. Document Status & Approval

\-\-\-

\#\# 1\. Executive Summary

\#\#\# 1\.1 Purpose

This document defines the explicit mapping from FCPL Excel sources to the ODOS canonical enterprise data model\. It provides column\-level mappings, data type transformations, and business logic translations for all source files identified in the FCPL data assessment\.

\#\#\# 1\.2 Source Files Covered

| File | Sheets | Purpose |

|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|

| Secured Tracker FY 26\-27\.xlsx | Tracker, Mastersheet, Bank Account Master | Loan case tracking, payouts, commissions |

| Connector Master\.xlsx | Overview, Column Dictionary, Master, Connector Directory, Reconciliation Summary, Connector Advances | Connector rates, bank details, reconciliation |

| Lender Payout Data\.xlsx | Single sheet \(39 columns\) | Lender commission rates, product classification |

| Salary Sheet Apr/May 2026\.xlsx | Payroll Sheet, Pivot | Employee salary, deductions, net pay |

| Rent Files \(Fineoteric\) | 20\+ sheets | Rent agreements, payments, TDS/GST |

| DSR \- BL and PL MIS\.xlsx | BL, PL | Loan application login, sanction, disbursement |

| Gold Crest Rent\.xlsx | 21 sheets | Office unit rent agreements |

\#\#\# 1\.3 Mapping Philosophy

| Principle | Description |

|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \*\*Canonical First\*\* | All mappings target the Canonical Enterprise Data Model |

| \*\*Business Semantics First\*\* | Business meaning drives mapping decisions |

| \*\*Metadata Driven\*\* | Mappings are metadata\-driven where possible |

| \*\*Traceable\*\* | Every canonical value traces to its source |

| \*\*Idempotent\*\* | Mappings produce the same result when re\-run |

\#\#\# 1\.4 Relationship to Other Repository Documents

| Document | Relationship |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| DOC\-010 | Architecture foundation for mapping decisions |

| DOC\-011 | Canonical data model referenced for all target tables |

| DOC\-014 | Finance & Operations Specifications for business logic |

| DOC\-017 | Core Module Specifications for implementation |

| DOC\-021 | FCPL Industry Configuration for reference data |

| DOC\-023 | Rule Engine Translation Guide for formula logic |

\-\-\-

\#\# 2\. Secured Tracker Mapping

\#\#\# 2\.1 Source File Overview

| Attribute | Details |

|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|

| \*\*File Name\*\* | Secured Tracker FY 26\-27 \(2\)\.xlsx |

| \*\*Primary Sheet\*\* | "Tracker" |

| \*\*Row Count\*\* | ~384 active rows |

| \*\*Column Count\*\* | 79 columns \(A to CA\) |

| \*\*Purpose\*\* | Loan case tracking, payout management, reconciliation |

\#\#\# 2\.2 Case\-Level Mapping \(TRN\_Case\)

\#\#\#\# 2\.2\.1 Column Mapping

| Source Column | Source Field | Target Table | Target Field | Transformation |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| D | CASE NO | TRN\_Case | CaseNumber | Direct mapping; primary key |

| E | ENQUIRY NO | TRN\_Case | EnquiryNumber | Direct mapping |

| F | APPLICATION NUMBER | TRN\_Case | ApplicationNumber | Direct mapping |

| B | ENTRY DATE | TRN\_Case | EntryDate | Date parse: DD\-MM\-YYYY → YYYY\-MM\-DD |

| C | ENTRY DONE BY | TRN\_Case | EntryBy | Direct mapping |

| G | COMPANY NAME | TRN\_Case | CompanyName | Direct mapping; allow NULL |

| H | CUSTOMER NAME | TRN\_Case | CustomerName | Direct mapping; allow NULL |

| I | BANK NAME | TRN\_Case | LenderID | Lookup: Match to MST\_Lender |

| J | CODE | TRN\_Case | BranchCode | Direct mapping |

| K | BRANCH | TRN\_Case | BranchName | Direct mapping |

| L | RM NAME | TRN\_Case | RMName | Direct mapping |

| M | PRODUCT | TRN\_Case | ProductID | Lookup: Match to MST\_Product |

| N | CONNECTOR | TRN\_Case | Connector1ID | Lookup: Match to MST\_Connector |

| O | CONNECTOR 2 | TRN\_Case | Connector2ID | Lookup: Match to MST\_Connector |

| P | Referred by | TRN\_Case | ReferredBy | Direct mapping |

| Q | UNIT HEAD | TRN\_Case | UnitHeadID | Lookup: Match to MST\_Employee |

| R | SM NAME | TRN\_Case | SalesManagerID | Lookup: Match to MST\_Employee |

| S | REGION | TRN\_Case | Region | Direct mapping |

| T | STATUS | TRN\_Case | Status | Lookup: Match to REF\_Status |

| U | TOTAL DISB AMOUNT | TRN\_Case | TotalDisbursementAmount | Parse numeric; DECIMAL\(18,2\) |

| V | DISB DATE | TRN\_Case | DisbursementDate | Date parse: DD\-MM\-YYYY → YYYY\-MM\-DD |

| W | PROFILE | TRN\_Case | Profile | Direct mapping \(SENP, SALARIED, N/A\) |

| AI | Taxable Amount | TRN\_Case | TaxableAmount | Parse numeric; DECIMAL\(18,2\) |

| AJ | INVOICE DATE | TRN\_Case | InvoiceDate | Date parse: DD\-MM\-YYYY → YYYY\-MM\-DD |

| AK | INVOICE NO | TRN\_Case | InvoiceNumber | Direct mapping |

| AL | Bill Status | TRN\_Case | BillStatus | Lookup: Match to REF\_Status |

| AM | Receive date | TRN\_Case | ReceiveDate | Date parse: DD\-MM\-YYYY → YYYY\-MM\-DD |

| AN | Case wise P&L | TRN\_Case | ProfitLoss | Parse numeric; DECIMAL\(18,2\) |

| AO | Payout % | TRN\_Case | PayoutPercentage | Parse numeric; DECIMAL\(10,4\) |

| AP | Remarks | TRN\_Case | Remarks | Direct mapping |

| AQ | Payment Approval | TRN\_Case | PaymentApproval | YES → TRUE, NO → FALSE |

\#\#\#\# 2\.2\.2 Date Parsing Rules

| Source Format | Parse Rule | Target Format |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \`2026\-04\-01 00:00:00\` | Extract date component | \`2026\-04\-01\` |

| \`2026\-04\-01\` | Direct parse | \`2026\-04\-01\` |

| \`29\-2\-25\` | Parse with year conversion | \`2025\-02\-29\` |

| \`31/05/2026\` | Parse with DD/MM/YYYY | \`2026\-05\-31\` |

| \`2023\-03\-01 00:00:00\` | Extract date component | \`2023\-03\-01\` |

\#\#\# 2\.3 Payout\-Level Mapping \(TRN\_Commission\)

\#\#\#\# 2\.3\.1 Column Mapping

| Source Column | Source Field | Target Table | Target Field | Transformation |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| D | CASE NO | TRN\_Commission | CaseID | Lookup to TRN\_Case\.CaseID |

| Y | BANK PAYOUTAMT | TRN\_Commission | BankPayoutAmount | Parse numeric; DECIMAL\(18,2\) |

| AA | CONNECTOR PAYOUT AMT | TRN\_Commission | ConnectorPayoutAmount | Parse numeric; DECIMAL\(18,2\) |

| AC | CONNECTOR 2 PAYOUT AMT | TRN\_Commission | Connector2PayoutAmount | Parse numeric; DECIMAL\(18,2\) |

| AE | UNIT HEAD AMT | TRN\_Commission | UnitHeadPayoutAmount | Parse numeric; DECIMAL\(18,2\) |

| AG | SM PAYOUT AMT | TRN\_Commission | SalesManagerPayoutAmount | Parse numeric; DECIMAL\(18,2\) |

| AW | PAYMENT AMT | TRN\_Commission | PaymentAmount | Parse numeric; DECIMAL\(18,2\) |

| AX | TDS@2% | TRN\_Commission | TDSAmount | Parse numeric; DECIMAL\(18,2\) |

| AY | FINAL PAYABLE AMT | TRN\_Commission | FinalPayableAmount | Parse numeric; DECIMAL\(18,2\) |

| BA | C\-1 UTR | TRN\_Commission | UTRNumber | Direct mapping |

| AT | Payment Request Date C\-1 | TRN\_Commission | PaymentRequestDate | Date parse → YYYY\-MM\-DD |

\#\#\#\# 2\.3\.2 Payee Type Mapping

| Payee | PayeeType | Target Column |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Bank | BANK | TRN\_Commission\.PayeeType = 'BANK' |

| Connector 1 | CONNECTOR\_1 | TRN\_Commission\.PayeeType = 'CONNECTOR' |

| Connector 2 | CONNECTOR\_2 | TRN\_Commission\.PayeeType = 'CONNECTOR' |

| Unit Head | UNIT\_HEAD | TRN\_Commission\.PayeeType = 'UNIT\_HEAD' |

| Sales Manager | SALES\_MANAGER | TRN\_Commission\.PayeeType = 'SM' |

\#\#\# 2\.4 Formula\-to\-Rule Translation

| Excel Formula | Business Logic | Target Rule |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \`=Y4/U4\` | Bank Payout % = Bank Payout Amt / Total Disb Amount | RUL\_CommissionRule\.BankPayoutPercent |

| \`=round\(AW4\*2%,\)\` | TDS = Payment Amount × 2% | RUL\_TDSRule\.TDSRate = 2% |

| \`=AW4\-AX4\` | Final Payable = Payment Amount \- TDS | RUL\_CommissionRule\.NetAmount |

| \`=SUBTOTAL\(9,U4:U5522\)\` | Sum of filtered values | BI\_DailySnapshot\.TotalDisbursement |

| \`=VLOOKUP\(AZ4,'Bank Account Master'\!B:F,3,0\)\` | Fetch bank details | MST\_PartyBankAccount lookup |

\#\#\# 2\.5 Master Data Lookup Mapping

\#\#\#\# 2\.5\.1 Bank Master Lookup \(MST\_Lender\)

| Source Value | Target LenderID | LenderName |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|

| Any bank name | System\-generated | Matched via fuzzy matching |

| Bank name variations | Normalized | Standardized name |

\#\#\#\# 2\.5\.2 Connector Lookup \(MST\_Connector\)

| Source Value | Target ConnectorID | ConnectorName |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Connector name | System\-generated | Matched via fuzzy matching |

| Connector code | System\-generated | Matched via exact code |

\#\#\#\# 2\.5\.3 Product Lookup \(MST\_Product\)

| Source Value | Target ProductID | ProductName |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| LAP | System\-generated | Loan Against Property |

| HL | System\-generated | Home Loan |

| BL | System\-generated | Business Loan |

| WC/OD | System\-generated | Working Capital/Overdraft |

\#\#\# 2\.6 Data Quality Rules

| Rule ID | Rule Description | Validation |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|

| DQ\-001 | Case ID format | \`~/^FY\\d\{2\}\-\\d\{2\}/SC/\\d\{4\}$/\` |

| DQ\-002 | Disbursement amount positive | \`total\_disb\_amount >= 0\` |

| DQ\-003 | Date order | \`disb\_date <= invoice\_date <= receive\_date\` |

| DQ\-004 | Payout sum | \`SUM\(payouts\) <= total\_disb\_amount \* 0\.10\` |

| DQ\-005 | Status valid | \`IN \('DISBURSED', 'PART DISBURSED', 'CANCELLED', 'DUPLICATE', 'PENDING'\)\` |

\-\-\-

\#\# 3\. Connector Master Mapping

\#\#\# 3\.1 Source File Overview

| Attribute | Details |

|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|

| \*\*File Name\*\* | Connector Master\.xlsx |

| \*\*Primary Sheet\*\* | "Master" |

| \*\*Row Count\*\* | 2,966 rows |

| \*\*Column Count\*\* | 62 columns |

| \*\*Purpose\*\* | Connector rate cards, commission structures, bank details |

\#\#\# 3\.2 Connector Master Mapping \(MST\_Connector\)

\#\#\#\# 3\.2\.1 Column Mapping

| Source Column | Source Field | Target Table | Target Field | Transformation |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| B | Connector Code | MST\_Connector | ConnectorCode | Clean: remove quotes, trim spaces |

| C | Connector Name | MST\_Connector | ConnectorName | Direct mapping; fuzzy matching for duplicates |

| A | Sr No | MST\_Connector | ExternalID | Direct mapping |

| D | DSA | MST\_Connector | DSA | FCPL/BW |

| AZ\-BD | Qualifying Notes | MST\_Connector | QualifyingNotes | Direct mapping; parse structured data |

\#\#\#\# 3\.2\.2 Bank Account Details \(MST\_PartyBankAccount\)

| Source Column | Source Field | Target Table | Target Field | Transformation |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Connector Name | Bank Account Master | MST\_PartyBankAccount | PartyID | Lookup to MST\_Connector |

| Bank Account Master | Bank Name | MST\_PartyBankAccount | BankName | Direct mapping |

| Bank Account Master | Account No | MST\_PartyBankAccount | AccountNumber | Direct mapping |

| Bank Account Master | IFSC | MST\_PartyBankAccount | IFSC | Direct mapping |

| Bank Account Master | PAN | MST\_PartyBankAccount | PAN | Direct mapping |

| Bank Account Master | GST | MST\_PartyBankAccount | GSTIN | Direct mapping |

\#\#\# 3\.3 Commission Rate Mapping \(RUL\_CommissionRule\)

\#\#\#\# 3\.3\.1 Bucket Unpivoting

The 10 bucket columns \(U\-AD, AE\-AN, AO\-AX\) shall be unpivoted into 10 rows per connector\-lender\-subproduct\.

| Source Column Range | Description | Target Field |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| U\-AD | Base % \(10 columns\) | RUL\_CommissionRule\.BaseRate |

| AE\-AN | Connector % \(10 columns\) | RUL\_CommissionRule\.ConnectorShare |

| AO\-AX | Effective % \(10 columns\) | RUL\_CommissionRule\.EffectiveRate |

\#\#\#\# 3\.3\.2 Bucket Tier Mapping

| Column | Tier Name | Min Amount | Max Amount |

|\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|

| U | \`< ₹50 L\` | 0 | 50,00,000 |

| V | \`₹50 L – < ₹1 Cr\` | 50,00,000 | 1,00,00,000 |

| W | \`₹1 Cr – < ₹2 Cr\` | 1,00,00,000 | 2,00,00,000 |

| X | \`₹2 Cr – < ₹3 Cr\` | 2,00,00,000 | 3,00,00,000 |

| Y | \`₹3 Cr – < ₹5 Cr\` | 3,00,00,000 | 5,00,00,000 |

| Z | \`₹5 Cr – < ₹10 Cr\` | 5,00,00,000 | 10,00,00,000 |

| AA | \`₹10 Cr – < ₹25 Cr\` | 10,00,00,000 | 25,00,00,000 |

| AB | \`₹25 Cr – < ₹50 Cr\` | 25,00,00,000 | 50,00,00,000 |

| AC | \`₹50 Cr – < ₹100 Cr\` | 50,00,00,000 | 100,00,00,000 |

| AD | \`≥ ₹100 Cr\` | 100,00,00,000 | NULL |

\#\#\#\# 3\.3\.3 Commission Rule Mapping

| Source Field | Target Field | Description |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Base % \(U\-AD\) | RUL\_CommissionRule\.BaseRate | Lender\-side commission rate |

| Connector % \(AE\-AN\) | RUL\_CommissionRule\.ConnectorShare | Connector share percentage |

| Effective % \(AO\-AX\) | RUL\_CommissionRule\.EffectiveRate | Calculated: Base × Connector |

| Slab Type | RUL\_CommissionRule\.SlabType | Flat / Loan\-Amount / Achievement\-Volume |

| Observed Cases \(AY\) | RUL\_CommissionRule\.ObservedCases | Historical case count |

\#\#\# 3\.4 Qualifying Conditions Mapping

\#\#\#\# 3\.4\.1 Qualifying Flags

| Source Column | Source Value | Target Field | Target Value |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| AC \(Qualifying\) | I\+PF | RUL\_ValidationRule | Insurance AND PF Applicable |

| AC \(Qualifying\) | I | RUL\_ValidationRule | Insurance Applicable |

| AC \(Qualifying\) | PF | RUL\_ValidationRule | PF Applicable |

| AC \(Qualifying\) | ROI | RUL\_ValidationRule | ROI Based |

\#\#\#\# 3\.4\.2 Rate Extraction

| Source Column | Source Value | Extraction Rule | Target Field |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| AD \(PF %\) | \`0\.02\` | Direct parse | RUL\_ValidationRule\.PF\_Rate |

| AE \(I %\) | \`0\.01\` | Direct parse | RUL\_ValidationRule\.Insurance\_Rate |

| AC \(Qualifying Notes\) | \`\(1\.25% pf \+ Insurance Mandatory\)\` | Regex extraction | RUL\_ValidationRule\.QualifyingNotes |

\#\#\# 3\.5 Contest Data Mapping

| Source Column | Source Field | Target Table | Target Field |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| BF | Contest Frequency | RUL\_Contest | Frequency |

| BG | Contest Target | RUL\_Contest | TargetAmount |

| BH | Contest Bonus % | RUL\_Contest | BonusPercent |

| BI | Contest Period | RUL\_Contest | Period |

| BJ | Contest Notes | RUL\_Contest | Notes |

\#\#\# 3\.6 Connector Hierarchy Mapping \(MST\_ConnectorHierarchy\)

| Source Field | Source Value | Target Field | Target Value |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Connector Type | Level 1 | HierarchyLevel | 1 \(Master DSA\) |

| Connector Type | Level 2 | HierarchyLevel | 2 \(Regional Connector\) |

| Connector Type | Level 3 | HierarchyLevel | 3 \(Field Connector\) |

\-\-\-

\#\# 4\. Lender Payout Data Mapping

\#\#\# 4\.1 Source File Overview

| Attribute | Details |

|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|

| \*\*File Name\*\* | FCPL Lender Payout Data\.xlsx |

| \*\*Primary Sheet\*\* | Single sheet \(unnamed\) |

| \*\*Row Count\*\* | 230 rows |

| \*\*Column Count\*\* | 39 columns |

| \*\*Purpose\*\* | Lender commission rates, product classification, qualifying conditions |

\#\#\# 4\.2 Core Payout Mapping \(RUL\_CommissionRule\)

\#\#\#\# 4\.2\.1 Column Mapping

| Source Column | Source Field | Target Table | Target Field | Transformation |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Sr\. No\. | Serial Number | RUL\_CommissionRule | ExternalID | Direct mapping |

| DSA | DSA | RUL\_CommissionRule | DSA | FCPL/BW |

| Lender/NBFC | Lender Name | MST\_Lender | LenderName | Lookup/match |

| NBFC? | NBFC Flag | MST\_Lender | IsNBFC | TRUE/FALSE |

| Type | Loan Type | RUL\_CommissionRule | LoanType | Secured/Unsecured |

| Category | Product Category | MST\_Product | Category | BL/HL/LAP/PL |

| Sub\-product | Sub\-product | MST\_Product | SubProduct | Direct mapping |

| Base % | Base Percentage | RUL\_CommissionRule | BaseRate | Parse decimal |

| Headline % | Headline Percentage | RUL\_CommissionRule | HeadlineRate | Parse decimal |

| Slab Type | Slab Type | RUL\_CommissionRule | SlabType | Flat/Loan\-Amount/Achievement\-Volume |

\#\#\#\# 4\.2\.2 Commission Slab Mapping

| Source Column | Tier Name | Target Field |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| S | \`< ₹50 L\` | RUL\_CommissionSlab\.Slab1 |

| T | \`₹50 L – < ₹1 Cr\` | RUL\_CommissionSlab\.Slab2 |

| U | \`₹1 Cr – < ₹2 Cr\` | RUL\_CommissionSlab\.Slab3 |

| V | \`₹2 Cr – < ₹3 Cr\` | RUL\_CommissionSlab\.Slab4 |

| W | \`₹3 Cr – < ₹5 Cr\` | RUL\_CommissionSlab\.Slab5 |

| X | \`₹5 Cr – < ₹10 Cr\` | RUL\_CommissionSlab\.Slab6 |

| Y | \`₹10 Cr – < ₹25 Cr\` | RUL\_CommissionSlab\.Slab7 |

| Z | \`₹25 Cr – < ₹50 Cr\` | RUL\_CommissionSlab\.Slab8 |

| AA | \`₹50 Cr – < ₹100 Cr\` | RUL\_CommissionSlab\.Slab9 |

| AB | \`≥ ₹100 Cr\` | RUL\_CommissionSlab\.Slab10 |

\#\#\# 4\.3 Qualifying Conditions Mapping \(RUL\_ValidationRule\)

| Source Column | Source Field | Target Field | Transformation |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| AC | Qualifying | RUL\_ValidationRule\.QualifyingType | I\+PF / I / PF / ROI / NA |

| AD | PF % | RUL\_ValidationRule\.PF\_Rate | Parse decimal; DECIMAL\(10,4\) |

| AE | I % | RUL\_ValidationRule\.Insurance\_Rate | Parse decimal; DECIMAL\(10,4\) |

| AF | Qualifying Notes | RUL\_ValidationRule\.QualifyingNotes | Direct mapping; parse embedded data |

| AG | Commercial | RUL\_ValidationRule\.CommercialNotes | Direct mapping; parse for ROI |

\#\#\# 4\.4 ROI Extraction from Commercial Text

| Pattern | Extraction Rule | Example |

|\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|

| \`ROI X%\` | Extract X | \`ROI 16\.5%\` → 0\.165 |

| \`IRR X%\` | Extract X | \`IRR 15\.2%\` → 0\.152 |

| \`X% \- Y%\` | Extract range | \`12\.0% \- 18\.0%\` → Min=0\.12, Max=0\.18 |

| \`Rate X%\` | Extract X | \`Rate 15\.50%\` → 0\.155 |

\#\#\# 4\.5 Contest Data Mapping

| Source Column | Source Field | Target Table | Target Field |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| AH | Contest Frequency | RUL\_Contest | Frequency |

| AI | Contest Target | RUL\_Contest | TargetAmount |

| AJ | Contest Bonus % | RUL\_Contest | BonusPercent |

| AK | Contest Period | RUL\_Contest | Period |

| AL | Contest Notes | RUL\_Contest | Notes |

\-\-\-

\#\# 5\. Salary Data Mapping

\#\#\# 5\.1 Source File Overview

| Attribute | Details |

|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|

| \*\*File Name\*\* | Combine Salary Sheet APR\-2026\.xlsx |

| \*\*Primary Sheet\*\* | "Payroll Sheet" |

| \*\*Row Count\*\* | ~63 employees |

| \*\*Column Count\*\* | 67 columns |

| \*\*Purpose\*\* | Employee salary calculation, deductions, net pay |

\#\#\# 5\.2 Employee Master Mapping \(MST\_Employee\)

\#\#\#\# 5\.2\.1 Column Mapping

| Source Column | Source Field | Target Table | Target Field | Transformation |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Employee Code | Code | MST\_Employee | EmployeeCode | Direct mapping |

| Employee Name | Name | MST\_Employee | FullName | Direct mapping |

| Gender | Gender | MST\_Employee | Gender | M/F → Male/Female |

| Date of Birth | DOB | MST\_Employee | DateOfBirth | Date parse: DD\-MM\-YYYY → YYYY\-MM\-DD |

| Father Name | Father Name | MST\_Employee | FatherName | Direct mapping |

| Marital Status | Marital Status | MST\_Employee | MaritalStatus | Standardize: MARRIED, UNMARRIED, SINGLE |

| PAN | PAN | MST\_Employee | PAN | Direct mapping |

| Aadhar Number | Aadhar | MST\_Employee | AadharNumber | Direct mapping |

| Email | Email | MST\_Employee | Email | Direct mapping |

| Mobile Number | Mobile | MST\_Employee | MobileNumber | Direct mapping |

| Address | Address | MST\_Employee | Address | Direct mapping |

| Date of Joining | DOJ | MST\_Employee | DateOfJoining | Date parse: DD\-MM\-YYYY → YYYY\-MM\-DD |

| Designation | Designation | MST\_Employee | Designation | Direct mapping |

| Department | Department | MST\_Employee | Department | Direct mapping |

| Team | Team | MST\_Employee | TeamName | Direct mapping |

| Branch | Branch | MST\_Employee | BranchName | Direct mapping |

\#\#\#\# 5\.2\.2 Bank Account Mapping \(MST\_PartyBankAccount\)

| Source Column | Source Field | Target Table | Target Field |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Bank Name | Bank | MST\_PartyBankAccount | BankName |

| Bank Account Number | Account No | MST\_PartyBankAccount | AccountNumber |

| IFSC | IFSC | MST\_PartyBankAccount | IFSC |

| UAN | UAN | MST\_PartyBankAccount | UAN |

| PF Applicable | PF | MST\_PartyBankAccount | PF\_Applicable |

| ESIC Applicable | ESIC | MST\_PartyBankAccount | ESIC\_Applicable |

\#\#\# 5\.3 Salary Payment Mapping \(TRN\_Salary\)

\#\#\#\# 5\.3\.1 Column Mapping

| Source Column | Source Field | Target Table | Target Field | Transformation |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Pay Month | Month | TRN\_Salary | PayMonth | Date parse → YYYY\-MM |

| Employee Code | Code | TRN\_Salary | EmployeeID | Lookup to MST\_Employee |

| Payable Days | Days | TRN\_Salary | PayableDays | Parse integer |

| One Day Salary | One Day | TRN\_Salary | OneDaySalary | Parse numeric; DECIMAL\(18,2\) |

| Gross Earnings | Gross | TRN\_Salary | GrossEarnings | Parse numeric; DECIMAL\(18,2\) |

| PF \- Employee | PF | TRN\_Salary | PF\_EmployeeShare | Parse numeric; DECIMAL\(18,2\) |

| ESIC \- Employee | ESIC | TRN\_Salary | ESIC\_EmployeeShare | Parse numeric; DECIMAL\(18,2\) |

| Professional Tax | PT | TRN\_Salary | ProfessionalTax | Parse numeric; DECIMAL\(18,2\) |

| MLWF | MLWF | TRN\_Salary | MLWF | Parse numeric; DECIMAL\(18,2\) |

| TDS | TDS | TRN\_Salary | TDS\_Amount | Parse numeric; DECIMAL\(18,2\) |

| Advance Salary | Advance | TRN\_Salary | AdvanceSalary | Parse numeric; DECIMAL\(18,2\) |

| Net Payable | Net Payable | TRN\_Salary | NetPayable | Parse numeric; DECIMAL\(18,2\) |

| Payment Date | Payment Date | TRN\_Salary | PaymentDate | Date parse → YYYY\-MM\-DD |

| UTR Number | UTR | TRN\_Salary | UTRNumber | Direct mapping |

\#\#\# 5\.4 Statutory Payment Mapping \(TRN\_StatutoryPayment\)

| Source Field | Target Table | Target Field | Transformation |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| PF \- Employee | TRN\_StatutoryPayment | PF\_EmployeeShare | Parse numeric |

| PF \- Employer | TRN\_StatutoryPayment | PF\_EmployerShare | Parse numeric |

| ESIC \- Employee | TRN\_StatutoryPayment | ESIC\_EmployeeShare | Parse numeric |

| ESIC \- Employer | TRN\_StatutoryPayment | ESIC\_EmployerShare | Parse numeric |

| Professional Tax | TRN\_StatutoryPayment | ProfessionalTax | Parse numeric |

| TDS | TRN\_StatutoryPayment | TDS\_Amount | Parse numeric |

\#\#\# 5\.5 Formula\-to\-Rule Translation

| Excel Formula | Business Logic | Target Rule |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \`=40000\-1800\` | Basic Salary | MST\_Employee\.BasicSalary |

| \`=AI50\*2%\` | TDS Calculation | RUL\_TDSRule\.TDSRate = 2% |

| \`=Gross \- PF \- ESIC \- PT \- TDS\` | Net Payable | TRN\_Salary\.NetPayable |

\-\-\-

\#\# 6\. Rent & Property Data Mapping

\#\#\# 6\.1 Source File Overview

| Attribute | Details |

|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|

| \*\*File Name\*\* | Rent for Fineoteric FY 2026\-27\.xlsx |

| \*\*Sheets\*\* | 20\+ rent agreements |

| \*\*Purpose\*\* | Rent agreements, payments, TDS/GST calculations |

\#\#\# 6\.2 Tenant/Landlord Mapping \(MST\_Party\)

| Source Field | Target Table | Target Field | Transformation |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Tenant Name | MST\_Party | PartyName | Direct mapping |

| Tenant PAN | MST\_Party | PAN | Direct mapping |

| Tenant GSTIN | MST\_Party | GSTIN | Direct mapping |

| Address | MST\_PartyAddress | Address | Split into structured fields |

\#\#\# 6\.3 Property Mapping \(MST\_Property\)

| Source Field | Target Table | Target Field | Transformation |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Property Name | MST\_Property | PropertyName | Direct mapping |

| Address | MST\_Property | Address | Split into structured fields |

| City | MST\_Property | City | Direct mapping |

| State | MST\_Property | State | Lookup to REF\_State |

\#\#\# 6\.4 Rent Agreement Mapping \(TRN\_RentAgreement\)

| Source Field | Target Table | Target Field | Transformation |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Sheet Name | TRN\_RentAgreement | PropertyCode | Extract from sheet name |

| Agreement Start | TRN\_RentAgreement | StartDate | Date parse |

| Agreement End | TRN\_RentAgreement | EndDate | Date parse |

| Monthly Rent | TRN\_RentAgreement | MonthlyRent | Parse numeric |

| Security Deposit | TRN\_RentAgreement | SecurityDeposit | Parse numeric |

| TDS Rate | TRN\_RentAgreement | TDS\_Rate | Parse numeric |

| GST Rate | TRN\_RentAgreement | GST\_Rate | Parse numeric |

| Escalation % | TRN\_RentAgreement | EscalationPercent | Parse numeric |

\#\#\# 6\.5 Rent Payment Mapping \(TRN\_RentPayment\)

| Source Field | Target Table | Target Field | Transformation |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| Period Start | TRN\_RentPayment | PeriodStart | Date parse |

| Period End | TRN\_RentPayment | PeriodEnd | Date parse |

| Gross Amount | TRN\_RentPayment | GrossAmount | Parse numeric |

| TDS Amount | TRN\_RentPayment | TDSAmount | Parse numeric |

| GST Amount | TRN\_RentPayment | GSTAmount | Parse numeric |

| Net Amount | TRN\_RentPayment | NetAmount | Parse numeric |

| Payment Date | TRN\_RentPayment | PaymentDate | Date parse |

| Payment Mode | TRN\_RentPayment | PaymentMode | Standardize |

\#\#\# 6\.6 Formula\-to\-Rule Translation

| Excel Formula | Business Logic | Target Rule |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-|

| \`=F13\*10%\` | TDS = Gross × 10% | RUL\_TDSRule\.TDSRate = 10% |

| \`=F13\*18%\` | GST = Gross × 18% | RUL\_GSTRule\.GSTRate = 18% |

| \`=F13\-G13\+H13\` | Net = Gross \- TDS \+ GST | TRN\_RentPayment\.NetAmount |

\-\-\-

\#\# 7\. Loan Application \(DSR\) Mapping

\#\#\# 7\.1 Source File Overview

| Attribute | Details |

|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-|

| \*\*File Name\*\* | DSR – BL and PL MIS – APRIL\_2026\.xlsx |

| \*\*Sheets\*\* | BL, PL |

| \*\*Row Count\*\* | ~250 rows \(BL\), ~167 rows \(PL\) |

| \*\*Purpose\*\* | Loan application login, sanction, disbursement tracking |

\#\#\# 7\.2 Loan Application Mapping \(TRN\_Case\)

| Source Column | Source Field | Target Table | Target Field | Transformation |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| APP NO | Application Number | TRN\_Case | ApplicationNumber | Direct mapping |

| MONTH | Month | TRN\_Case | ReportMonth | Date parse → YYYY\-MM |

| COMPANY NAME | Company Name | TRN\_Case | CompanyName | Direct mapping |

| CUSTOMER NAME | Customer Name | TRN\_Case | CustomerName | Direct mapping |

| PROFILE | Profile | TRN\_Case | Profile | Direct mapping |

| PRODUCT | Product | TRN\_Case | ProductID | Lookup to MST\_Product |

| CONNECTOR NAME | Connector | TRN\_Case | ConnectorID | Lookup to MST\_Connector |

| UNIT HEAD | Unit Head | TRN\_Case | UnitHeadID | Lookup to MST\_Employee |

| SM NAME | Sales Manager | TRN\_Case | SalesManagerID | Lookup to MST\_Employee |

| BANKER NAME | Banker Name | TRN\_Case | BankerName | Direct mapping |

| BANKER NUMBER | Banker Contact | TRN\_Case | BankerContact | Clean phone number |

| BANK NAME | Lender | TRN\_Case | LenderID | Lookup to MST\_Lender |

| BRANCH | Branch | TRN\_Case | BranchName | Direct mapping |

| LOGIN AMT | Login Amount | TRN\_Case | LoginAmount | Parse numeric |

| SANCTION AMT | Sanction Amount | TRN\_Case | SanctionAmount | Parse numeric |

| DISBURSE AMT | Disbursed Amount | TRN\_Case | DisbursementAmount | Parse numeric |

| NET AMT | Net Amount | TRN\_Case | NetAmount | Parse numeric |

| RATE | Interest Rate | TRN\_Case | InterestRate | Parse decimal |

| TENURE | Tenure | TRN\_Case | Tenure | Parse months |

| LOGIN DATE | Login Date | TRN\_Case | LoginDate | Date parse |

| STATUS | Status | TRN\_Case | Status | Lookup to REF\_Status |

| SANCTION DATE | Sanction Date | TRN\_Case | SanctionDate | Date parse |

| DISB DATE | Disbursement Date | TRN\_Case | DisbursementDate | Date parse |

| REMARK | Remarks | TRN\_Case | Remarks | Direct mapping |

\#\#\# 7\.3 PF/Tenure Parsing

| Field | Source Value | Parse Rule | Target Field |

|\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| PF | \`30000\(3%\)\` | Extract 30000 and 3% | TRN\_Case\.ProcessingFee, TRN\_Case\.ProcessingFeeRate |

| TENURE | \`36M\` | Strip M, convert to int | TRN\_Case\.TenureMonths = 36 |

| TENURE | \`2\+4\` | Sum \(2\+4=6\) | TRN\_Case\.TenureMonths = 6 |

\#\#\# 7\.4 Data Standardization

| Source Value | Target Value | Rule |

|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-|

| \`REJECT\` | REJECTED | Standardize status |

| \`LOGIN DONE \- IN PROCESS\` | IN\_PROCESS | Standardize status |

| \`DISBURSED\(BT\+TOP UP\)\` | DISBURSED | Standardize status |

| \`ONLINE\`, \`online\`, \`Online\` | ONLINE | Standardize payment mode |

\-\-\-

\#\# 8\. Mapping Cross\-Reference

\#\#\# 8\.1 Source\-to\-Target Summary

| Source File | Target Tables | Complexity |

|\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-|

| Secured Tracker | TRN\_Case, TRN\_Commission, MST\_Customer, MST\_Connector, MST\_Lender | High |

| Connector Master | MST\_Connector, MST\_PartyBankAccount, RUL\_CommissionRule, RUL\_CommissionSlab | High |

| Lender Payout Data | MST\_Lender, MST\_Product, RUL\_CommissionRule, RUL\_ValidationRule | Medium |

| Salary Data | MST\_Employee, MST\_PartyBankAccount, TRN\_Salary, TRN\_StatutoryPayment | High |

| Rent Files | MST\_Party, MST\_Property, TRN\_RentAgreement, TRN\_RentPayment | Medium |

| DSR Files | TRN\_Case | Low |

\#\#\# 8\.2 Data Quality Checks

| Check ID | Check Description | Implementation |

|\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-|

| QC\-001 | All required fields populated | Validation Rule |

| QC\-002 | Foreign key references valid | Referential Integrity |

| QC\-003 | Date order valid | Business Rule |

| QC\-004 | Amounts within expected ranges | Validation Rule |

| QC\-005 | Status values valid | Reference Data Lookup |

\#\#\# 8\.3 ETL Processing Order

\`\`\`

┌─────────────────────────────────────────────────────────────────┐

│                    ETL PROCESSING ORDER                         │

├─────────────────────────────────────────────────────────────────┤

│                                                                 │

│  1\. Load Reference Data \(REF\_ tables\)                          │

│  2\. Load Configuration \(CFG\_ tables\)                           │

│  3\. Load Master Data \(MST\_ tables\)                             │

│     a\. MST\_Company                                             │

│     b\. MST\_InternalRegion, MST\_InternalBranch, MST\_Team       │

│     c\. MST\_Lender                                              │

│     d\. MST\_Product                                             │

│     e\. MST\_Connector                                           │

│     f\. MST\_Employee                                            │

│     g\. MST\_Customer                                            │

│  4\. Load Rules \(RUL\_ tables\)                                   │

│     a\. RUL\_CommissionRule, RUL\_CommissionSlab                 │

│     b\. RUL\_ValidationRule                                      │

│     c\. RUL\_TDSRule, RUL\_GSTRule                                │

│  5\. Load Transactions \(TRN\_ tables\)                            │

│     a\. TRN\_Case                                                │

│     b\. TRN\_Commission                                          │

│     c\. TRN\_Salary                                              │

│     d\. TRN\_RentAgreement, TRN\_RentPayment                     │

│  6\. Run Validation                                             │

│  7\. Generate Reports                                           │

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

\*\*This document is designated as an ETL Baseline Artefact\.\*\*

\*\*Following approval:\*\*

\- Structural changes to mapping rules require a new Architecture Decision Record \(ADR\)\.

\- Changes to source\-to\-canonical mappings require Architecture Review Board \(ARB\) approval\.

\- All ETL development shall use this document as the governing mapping baseline\.

\*\*Freeze Status:\*\* ✅ \*\*FROZEN\*\*

\#\#\# 9\.3 Approval Sign\-Off

| Role | Name | Signature | Date |

|\-\-\-\-\-\-|\-\-\-\-\-\-|\-\-\-\-\-\-\-\-\-\-\-|\-\-\-\-\-\-|

| Enterprise Architect | Architecture Review Board | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

| ETL Lead | \[Name\] | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

| Data Architect | \[Name\] | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_/\_\_\_/2026 |

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

| DOC\-010 | Architecture & ADRs referencing mapping decisions |

| DOC\-011 | Data Model referenced for all target tables |

| DOC\-014 | Finance & Operations referencing business logic |

| DOC\-017 | Core Modules referencing ETL implementation |

| DOC\-021 | FCPL Industry Configuration for reference data |

| DOC\-023 | Rule Engine Translation Guide for formula mapping |

\-\-\-

\#\# End of Document

\*\*Document ID:\*\* DOC\-022  

\*\*Document Name:\*\* \*FCPL Source\-to\-Canonical Mapping Guide\*  

\*\*Version:\*\* 1\.0  

\*\*Status:\*\* Approved / Frozen  

\*\*Owner:\*\* CTO

