i want to develop this for my internal dsa and want results asap, i will share the excel sheets MIS we can have fro the dsa 1 by 1, ingest it for now and when i say complete we will decide way forward. # Data Assessment for Database Import: Fineoteric Rent & Payroll Files

## Executive Summary

You have provided **3 Excel files** containing:
1. **20 sheets** of rent agreement data (various properties across India)
2. **21 sheets** of Gold Crest rent data (multiple office units)
3. **3 sheets** of payroll/salary data

This assessment analyzes the structure, attributes, data quality issues, and provides recommendations for importing into a structured database.

---

## File 1: `1.RENT FOR FINEOTERIC PVT LTD FY 2026-27.xlsx`

### Sheets Overview

| Sheet Name | Purpose | Records | Key Attributes |
|------------|---------|---------|----------------|
| **Thane New** | Rent agreement with Amit Rayshi Kariya | 33 rows (3 year-cycles) | Tenant, gross rent, TDS@10%, GST@18%, net amount, payment dates |
| **Dadar New** | Rent agreement with Radheshyam Natraj (HUF) | 50+ rows | Tenant, gross rent, TDS@10%, net amount (no GST), payment dates |
| **UP New** | Rent agreement with Nikhil Talwar | 11 rows | Tenant, gross rent ₹35,000, **TDS=0**, payment dates |
| **ANDHERI EAST** | Rent agreement with Sandip Kumar Banerjee | 11 rows | Gross ₹60,000, TDS@10%, GST@18% |
| **PUNE NEW OFFICE** | Rent agreement with Rachna Parmand Lulla | 11 rows | Gross ₹25,000-50,000, **TDS=0, GST=0** |
| **PUNE NEW** | Rent agreement with Monish Parmand Lulla | 11 rows | Duplicate structure of PUNE NEW OFFICE |
| **HUBALI** | Rent agreement with Reshma Shetty | 36 rows (3 year-cycles) | Gross ₹19,000-20,948, TDS 0% (except first year), 5% annual escalation |
| **ANDHERI(MAROL OFFICE)** | Rent agreement with Saravana Murugan Yadhav | 12 rows | Gross ₹55,000, TDS@10%, GST@18% |
| **THANE Usman** | Rent agreement with Mohd Usman Khan | 24 rows | Gross ₹54,000-56,700, TDS@10%, deposit ₹150,000 noted |
| **CHEENAI OFFICE-Closed** | Rent agreement with Rankraze Ecoworks | 11 rows | Partial data, **some gross amounts missing** |
| **UP-Closed** | Rent agreement with Kiran H Sinha | 22 rows (2 agreements) | Gross ₹24,000→₹25,200, TDS@10% |
| **Hyderabad** | Rent agreement with Apeejay Business Centre | 23 rows | Gross ₹10,534-20,738, TDS@10%, GST@18% |
| **Inv- Bangalore** | Rent agreement with K K Radhakrishna | 36 rows (3 years) | Gross ₹60,000→₹66,150, TDS@10%, GST@18% |
| **Belapur** | Rent agreement with Patel Microdata | 11 rows | Gross ₹46,200, TDS@10%, GST@18% |
| **Chennai** | Rent agreement with Regus Chennai | 7 rows | Gross ₹27,600, GST@18%, TDS partial |
| **Ahmedabad** | Rent agreement with Flexi Business Hub | 22 rows | Variable gross, TDS@0-10%, GST@18% |
| **PUNE** | Rent agreement with Anant Rajendra Shirole | 57 rows (3 years) | Gross ₹40,000→₹44,100, TDS@10%, deposit ₹120,000 |
| **THANE-SURESH** | Rent agreement with Suresh Roopnarayan Upadhyay | 36 rows (3 years) | Gross ₹53,000→₹58,433, TDS@10%, some months TDS@20% |
| **Dadar -Closed** | Rent agreement with Sanjay Mahadeo Kelkar | 36 rows (3 years) | Gross ₹56,000→₹61,740, TDS@10% |
| **Noida** | Rent agreement with Usha Prashad | 33 rows | Rent + maintenance split, TDS@10% |

---

## File 2: `2.RENT FOR FINEOTERIC PVT LTD _Gold Crest FY 2026-27.xlsx`

### Sheets Overview

| Sheet Name | Purpose | Records | Key Attributes |
|------------|---------|---------|----------------|
| **710** | Office 710 - Pramesh Dilip Waghela | 60+ rows | Gross ₹31,500→₹44,100 over 5 years, TDS@10% |
| **711** | Office 711 - Dharmishta Pramesh Waghela | 60+ rows | Same structure as 710 |
| **905** | Office 905 - Harshada N. Desai | 78 rows | Gross ₹40,000→₹51,051 over 3 years, TDS@10%, GST@18% |
| **906** | Office 906 - Navinchandra Narandas Desai | 78 rows | Same as 905, some "HOLD" status |
| **907** | Office 907 - Sarvang N. Desai | 67 rows | Same structure, new agreement required |
| **908** | Office 908 - Sarvang N. Desai | 90+ rows | Full 3-year cycle with GST |
| **1405** | Office 1405 - Navinchandra Narandas Desai | 78 rows | Gross ₹40,000→₹51,051, GST@18% |
| **1406** | Office 1406 - Harshada Navinchandra Desai | 78 rows | Same as 1405 |
| **1407** | Office 1407 - Harshada N. Desai | 78 rows | Same structure |
| **Belapur New- Closed** | Patel Microdata - closed | 11 rows | Gross ₹44,000, TDS@10%, GST@18% |
| **609** | Office 609 - Usha Kantilal Pattani | 80+ rows | Gross ₹55,000→₹66,852, TDS varied (10-40%), deposit ₹200,000 |
| **UP** | Rishi Gupta / Shweta Gupta | 44 rows | Shared rent split between 2 parties, maintenance separate |
| **UP-2** | Shweta Gupta | 44 rows | Mirror of UP sheet |
| **1111- Closed** | Suresh G. Panchmatiya - closed | 35 rows | Gross ₹40,000→₹46,656, GST@18% |
| **1112-Closed** | Geeta Suresh Panchmatiya - closed | 35 rows | Same as 1111 |
| **LODHA -THANE-CLOSE** | Pankaj Hande - closed | 60+ rows | Gross ₹85,000→₹103,318, GST@18% |
| **804** | Doshi Kashyap/Pratik Mahendra | 36 rows | Gross ₹30,000→₹33,075, **no TDS, no GST** |
| **804- Amenities** | Same tenant - amenities | 36 rows | Separate amenities charge ₹20,000→₹22,050 |

---

## File 3: `Combine Salary Sheet APR-2026.xlsx` & `Salary Sheet May-2026.xlsx`

### Sheets Overview

| Sheet Name | Purpose | Columns | Key Attributes |
|------------|---------|---------|----------------|
| **Payroll Sheet (Apr'26)** | Employee salary calculation | 67 columns | Employee demographics, salary components (Basic, HRA, Allowances), deductions (PF, ESIC, PT, TDS), net payable, bank details |
| **Pivot** | Summary view | 3 columns | Salary summary by type (Commission vs Salary) |
| **Payroll Sheet (May'26)** | Salary calculation | 67 columns | Similar structure, additional new joiners noted |

### Employee Count: ~63 employees

---

## Critical Data Quality Issues

### ❌ **Parsing/Formula Dependencies**

**Issue:** Many numeric columns contain **Excel formulas** instead of raw values.

```
Examples:
- =F13*10%          (TDS calculation)
- =F13*18%          (GST calculation)
- =F13-G13+H13      (Net amount)
- =+E11-F11+G11     (Net amount with + prefix)
```

**Impact:** When importing, formulas will not evaluate automatically. Database import will see formula strings, not calculated values.

**Recommendation:** Pre-calculate values in Excel before import or implement formula evaluation in ETL pipeline.

---

### ❌ **Date Format Inconsistency**

| Format Example | Frequency |
|----------------|-----------|
| `2026-04-01 00:00:00` | Common (full datetime) |
| `2026-04-01` | Some sheets |
| `29-2-25` | 906 sheet |
| `31/05/2026` | UP-Closed |
| `2023-03-01 00:00:00` | Common |
| `2024-12-19` | Dadar-Closed (future payment date) |

**Recommendation:** Standardize to ISO format `YYYY-MM-DD` for database import.

---

### ❌ **Inconsistent GST/TDS Treatment**

| Property | TDS | GST | Notes |
|----------|-----|-----|-------|
| Thane New | 10% | 18% | Standard commercial |
| Dadar New | 10% | None | No GST column |
| UP New | 0% | None | TDS=0 |
| PUNE NEW OFFICE | 0% | 0% | No TDS/GST |
| HUBALI | 0% (most years) | None | 5% escalation |
| 609 | 10-40% | 18% | TDS varied (40% in one month) |

**Recommendation:** Normalize by creating tax type flags:
- `tds_applicable` (boolean)
- `tds_rate` (decimal)
- `gst_applicable` (boolean)
- `gst_rate` (decimal)

---

### ❌ **Duplicate/Mirror Sheets**

**Identified duplicates:**
- `PUNE NEW OFFICE` ↔ `PUNE NEW` (identical structure, different tenant names)
- `UP` ↔ `UP-2` (split between Rishi Gupta and Shweta Gupta)
- `1111-Closed` ↔ `1112-Closed` (different tenants, identical amounts)

**Recommendation:** Consolidate into a single tenant table with relationship mapping.

---

### ❌ **Missing/Null Payment Data**

| Sheet | Missing Payment Dates |
|-------|----------------------|
| Thane New | Periods 5-11 (2026-2027) |
| ANDHERI EAST | Periods 5-11 |
| ANDHERI(MAROL OFFICE) | Periods 2-12 |
| 906 | "HOLD" status for multiple periods |
| Chennai | Some payment dates missing |

**Recommendation:** Allow NULL values for pending/unknown payment dates.

---

### ❌ **Address Parsing Issues**

| Issue | Example |
|-------|---------|
| Multi-line addresses in single cell | `Unit No. 402, 4t floor, Raunak <br>Arcade, Gokhale Road, Naupada,` |
| Commas in addresses (CSV parsing issue) | `Marvel Artiza', CTS No. 4A/2, Third Floor – 301, Jayanagara,` |
| Inconsistent fields | Some have building, road, city in separate columns, some combined |

**Recommendation:** Split address into structured fields:
- `address_line_1`, `address_line_2`, `city`, `state`, `pincode`

---

### ❌ **Employee Data Issues**

| Issue | Example |
|-------|---------|
| Blank values for new joiners | Employee 64, 65 (no PAN, UAN, bank details) |
| Calculated salary fields | Gross = formula (e.g., `=40000-1800`) |
| Inconsistent marital status values | `MARRIED`, `married`, `Unmarried`, `Single`, `UNMARRIED` |
| Missing DOB | Employee 68, 69, 70 (DOB blank) |
| Duplicate employee entries | `HARSHADA DEEPAK WADEKAR` appears twice (FCPL0112 in Apr, May sheets) |
| Inconsistent date formats | `1993-06-10` vs `24-05-2004` |

---

### ❌ **Currency/Amount Precision Issues**

| Issue | Example |
|-------|---------|
| Decimal values | `46305` vs `48620.25` vs `51051.2625` |
| Inconsistent rounding | Some values rounded to 0 decimals, some to 2 decimals |
| Currency symbols | None specified (assumed INR) |

**Recommendation:** Use `DECIMAL(15,2)` for all monetary fields.

---

### ❌ **Redundant/Calculated Columns**

**Salary sheet has many derived columns:**
- `Total Leaves Gross Earning` (sum of Basic+HRA+Allowances)
- `Net Payable` (Gross - deductions)
- PF, ESIC, PT calculations

**Recommendation:** Store only base data in database, derive calculations in application layer.

---

### ❌ **Metacharacters in Sheet Names**

```
Thane New
Dadar New
UP New
ANDHERI  EAST (two spaces)
PUNE  NEW (two spaces)
HUBALI (mis-spelled Hubballi?)
ANDHERI(MAROL OFFICE) (no space)
Belapur New- Closed (hyphen)
LODHA -THANE-CLOSE (hyphen)
```

**Recommendation:** Clean sheet names: replace spaces/hyphens with underscores, handle parentheses.

---

## Structural Assessment

### ✅ **Strengths**

1. **Consistent rent table structure** across most sheets (SR NO, Period Start/End, Gross, TDS, GST, Net, Payment Date, Mode)
2. **Clear property categorization** by sheet name
3. **Annual escalation logic** documented (5% increases visible)
4. **Employee salary structure** has comprehensive fields
5. **Audit trail** - closed/active status indicated in sheet names

### ⚠️ **Weaknesses**

1. **No unique identifiers** - no property ID, tenant ID, employee ID system
2. **No foreign key relationships** - sheets are standalone
3. **Historical data mixed with current** (closed agreements still present)
4. **No data dictionary** - column meanings inferred from labels
5. **No normalization** - tenant names repeated across sheets
6. **Payment mode inconsistent** (`Online` vs `ONLINE` vs `online` vs `Online/Cheque`)

---

## Proposed Database Schema

### Core Tables

```sql
-- ============================================
-- Tenant/Landlord Master
-- ============================================
CREATE TABLE tenants (
    tenant_id SERIAL PRIMARY KEY,
    tenant_name VARCHAR(255) NOT NULL,
    legal_name VARCHAR(255),  -- HUF, LLP, Pvt Ltd
    pan VARCHAR(20),
    gstin VARCHAR(20),
    address_line_1 VARCHAR(255),
    address_line_2 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    pincode VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- Property Master
-- ============================================
CREATE TABLE properties (
    property_id SERIAL PRIMARY KEY,
    property_code VARCHAR(50),  -- Sheet name alias
    property_name VARCHAR(255),
    address_line_1 VARCHAR(255),
    address_line_2 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    pincode VARCHAR(10),
    property_type VARCHAR(50),  -- Commercial, Office, Co-working
    owner_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- Rent Agreements
-- ============================================
CREATE TABLE rent_agreements (
    agreement_id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(tenant_id),
    property_id INTEGER REFERENCES properties(property_id),
    agreement_start_date DATE NOT NULL,
    agreement_end_date DATE NOT NULL,
    agreement_document_date DATE,
    monthly_rent DECIMAL(15,2) NOT NULL,
    security_deposit DECIMAL(15,2),
    tds_applicable BOOLEAN DEFAULT FALSE,
    tds_rate DECIMAL(5,2) DEFAULT 0,
    gst_applicable BOOLEAN DEFAULT FALSE,
    gst_rate DECIMAL(5,2) DEFAULT 0,
    escalation_percent DECIMAL(5,2) DEFAULT 0,
    escalation_frequency VARCHAR(20),  -- Annual, Yearly
    agreement_status VARCHAR(20) DEFAULT 'Active',  -- Active, Closed, Expired
    source_sheet VARCHAR(100),  -- Track original sheet
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- Rent Payments
-- ============================================
CREATE TABLE rent_payments (
    payment_id SERIAL PRIMARY KEY,
    agreement_id INTEGER REFERENCES rent_agreements(agreement_id),
    rent_period_start DATE NOT NULL,
    rent_period_end DATE NOT NULL,
    gross_amount DECIMAL(15,2) NOT NULL,
    tds_amount DECIMAL(15,2) DEFAULT 0,
    gst_amount DECIMAL(15,2) DEFAULT 0,
    net_amount DECIMAL(15,2) NOT NULL,
    payment_due_date DATE,
    payment_date DATE,
    payment_mode VARCHAR(50),  -- Online, Cheque, Cash
    payment_status VARCHAR(20) DEFAULT 'Pending',  -- Paid, Pending, Hold
    utr_reference VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- Employees
-- ============================================
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    employee_code VARCHAR(50) UNIQUE NOT NULL,  -- FIN00023, FCPL0112
    full_name VARCHAR(255) NOT NULL,
    gender VARCHAR(10),
    date_of_birth DATE,
    father_name VARCHAR(255),
    marital_status VARCHAR(20),
    pan VARCHAR(20),
    aadhar_number VARCHAR(20),
    email VARCHAR(255),
    mobile_number VARCHAR(15),
    address TEXT,
    date_of_joining DATE,
    designation VARCHAR(100),
    department VARCHAR(100),
    team_name VARCHAR(100),
    branch_name VARCHAR(100),
    pf_applicable BOOLEAN DEFAULT FALSE,
    esic_applicable BOOLEAN DEFAULT FALSE,
    uan_number VARCHAR(20),
    bank_name VARCHAR(100),
    bank_account_number VARCHAR(50),
    bank_ifsc VARCHAR(20),
    current_status VARCHAR(20) DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- Salary Structure (monthly)
-- ============================================
CREATE TABLE salary_structures (
    salary_structure_id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(employee_id),
    effective_month DATE NOT NULL,
    gross_salary DECIMAL(15,2),
    basic_da DECIMAL(15,2),
    hra DECIMAL(15,2),
    other_allowance DECIMAL(15,2),
    special_allowance DECIMAL(15,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(employee_id, effective_month)
);

-- ============================================
-- Salary Payments
-- ============================================
CREATE TABLE salary_payments (
    salary_payment_id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(employee_id),
    pay_month DATE NOT NULL,
    payable_days INTEGER,
    one_day_salary DECIMAL(15,2),
    gross_earnings DECIMAL(15,2),
    pf_employee DECIMAL(15,2) DEFAULT 0,
    esic_employee DECIMAL(15,2) DEFAULT 0,
    professional_tax DECIMAL(15,2) DEFAULT 0,
    mlwf DECIMAL(15,2) DEFAULT 0,
    tds_amount DECIMAL(15,2) DEFAULT 0,
    advance_salary DECIMAL(15,2) DEFAULT 0,
    net_payable DECIMAL(15,2),
    payment_date DATE,
    utr_number VARCHAR(100),
    payment_status VARCHAR(20) DEFAULT 'Pending',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(employee_id, pay_month)
);

-- ============================================
-- Salary components audit
-- ============================================
CREATE TABLE salary_components (
    component_id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(employee_id),
    pay_month DATE NOT NULL,
    component_type VARCHAR(50),  -- Basic, HRA, Allowance, Overtime
    amount DECIMAL(15,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- PF/ESIC Challan tracking
-- ============================================
CREATE TABLE statutory_challans (
    challan_id SERIAL PRIMARY KEY,
    challan_type VARCHAR(20),  -- PF, ESIC
    pay_month DATE NOT NULL,
    total_wages DECIMAL(15,2),
    employee_share DECIMAL(15,2),
    employer_share DECIMAL(15,2),
    total_amount DECIMAL(15,2),
    payment_date DATE,
    challan_number VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- Tax calculation audit
-- ============================================
CREATE TABLE tax_details (
    tax_id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(employee_id),
    financial_year VARCHAR(20),
    monthly_tds DECIMAL(15,2),
    cumulative_tds DECIMAL(15,2),
    estimated_total_income DECIMAL(15,2),
    estimated_tax_liability DECIMAL(15,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- Audits/Integrations Log
-- ============================================
CREATE TABLE import_logs (
    log_id SERIAL PRIMARY KEY,
    source_file VARCHAR(255),
    source_sheet VARCHAR(100),
    row_number INTEGER,
    entity_type VARCHAR(50),
    action VARCHAR(20),  -- INSERT, UPDATE, SKIP
    status VARCHAR(20),  -- SUCCESS, ERROR, WARNING
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Data Mapping Recommendations

### Tenant Normalization

Current tenant names that should be merged:
- `PRAMESH DILIP WAGHELA` ↔ `MRS. DHARMISHTA PRAMESH WAGHELA` (same family, different units)
- `NAVINCHANDRA NARANDAS DESAI` ↔ `HARSHADA N. DESAI` ↔ `SARVANG N. DESAI` (family members)
- `RISHI GUPTA` ↔ `SHWETA GUPTA` (shared agreement split)

### Property Normalization

Create property mapping:
- Gold Crest → Multiple units (710, 711, 905, 906, 907, 908, 1405, 1406, 1407)
- Each unit is a separate property with same building address

---

## Import Priority

| Priority | Task | Complexity |
|----------|------|------------|
| **1** | Tenant master (deduplicate & normalize) | Medium |
| **2** | Property master (extract addresses) | Low-Medium |
| **3** | Rent agreements (parse dates, amounts) | Medium |
| **4** | Rent payments (extract from tables) | Medium-High |
| **5** | Employees (deduplicate & validate) | Medium |
| **6** | Salary structures/payments | High (complex formulas) |
| **7** | PF/ESIC challan calculations | High |

---

## ETL Pipeline Recommendations

1. **Stage 1: Raw Import**
   - Import each sheet as-is into staging tables
   - Preserve original values (including formulas as text)

2. **Stage 2: Data Cleansing**
   - Parse dates using multiple format templates
   - Extract numeric values from formulas (pre-calculate)
   - Clean text fields (trim, standardize)

3. **Stage 3: Normalization**
   - Match tenants using fuzzy matching
   - Normalize property addresses
   - Deduplicate employees (PAN/Aadhar matching)

4. **Stage 4: Validation**
   - Check payment dates vs agreement dates
   - Validate tax calculations
   - Check for completeness

---

## Critical Errors to Address Before Import

| Error | Location | Impact | Fix |
|-------|----------|--------|-----|
| **Past payment dates in future** | Dadar-Closed row 4: `2024-12-19` | Payment date after period end | Review and correct |
| **TDS 40%** | 609 row 4: `=E13*40%` | Unusual TDS rate | Verify with source |
| **Duplicated rent** | 609 rows 4-5 have duplicate periods | Data integrity issue | Remove duplicate |
| **Income tax deduction formula** | Salary sheet: `=AI50*2%` | Incorrect TDS calculation | Review with finance team |
| **Gross salary formula** | Salary sheet: `=40000-1800` | Hardcoded deduction | Store base salary separately |

---

## Recommendations for Next Steps

1. **Establish a data dictionary** - Define each field's purpose, format, and validation rules
2. **Build validation rules** - Check data types, ranges, and business logic
3. **Create mapping tables** - Tenant aliases, property codes, sheet name → table mappings
4. **Implement incremental imports** - Load only new/changed data
5. **Automate formula evaluation** - Use openpyxl/XLConnect to evaluate formulas before import
6. **Add audit columns** - `created_by`, `created_at`, `updated_by`, `updated_at` in every table
7. **Create a lookup for payment modes** - Standardize `Online`, `ONLINE`, `online` → `ONLINE`

---

## Estimated Effort

| Phase | Effort | Description |
|-------|--------|-------------|
| Schema Design | 1-2 days | Finalize tables, relationships, data types |
| ETL Development | 5-7 days | Build import scripts for all sheets |
| Data Cleansing | 3-5 days | Handle inconsistencies, deduplication |
| Validation | 2-3 days | Test imports, verify calculations |
| Deployment | 1 day | Production migration |

**Total Estimated: ~2-3 weeks**

---

Would you like me to:
1. Create specific Python/R scripts for data extraction?
2. Design a more detailed ETL pipeline architecture?
3. Create a sample output for one sheet to validate the mapping?
4. Provide SQL scripts for table creation?

---

## Data Assessment for Database Import: DSR – BL and PL MIS – APRIL_2026.xlsx

---

### Executive Summary

This file contains **two sheets** tracking **Business Loan (BL)** and **Personal Loan (PL)** applications for the month of April 2026. The data captures the entire loan lifecycle from login to sanction to disbursement, along with stakeholder details (connectors, unit heads, sales managers, bankers) and financial parameters.

| Sheet | Purpose | Records (approx.) | Key Attributes |
|-------|---------|-------------------|----------------|
| **BL** | Business Loan applications | ~250 rows | Company/Customer details, loan amount, sanction/disbursement, rate, PF, insurance, tenure, status, dates, banker info |
| **PL** | Personal Loan applications | ~167 rows | Similar structure with customer name, product, loan amount, tenure, status, banker details |

This assessment evaluates the structure, data consistency, quality issues, and provides a recommended schema for importing into a structured database.

---

### Sheet Overview

#### BL Sheet Columns

| Column | Description | Data Type Issues |
|--------|-------------|------------------|
| SR NO | Serial number | Numeric (1-~250) |
| APP NO | Application number | Mixed: some blank, some alphanumeric (`AP0181006`, `A808532`, `US0003545643`, `169780941`) |
| MONTH | Month of record | Date (all are `2026-04-26 00:00:00`) – repeated |
| COMPANY NAME | Business name | Free text, many blank |
| CUSTOMER NAME | Applicant name | Free text, many blank |
| PROFILE | Applicant profile | Values like `SENP` (likely Senior Professional) |
| PRODUCT | Loan product | Values like `SBL-TL`, `SBL-OD`, `BL-TL`, `BL-OD` |
| CONNECTOR NAME | Referrer/connector | Free text, often blank |
| UNIT HEAD | Unit head name | Free text, many blank |
| SM NAME | Sales manager name | Free text, often blank |
| BANKER NAME | Bank relationship manager | Free text |
| BANKER NUMBER | RM contact number | Mixed: some numeric, some with spaces |
| BANK NAME | Lender bank | e.g., `FT CASH`, `PROTIUM`, `TATA`, `INDIFI`, `PIRAMAL`, `ABFL`, etc. |
| CODE | Possibly branch code? | Often blank or `FINEOTERIC CONSULTING PVT LTD` |
| BRANCH | Branch/location | e.g., `ANDHERI`, `PUNE`, `DELHI`, `MUMBAI`, etc. |
| LOGIN AMT | Loan amount applied | Numeric (often 1,500,000 or 3,000,000) |
| SANCTION AMT | Amount sanctioned | Numeric, often blank if not sanctioned |
| DISBURSE AMT | Amount disbursed | Numeric, often blank |
| NET AMT | Net amount? | Often same as disbursed or blank |
| RATE | Interest rate | Decimal (e.g., 0.24, 0.209) |
| PF | Processing fee? | Mixed: sometimes numeric, sometimes with `(3%)` text, e.g., `30000(3%)` |
| INSURANCE | Insurance amount | Numeric or blank |
| TENURE | Loan tenure | Mixed: `36M`, `36.0`, `48.0`, sometimes `2+4` |
| SUBVENTION | Subvention rate | Often 0.0 |
| REGION | Region | All `WEST` |
| LOGIN DATE | Application login date | Date (many with time component) |
| STATUS | Application status | `REJECTED`, `DISBURSED`, `APPROVED`, `HOLD`, `LOGIN DONE - IN PROCESS` |
| SANCTION DATE | Sanction date | Date, often blank |
| DISB DATE | Disbursement date | Date, often blank |
| REMARK | Additional notes | Free text, often blank or explanation for rejection |

#### PL Sheet Columns (similar, with variations)

- Column names differ slightly: `BANK RM NAME` instead of `BANKER NAME`, `LOGIN AMOUNT` instead of `LOGIN AMT`, `DISB AMT` instead of `DISBURSE AMT`.
- `CONNECTOR` instead of `CONNECTOR NAME`.
- `REMARKS` (plural) vs `REMARK`.

---

### Critical Data Quality Issues

#### ❌ **Inconsistent Data Types in Numeric Fields**

| Column | Issue | Example |
|--------|-------|---------|
| **PF** (Processing Fee) | Contains text and numbers mixed | `30000(3%)`, `37500.0`, `14374`, `7670`, `17797` – some with percentages |
| **INSURANCE** | Sometimes blank, sometimes numeric | `12624.82`, `15049.0`, `63750.0` |
| **TENURE** | Mixed formats | `36M`, `36.0`, `48.0`, `72M`, `2+4`, `12+36` – need to parse months |
| **RATE** | Decimal with various precision | `0.24`, `0.209`, `0.17`, `0.1035` |
| **LOGIN AMT/SANCTION AMT** | Large numbers with decimals? | Mostly integers but could be decimal; need to treat as `DECIMAL(15,2)` |

**Impact:** These fields cannot be imported directly as numeric; parsing logic required.

---

#### ❌ **Missing and Sparse Data**

- **CUSTOMER NAME** is blank in many BL rows (e.g., rows 2,3,4,5, etc.).
- **COMPANY NAME** also often blank.
- **CONNECTOR NAME** / **CONNECTOR** is blank in many rows.
- **UNIT HEAD** and **SM NAME** are frequently blank.
- **SANCTION DATE** and **DISB DATE** are blank unless status is DISBURSED/APPROVED.
- Many rows have status `REJECTED` with no rejection reason; some have REMARK but not consistently.

**Impact:** Need to allow NULLs; consider default values for missing fields.

---

#### ❌ **Duplicate/Repeated Application Numbers**

- The same `APP NO` appears across multiple rows for the same customer, possibly for different lenders (e.g., `LEELADHAR ENTERPRISES` appears multiple times with different bankers).
- For a given customer/company, multiple login attempts to different banks are recorded separately. This is acceptable but requires careful modeling.

**Impact:** Need to identify the unique loan application per lender; the `APP NO` may be lender-specific.

---

#### ❌ **Inconsistent Date Formats**

- **MONTH** column is a timestamp: `2026-04-26 00:00:00` – all rows share the same date, likely the reporting month.
- **LOGIN DATE**, **SANCTION DATE**, **DISB DATE** are mixed: some have time `00:00:00`, some are like `2026-04-07`, others like `2026-04-01 00:00:00`. No consistency.

**Impact:** Standardize to `DATE` type (YYYY-MM-DD) during import.

---

#### ❌ **Inconsistent Categorical Values**

- **STATUS** values: `REJECTED`, `DISBURSED`, `APPROVED`, `HOLD`, `LOGIN DONE - IN PROCESS`, `REJECT`, `APPROVED`, `DISBURSED(BT+TOP UP)`, etc. Some with extra descriptions.
- **BANK NAME** has many variations: `FT CASH`, `PROTIUM`, `TATA`, `INDIFI`, `PIRAMAL`, `ABFL`, `FLEXI LOAN`, `GODREJ CAPITAL`, `L&T`, etc. Could be normalized.
- **PRODUCT** values: `SBL-TL`, `SBL-OD`, `BL-TL`, `BL-OD`, `PL`, `PL-OD` – need to classify.

**Impact:** Create lookup tables for status, product, bank.

---

#### ❌ **Spelling and Punctuation Errors**

- `DISBURSE AMT` vs `DISB AMT` – column names differ between sheets.
- `BANKER NAME` vs `BANK RM NAME` – could be mapped to same field.
- `REMARK` vs `REMARKS` – align.

**Impact:** Need to define a unified schema and map columns.

---

#### ❌ **Amount Fields with Units**

- **PF** sometimes includes a percentage in parentheses like `30000(3%)`. This should be split into a numeric fee and a rate.

**Impact:** Parsing required to extract numeric and percentage.

---

#### ❌ **Duplicate Sheet Structures**

The two sheets (BL and PL) are nearly identical but with slight column name variations. They can be combined into a single table with a `loan_type` field (BL/PL) and appropriate column mappings.

---

### Structural Strengths

✅ **Clear separation of loan type** – BL and PL sheets allow for different products.  
✅ **Each row represents a unique loan application attempt** – good for transactional tracking.  
✅ **Includes important dates** – login, sanction, disbursement – enabling lifecycle analysis.  
✅ **Has stakeholder fields** – connector, unit head, SM, banker – useful for performance tracking.  
✅ **Financial metrics** – amounts, rates, tenure, fees – comprehensive.

---

### Proposed Database Schema

Based on the analysis, we recommend a normalized schema with the following core tables:

```sql
-- ============================================
-- Loan Application Master (unified for BL & PL)
-- ============================================
CREATE TABLE loan_applications (
    application_id SERIAL PRIMARY KEY,
    loan_type VARCHAR(10) NOT NULL,          -- 'BL' or 'PL'
    application_number VARCHAR(50),           -- APP NO (can be blank)
    report_month DATE NOT NULL,               -- MONTH (e.g., 2026-04-26)
    company_name VARCHAR(255),
    customer_name VARCHAR(255),
    profile VARCHAR(50),                      -- e.g., SENP, SEP
    product VARCHAR(50),                      -- e.g., SBL-TL, BL-OD, PL
    connector_name VARCHAR(255),
    unit_head VARCHAR(255),
    sales_manager VARCHAR(255),
    banker_name VARCHAR(255),
    banker_contact VARCHAR(20),
    bank_name VARCHAR(100),
    branch_code VARCHAR(50),
    branch_location VARCHAR(100),
    login_amount DECIMAL(15,2),
    sanction_amount DECIMAL(15,2),
    disbursed_amount DECIMAL(15,2),
    net_amount DECIMAL(15,2),                 -- often same as disbursed
    interest_rate DECIMAL(6,4),               -- RATE
    processing_fee DECIMAL(15,2),             -- PF (numeric part)
    processing_fee_rate DECIMAL(6,4),         -- extracted from PF if present as percentage
    insurance_amount DECIMAL(15,2),
    tenure_months INTEGER,                    -- parse from TENURE
    subvention DECIMAL(6,4),
    region VARCHAR(50),
    login_date DATE,
    sanction_date DATE,
    disbursement_date DATE,
    status VARCHAR(50),                       -- REJECTED, DISBURSED, APPROVED, HOLD, etc.
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- Lookup Tables (for normalization)
-- ============================================
CREATE TABLE loan_status_lookup (
    status_code VARCHAR(20) PRIMARY KEY,
    status_description VARCHAR(100)
);

CREATE TABLE bank_lookup (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) UNIQUE,
    bank_short_name VARCHAR(50)
);

CREATE TABLE product_lookup (
    product_code VARCHAR(20) PRIMARY KEY,
    product_description VARCHAR(100),
    loan_type VARCHAR(10)  -- BL or PL
);

-- ============================================
-- Additionally, track application attempts per customer/company
-- ============================================
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(255),
    company_name VARCHAR(255),
    -- additional fields if needed
);

-- ============================================
-- And link applications to customers (optional)
-- ============================================
```

#### Mapping Considerations

| Source Field | Target Field | Notes |
|--------------|--------------|-------|
| SR NO | Not stored (row order) | Could be used as order, but not needed |
| APP NO | application_number | Handle blank |
| MONTH | report_month | Standardize to DATE |
| COMPANY NAME | company_name | Allow NULL |
| CUSTOMER NAME | customer_name | Allow NULL |
| PROFILE | profile | Free text |
| PRODUCT | product | Link to product lookup |
| CONNECTOR NAME / CONNECTOR | connector_name | Use same field |
| UNIT HEAD | unit_head | |
| SM NAME | sales_manager | |
| BANKER NAME / BANK RM NAME | banker_name | Map both |
| BANKER NUMBER / RM NUMBER | banker_contact | Clean phone numbers |
| BANK NAME | bank_name | Normalize via lookup |
| CODE | branch_code | Often blank, could be omitted |
| BRANCH | branch_location | |
| LOGIN AMT / LOGIN AMOUNT | login_amount | Use DECIMAL |
| SANCTION AMT / SANCTION AMOUNT | sanction_amount | |
| DISBURSE AMT / DISB AMT | disbursed_amount | |
| NET AMT | net_amount | |
| RATE | interest_rate | |
| PF | processing_fee / processing_fee_rate | Parse if contains `(xx%)` |
| INSURANCE | insurance_amount | |
| TENURE | tenure_months | Parse: strip 'M', handle '2+4' → sum? Or store as text? Better to parse to months (e.g., `2+4` = 6? But ambiguous). Could store as original and have derived column. |
| SUBVENTION | subvention | |
| REGION | region | All WEST |
| LOGIN DATE | login_date | |
| STATUS | status | Use lookup |
| SANCTION DATE | sanction_date | |
| DISB DATE / DISB DATE | disbursement_date | |
| REMARK / REMARKS | remarks | |

---

### Data Cleansing Recommendations

1. **Date Standardization**
   - Convert all date strings to `YYYY-MM-DD` using `pd.to_datetime` with errors='coerce'.

2. **Parsing PF Field**
   - Use regex to extract numeric value and percentage (if present). Example: `30000(3%)` → fee=30000, rate=0.03. If no percentage, store fee only.

3. **Tenure Parsing**
   - If ends with `M`, strip and convert to integer.
   - If contains `+` (e.g., `2+4`), decide whether to sum or store separately; simplest: store original text in a `tenure_original` field and keep `tenure_months` as sum.

4. **Handling Blank Values**
   - All text fields: default to NULL or empty string.
   - Numeric: NULL if blank.

5. **Deduplication?**
   - Since each row is a unique loan attempt (different lenders), we may keep all rows. For a unique application across lenders, use the `application_number` (APP NO) which is often unique per lender. But if APP NO is blank, we cannot dedupe. We'll store all.

6. **Column Name Mapping**
   - Create a mapping dictionary to unify BL and PL sheets into one import process.

7. **Status Standardization**
   - Map variations (e.g., `REJECT` → `REJECTED`, `APPROVED` → `APPROVED`, `DISBURSED` → `DISBURSED`, `HOLD` → `HOLD`, `LOGIN DONE - IN PROCESS` → `IN_PROGRESS`). Keep original also as a note.

---

### Import Priority & Effort

| Priority | Task | Complexity |
|----------|------|------------|
| 1 | Build schema (unified loan_applications + lookups) | Low |
| 2 | Clean and parse PF, tenure, dates | Medium |
| 3 | Import both sheets with column mapping | Medium |
| 4 | Validate amounts and statuses | Low |
| 5 | Create indexes on dates, status, bank, product | Low |

**Estimated Effort:** ~2 days for schema design, parsing, and import.

---

### Summary of Recommendations

- **Unify BL and PL** into a single table with `loan_type` discriminator.
- **Normalize categorical fields** with lookup tables (status, product, bank).
- **Parse complex fields** (PF, tenure) into structured numeric columns while retaining original for audit.
- **Allow NULLs** for missing data.
- **Standardize dates** to ISO format.
- **Add audit columns** (`created_at`, `updated_at`).

---

Would you like me to:
1. Provide a sample Python script for parsing and importing these sheets?
2. Design a more detailed ETL pipeline for this data?
3. Create additional tables for tracking connectors, unit heads, sales managers?

---

# Assessment: FCPL Connector Master Workbook

## 1. Executive Summary

This is a **complex, multi-sheet financial master data workbook** that serves as a contract-rate sheet between FCPL and its connectors. It contains **2,966 master rows** with a wide-format structure (62 columns) that combines:

- **Connector/Lender/Sub-product dimensions** (3 identity columns)
- **Inherited taxonomy** from Lender Master V3.3 (17 columns)
- **Rate buckets** (10 Base %, 10 Connector %, 10 Effective %)
- **Commercial & qualifying attributes** (5 columns for PF%, I%, conditions)

The workbook is well-documented with a **Column Dictionary** (62 detailed column definitions) and clearly structured business logic.

---

## 2. Overall Structure & Organization

### Sheet Breakdown

| Sheet Name | Purpose | Row Count | Key Characteristics |
|------------|---------|-----------|---------------------|
| **Overview** | Documentation & metadata | ~30 rows | Reference/instructional |
| **Column Dictionary** | Detailed column definitions | 62 rows | Reference/master data |
| **Master** | Main contract-rate data | **2,966 rows** | **Wide format**, 62 cols |
| **Connector Directory** | Bank Account Master | 741 rows | Connector lookup |
| **Reconciliation Summary** | Running balances | 927 rows | Per (connector × lender) |
| **Connector Advances** | EMI schedule (2 dummy rows) | Live formulas | WC/SC advances |

### Data Volume Summary
- **Master rows:** 2,966 unique (Connector × Lender × Sub-product) tuples
- **Connectors:** ~741 unique entities
- **Lenders:** Multiple banks & NBFCs (HDFC, Axis, ICICI, Tata Capital, etc.)
- **Sub-products:** Various (BL, PL, HL, LAP, etc.)

---

## 3. Data Model Analysis

### 3.1 Dimensions (Key Identifiers)

| Column Range | Columns | Type | Description |
|-------------|---------|------|-------------|
| A–C | 3 | **Connector Identity** | Sr No, Connector Code, Connector Name |
| D–T | 17 | **Product Taxonomy** | DSA, Lender, Type, Category, Sub-product, Channel, Borrower, Employer, Salary Range, Nature, Location, ROI %, DSA Code, Slab Type, Base %, Headline % |

### 3.2 Facts (Rate/Commercial Data)

| Column Range | Columns | Type | Description |
|-------------|---------|------|-------------|
| U–AD | 10 | **Lender-side Base %** | Bucketed by loan amount tiers |
| AE–AN | 10 | **Connector % share** | Editable, seeded from history |
| AO–AX | 10 | **Effective %** | **Live formula**: `=Base × Connector` |
| AY | 1 | Observed Cases (FY 25-26) | Historical case count |
| AZ–BD | 5 | **Qualifying attributes** | PF %, I %, Qualifying Notes, Commercial terms |
| BE | 1 | Clawback conditions | Free text |
| BF–BJ | 5 | **Contest block** | Frequency, Target, Bonus %, Period, Notes |

### 3.3 Bucket Tiers (10 value bands)

1. `< ₹50 L`
2. `₹50 L – < ₹1 Cr`
3. `₹1 Cr – < ₹2 Cr`
4. `₹2 Cr – < ₹3 Cr`
5. `₹3 Cr – < ₹5 Cr`
6. `₹5 Cr – < ₹10 Cr`
7. `₹10 Cr – < ₹25 Cr`
8. `₹25 Cr – < ₹50 Cr`
9. `₹50 Cr – < ₹100 Cr`
10. `≥ ₹100 Cr`

---

## 4. Key Observations & Data Quality

### 4.1 Strengths ✅

1. **Well-documented**: Complete Column Dictionary with examples, formats, and business logic
2. **Clear business rules**: Effective % formulas documented (`=IFERROR(Base × Connector, "NA")`)
3. **Consistent structure**: Wide-format follows a logical pattern (identity → taxonomy → rate buckets → commercial)
4. **Historical seeding**: Connector % values are seeded from FY25-26 tracker data
5. **Auditability**: Observed Cases column shows data provenance
6. **Live formulas**: Excel formulas reduce manual errors

### 4.2 Challenges & Considerations ⚠️

1. **Wide format challenges**:
   - 10 bucket columns × 3 = 30 columns for rates
   - Not ideal for database import (relational normalization needed)
   - Querying across buckets requires column pivoting

2. **Data quality issues observed**:
   - **Missing Connector Codes**: ~12% of rows have "NA" in Connector Code (rows with "AARY FINANCIAL SERVICES", "ABHIJEET DESHPANDE", etc.)
   - **Inconsistent naming**: Same entity appears under different names (e.g., "DIPALI ANIRUDDHA NEVREKAR" vs variations)
   - **Free-text fields**: Qualifying Notes, Commercial, Post-disbursement conditions contain unstructured data
   - **"NA" and blank values**: Significant amount of non-applicable data

3. **Nested logic complexity**:
   - Qualifying conditions encoded as `I+PF` or `I+ROI` strings
   - Commercial conditions in free text (e.g., "ROI > 16.50% AND ABOVE")
   - Contest attributes nested within single columns

4. **Data lineage concerns**:
   - Mix of April 2026 rate card and FY25-26 historical data
   - Connector rates are "seeded" but editable → version control needed

---

## 5. Database Import Recommendations

### 5.1 Suggested Normalization Strategy

Instead of a single 62-column table, consider a **star/snowflake schema**:

#### Fact Table: **connector_rates**
| Column | Type | Description |
|--------|------|-------------|
| id | BIGINT | Surrogate key |
| connector_id | BIGINT | FK to connectors |
| lender_id | BIGINT | FK to lenders |
| sub_product_id | BIGINT | FK to sub_products |
| bucket_id | BIGINT | FK to buckets |
| base_rate | DECIMAL(10,4) | Lender-side rate |
| connector_share | DECIMAL(10,4) | Connector % |
| effective_rate | DECIMAL(10,4) | Calculated rate |
| observed_cases | INT | Historical case count |
| effective_date | DATE | Rate effective date |
| created_at | TIMESTAMP | Audit |
| updated_at | TIMESTAMP | Audit |

#### Dimension Tables:

**connectors**
- id, code, name, normalized_name, is_active

**lenders**
- id, name, is_nbfc, dsa_code

**sub_products**
- id, name, category, type, channel, borrower_type, employer, salary_range, nature, location

**buckets**
- id, tier_name, lower_bound, upper_bound, tier_order

**qualifying_conditions**
- id, connector_rate_id, condition_type, condition_value
- For PF %, I %, ROI %, notes, clawback, commercial

**contests**
- id, connector_rate_id, frequency, target_amount, bonus_percent, period_start, period_end, notes

### 5.2 Transformation Requirements

| Current Column | Target Table | Notes |
|----------------|--------------|-------|
| A–C (Connector) | connectors | Deduplicate 741 unique connectors |
| D–T (Taxonomy) | product_taxonomy | Break into normalized dimensions |
| U–AD (Base %) | connector_rates | One row per bucket |
| AE–AN (Connector %) | connector_rates | One row per bucket |
| AO–AX (Effective %) | **Calculated** | `=Base × Connector` (store or compute) |
| AZ–BD | qualifying_conditions | Normalize conditions |
| BE | clawback_conditions | Free text or condition table |
| BF–BJ | contests | Normalize contest data |

### 5.3 ETL Pipeline Considerations

1. **Connector de-duplication**: 
   - Use fuzzy matching on name
   - Consolidate "NA" connector codes where possible
   - Create a master connector lookup

2. **Bucket unpivoting**:
   - Transform from wide to long format
   - Map 30 columns → 10 rows per connector-lender-subproduct

3. **Date dimension**:
   - Add effective date (April 2026)
   - Track historical changes

4. **Data cleansing**:
   - Parse `I+PF`, `I+ROI` codes into separate boolean flags
   - Extract numeric values from free text (e.g., ROI thresholds)
   - Standardize "NA" handling

---

## 6. Sample Table Schema (Simplified)

```sql
-- Core fact table with denormalized structure (if performance over normalization)
CREATE TABLE connector_rates (
    id SERIAL PRIMARY KEY,
    sr_no INTEGER,
    connector_code VARCHAR(50),
    connector_name VARCHAR(200),
    lender_name VARCHAR(100),
    is_nbfc BOOLEAN,
    product_type VARCHAR(50),
    category VARCHAR(10),
    sub_product VARCHAR(100),
    channel VARCHAR(20),
    borrower_type VARCHAR(50),
    employer_type VARCHAR(50),
    salary_range VARCHAR(50),
    loan_nature VARCHAR(20),
    location VARCHAR(50),
    roi_percent DECIMAL(10,4),
    dsa_code VARCHAR(50),
    slab_type VARCHAR(30),
    base_percent DECIMAL(10,4),
    headline_percent DECIMAL(10,4),
    
    -- Bucket columns (10 tiers)
    bucket_1_lower DECIMAL(15,2),
    bucket_1_upper DECIMAL(15,2),
    base_rate_1 DECIMAL(10,4),
    connector_share_1 DECIMAL(10,4),
    effective_rate_1 DECIMAL(10,4),
    -- ... repeats for buckets 2-10
    -- See normalized approach above for better design
    
    observed_cases INTEGER,
    qualifying_conditions VARCHAR(20),
    pf_percent DECIMAL(10,4),
    insurance_percent DECIMAL(10,4),
    qualifying_notes TEXT,
    commercial_terms TEXT,
    clawback_conditions TEXT,
    contest_frequency VARCHAR(20),
    contest_target DECIMAL(15,2),
    contest_bonus_percent DECIMAL(10,4),
    contest_period VARCHAR(50),
    contest_notes TEXT
);
```

### Normalized approach (recommended):

```sql
-- Core connector_rates table (unpivoted buckets)
CREATE TABLE connector_rates_long (
    id SERIAL PRIMARY KEY,
    connector_id INTEGER REFERENCES connectors(id),
    lender_id INTEGER REFERENCES lenders(id),
    sub_product_id INTEGER REFERENCES sub_products(id),
    bucket_id INTEGER REFERENCES buckets(id),
    base_rate DECIMAL(10,4),
    connector_share DECIMAL(10,4),
    effective_rate DECIMAL(10,4),  -- optional: store or compute
    observed_cases INTEGER,
    effective_date DATE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Supporting dimension tables as described above
```

---

## 7. Import Implementation Steps

1. **Pre-import validation**
   - Validate 2,966 rows match expected structure
   - Check for duplicate (connector × lender × sub-product) tuples
   - Identify and flag rows with missing connector codes

2. **Extract & Transform**
   - Parse all sheets using library (pandas, openpyxl, etc.)
   - Normalize connector names
   - Unpivot rate buckets (10 → rows)
   - Parse qualifying codes (`I+PF` → `has_insurance`, `has_pf`)
   - Extract numeric values from text fields

3. **Load strategy**
   - Option A: **Staging table** (load raw, then transform)
   - Option B: **Direct ETL** (transform in Python/SSIS before load)
   - Use **upsert logic** for incremental updates

4. **Post-load validation**
   - Verify row count matches
   - Check effective_rate = base_rate × connector_share
   - Validate foreign keys (connectors, lenders exist)

---

## 8. Key Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| **"NA" connector codes** | Cannot link to connector directory | Fuzzy match by name; create mapping table |
| **Free-text commercial terms** | Limited querying capability | Define structured fields for common terms |
| **Versioning** | April 2026 rate card + FY25-26 history | Add effective_date & version_id columns |
| **Wide format scalability** | Adding more buckets requires schema changes | Use long format (normalized) design |
| **Excel formulas** | Business logic in cells not data | Document formulas; compute in ETL |

---

## 9. Additional Recommendations

1. **Add audit columns**: `created_by`, `updated_by`, `version`, `is_current`
2. **Create lookup tables**: for all categorical columns (Type, Category, Channel, etc.)
3. **Implement soft deletes**: rather than hard deletions
4. **Build an API layer**: to serve rates to downstream systems
5. **Schedule regular updates**: monthly/quarterly rate card refresh

---

## 10. Summary

The FCPL Connector Master is a **well-structured but Excel-centric** data asset. While it's thoroughly documented and logically organized, its wide format presents normalization challenges for database import. The recommended approach is to **unpivot the 30 bucket columns** into a normalized star schema, clean the connector names for deduplication, and parse the commercial/qualifying fields into structured attributes.

The 2,966 rows represent a manageable volume, and the data quality is generally good with the exception of missing connector codes for some rows. The inclusion of live formulas (`Effective % = Base × Connector`) is a strength—consider storing both the raw inputs and the calculated result in the database.

**Estimated effort**: 3-5 days for ETL development, testing, and validation.

---

Would you like me to:
1. **Generate specific Python code** to parse and transform this file?
2. **Create a detailed migration plan** with SQL DDL statements?
3. **Help with connector deduplication** logic using fuzzy matching?
4. **Build a validation script** to check data quality before import?

---

# FCPL Lender Payout Data - Database Import Assessment

## Executive Summary

| Aspect | Assessment |
|--------|------------|
| **Total Rows** | 230 records |
| **Total Columns** | 39 columns |
| **Data Quality** | Mixed (structured + free-text) |
| **Import Readiness** | High with preprocessing |
| **Primary Challenge** | Mixed data types, inconsistent formatting |

---

## 1. Data Structure Overview

### 1.1 Schema Breakdown

```
┌─────────────────────────────────────────────────────────────┐
│                   39 Columns Total                          │
├─────────────────────────────────────────────────────────────┤
│ Identifier Columns:    Sr. No., DSA, Lender/NBFC, NBFC?    │
│ Classification:        Type, Category, Sub-product          │
│ Borrower Attributes:   Channel, Borrower, Employer, Salary  │
│ Loan Attributes:       Nature, Location                     │
│ Commercial:            ROI %, DSA Code, Slab Type           │
│ Commission Slabs:      Base %, Headline %, 10-tier buckets  │
│ Qualifying Conditions: Qualifying, PF %, I %, Qual Notes    │
│ Other:                 Commercial, Post-disbursement         │
│ Contests:              Frequency, Target, Bonus, Period     │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Category Distribution

| Category | Count | Percentage |
|----------|-------|------------|
| BL (Business Loan) | 80 | 34.8% |
| HL (Home Loan) | 45 | 19.6% |
| LAP (Loan Against Property) | 67 | 29.1% |
| PL (Personal Loan) | 38 | 16.5% |

### 1.3 DSA Distribution

| DSA | Count | Percentage |
|-----|-------|------------|
| FCPL | 192 | 83.5% |
| BW | 38 | 16.5% |

---

## 2. Detailed Column Assessment

### 2.1 ✅ **Well-Structured Columns (Ready for Direct Import)**

| Column | Data Type | Assessment |
|--------|-----------|------------|
| Sr. No. | Integer | Clean sequential numbering |
| DSA | Enum | FCPL/BW - consistent |
| Lender/NBFC | Text | Canonical names - consistent |
| NBFC? | Boolean | TRUE/FALSE - clean |
| Type | Enum | Secured/Unsecured - clean |
| Category | Enum | BL/HL/LAP/PL - clean |
| Sub-product | Text | Mostly clean, some nulls |
| Base % | Decimal | Clean percentages |
| Headline % | Decimal | Clean percentages |
| Slab Type | Enum | Flat/Loan-Amount/Achievement-Volume |

### 2.2 ⚠️ **Columns with Data Quality Issues**

| Column | Issues | Recommendation |
|--------|--------|----------------|
| **DSA Code** | Contains special chars, spaces, mixed formats | Normalize: strip quotes, clean whitespace |
| **Channel** | NA values inconsistent with empty strings | Standardize to NULL/NA |
| **Employer** | NA used extensively | Consider removing if >90% NA |
| **Salary Range** | Mostly NA (only 1 row populated) | Consider dropping or treating as metadata |
| **Nature** | Mostly "Fresh" (few exceptions) | Consider if needed |
| **Location** | Mixed "PAN INDIA", "Mumbai", "Metro Tier X" | Could create location hierarchy |
| **ROI %** | Some values as decimals, some null | Parse from Commercial text |
| **Qualifying Notes** | Free text with embedded data | Parse for PF/I/ROI extraction |
| **Commercial** | Free text with structured patterns | Contains ROI bands, subvention rules |
| **Post-disbursement** | Free text, many NA | Separate parsing needed |
| **Contest columns** | Mixed data across 5 columns | Create separate contest table |

### 2.3 🚨 **Critical Data Quality Findings**

#### **Commission Slab Columns (S through AB) - 10 columns**

```
Issue: Mixed use of NA and 0 values across different rows
- Some rows: All NA (Flat type)
- Some rows: All populated (Loan-Amount/Achievement-Volume)
- Some rows: Partial population
- Decimal precision varies (2-4 decimal places)
```

**Example - Row 7 (Axis Bank BL):**
```
< ₹50 L: 0.031
₹50 L – < ₹1 Cr: 0.031
₹1 Cr – < ₹2 Cr: 0.0325
₹2 Cr – < ₹3 Cr: 0.035
₹3 Cr – < ₹5 Cr: 0.035
₹5 Cr – < ₹10 Cr: 0.035
₹10 Cr – < ₹25 Cr: 0.036
₹25 Cr – < ₹50 Cr: 0.037
₹50 Cr – < ₹100 Cr: 0.037
≥ ₹100 Cr: 0.037
```

#### **Qualifying Columns (AC through AF)**

| Column | Pattern | Sample |
|--------|---------|--------|
| Qualifying | I+PF / I / PF / ROI / NA | "I+PF" |
| PF % | Decimal or NA | 0.02, 0.025, NA |
| I % | Decimal or NA | 0.01, NA |
| Qualifying Notes | Free text | "(1.25% pf + Insurance Mandatory)" |

**Issue:** Qualifying notes contain structured data that could be parsed further.

---

## 3. Data Type Mapping for Import

### 3.1 Recommended Data Types

| Column Range | Recommended Type | Example |
|--------------|------------------|---------|
| Sr. No. | `INTEGER` | 1 |
| DSA | `VARCHAR(10)` | FCPL |
| NBFC? | `BOOLEAN` | TRUE |
| Base %, Headline % | `DECIMAL(10,4)` | 0.0400 |
| All slab columns | `DECIMAL(10,4)` | 0.0310 |
| Contest Target (₹) | `BIGINT` | 170000000 |
| Qualifying | `VARCHAR(20)` | I+PF |
| PF %, I %, ROI % | `DECIMAL(10,4)` | 0.0200 |
| All other text | `VARCHAR(255)` or `TEXT` | - |

### 3.2 Suggested Schema (Staging Table)

```sql
CREATE TABLE lender_payouts_staging (
    -- Identifiers
    sr_no INTEGER PRIMARY KEY,
    dsa VARCHAR(10),
    lender_name VARCHAR(100),
    is_nbfc BOOLEAN,
    loan_type VARCHAR(20),
    category VARCHAR(10),
    sub_product VARCHAR(100),
    channel VARCHAR(20),
    borrower_type VARCHAR(50),
    employer_type VARCHAR(30),
    salary_range VARCHAR(50),
    loan_nature VARCHAR(20),
    location VARCHAR(50),
    roi_percent DECIMAL(10,4),
    dsa_code VARCHAR(50),
    slab_type VARCHAR(30),
    base_percent DECIMAL(10,4),
    headline_percent DECIMAL(10,4),
    
    -- Commission Slabs (10 columns)
    slab_less_50L DECIMAL(10,4),
    slab_50L_1Cr DECIMAL(10,4),
    slab_1Cr_2Cr DECIMAL(10,4),
    slab_2Cr_3Cr DECIMAL(10,4),
    slab_3Cr_5Cr DECIMAL(10,4),
    slab_5Cr_10Cr DECIMAL(10,4),
    slab_10Cr_25Cr DECIMAL(10,4),
    slab_25Cr_50Cr DECIMAL(10,4),
    slab_50Cr_100Cr DECIMAL(10,4),
    slab_100Cr_plus DECIMAL(10,4),
    
    -- Qualifying Conditions
    qualifying_summary VARCHAR(20),
    pf_percent DECIMAL(10,4),
    i_percent DECIMAL(10,4),
    qualifying_notes TEXT,
    commercial_notes TEXT,
    post_disbursement_notes TEXT,
    
    -- Contest Fields
    contest_frequency VARCHAR(20),
    contest_target BIGINT,
    contest_bonus_percent DECIMAL(10,4),
    contest_period VARCHAR(50),
    contest_notes TEXT,
    
    -- Metadata
    file_period VARCHAR(20),
    schema_version VARCHAR(10),
    import_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 4. Critical Issues to Address

### 4.1 Data Consistency Issues

| Issue | Location | Severity |
|-------|----------|----------|
| Empty strings vs NA vs NULL | Multiple columns | Medium |
| Decimal rounding inconsistencies | Slab columns | Low |
| DSA Code formatting | Varies (quotes, spaces) | Medium |
| Qualifying conditions in notes | Qualifying Notes | High |
| ROI hidden in Commercial text | Commercial column | High |

### 4.2 Missing/Ambiguous Data

```
1. Row 33 (ICICI Bank BL): 
   - Base % = NA, Headline % = NA
   - All slabs = NA
   - But Commercial contains: "IRR < 16.5%: 100% PF + 0.50%"
   - This is business logic, not a commission rate

2. Row 68 (Standard Chartered):
   - Qualifying = PF (0.02)
   - Commercial: "Rate 15.50% & PF 2% maintained: +0.35%"
   - The 0.35% is a bonus, not in contest columns

3. Row 75 (Tata Capital OD):
   - PF % = 0.0175 (extracted from Commercial)
   - Multiple payout rates based on PF tiers
```

### 4.3 Edge Cases

| Row | Issue | Recommendation |
|-----|-------|----------------|
| 197 | Headline % = 3.3 (likely 0.033) | Need validation |
| 217 | ROI % = 0.1501 (15.01%) | Already extracted |
| 158 | Base % = 1.0 (100%) | Verify if intentional |
| 34 | Base % = 1.0 (100%) | Verify if intentional |

---

## 5. Import Recommendations

### 5.1 Pre-import Transformations

```python
# Recommended preprocessing steps
1. Standardize NA handling
   - Empty strings → NULL
   - "NA" → NULL
   - "" → NULL

2. Clean DSA Code
   - Remove single quotes: 'M1146 → M1146
   - Remove trailing spaces
   - Standardize separators

3. Decimal parsing
   - Ensure all percentages are stored as decimals (0.01 = 1%)
   - Handle "NA" gracefully
   - Validate range (0.0 to 1.0 for percentages)

4. Extract ROI from Commercial
   - Pattern: ROI X% / IRR X% / X% - Y%
   - Populate ROI % column where empty

5. Parse Qualifying Notes
   - Extract PF % and I % if missing
   - Flag qualitative conditions
```

### 5.2 Import Strategy

**Option 1: Direct Staging (Recommended)**
```
Stage → Validate → Transform → Import to production
```

**Option 2: Two-Phase Import**
```
Phase 1: Core columns (well-structured)
Phase 2: Extended columns (text-based)
```

### 5.3 Validation Rules

```sql
-- Validation checks
1. Base % NOT NULL OR Slab columns NOT NULL
2. Category IN ('BL', 'HL', 'LAP', 'PL')
3. Type IN ('Secured', 'Unsecured')
4. Slab columns >= 0 AND <= 1
5. DSA IN ('FCPL', 'BW')
6. ROI % >= 0 AND <= 1 (if present)
7. PF % >= 0 AND <= 1 (if present)
8. I % >= 0 AND <= 1 (if present)
```

---

## 6. Schema Design Recommendations

### 6.1 Normalized Schema Proposal

```
┌─────────────────────────────────────────────────────────────┐
│                         MAIN TABLE                          │
│  lender_payouts (core record)                               │
│  - id, dsa, lender, is_nbfc, type, category, sub_product   │
│  - channel, borrower, employer, salary, nature, location   │
│  - dsa_code, slab_type                                     │
│  - roi_percent, qualifying_summary, pf_percent, i_percent  │
│  - base_percent, headline_percent                          │
├─────────────────────────────────────────────────────────────┤
│                    COMMISSION SLABS                         │
│  commission_slabs (1:many)                                 │
│  - id, payout_id, tier_name, tier_min, tier_max, rate      │
├─────────────────────────────────────────────────────────────┤
│                    CONTEST DETAILS                          │
│  contest_details (1:1 optional)                            │
│  - id, payout_id, frequency, target, bonus, period, notes  │
├─────────────────────────────────────────────────────────────┤
│                    QUALIFYING NOTES                         │
│  qualifying_conditions (1:1 optional)                      │
│  - id, payout_id, pf_note, i_note, roi_note, commercial    │
│  - post_disbursement, qualifying_raw                       │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 Denormalized vs Normalized

| Approach | Pros | Cons |
|----------|------|------|
| **Denormalized** (as-is) | Simple import, easy query | Redundant data, wide table |
| **Normalized** (slabs separate) | Clean design, flexible | More complex import, joins needed |

---

## 7. Import Timeline

| Phase | Activity | Duration |
|-------|----------|----------|
| 1 | Data profiling & validation | 1 day |
| 2 | Preprocessing script development | 2 days |
| 3 | Staging table import | 1 day |
| 4 | Data validation & cleansing | 2 days |
| 5 | Production table transformation | 1 day |
| 6 | Testing & QA | 2 days |
| **Total** | | **~9 days** |

---

## 8. Risk Assessment

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Parsing errors in Commercial text | Medium | High | Build robust regex, manual review |
| Mixed decimal formats | Low | Medium | Pre-validation scripts |
| Missing values causing issues | Medium | High | Clear NULL handling, fallbacks |
| Schema changes in future versions | Medium | Medium | Version tracking, ETL flexibility |
| Contest data separation | Low | Medium | Separate table design |

---

## 9. Final Recommendation

### ✅ **GO for Import** with the following conditions:

1. **Staging-first approach** - Import to staging, validate, then migrate
2. **Preprocess before import** - Handle NA, formatting, and extractions
3. **Normalize commission slabs** - Consider 1:many relation for better data modeling
4. **Build validation rules** - Ensure data quality before production
5. **Track schema version** - V3.3 identified, monitor for future changes

### 🔧 **Immediate Actions**:

```sql
-- 1. Create staging schema
-- 2. Build import script with preprocessing
-- 3. Validate against business rules
-- 4. Create exception report
-- 5. Migrate to production
```

---

## 10. Key Takeaways

| Aspect | Status | Note |
|--------|--------|------|
| Data completeness | ⭐⭐⭐⭐ | 230 rows with 39 attributes |
| Data quality | ⭐⭐⭐ | Mixed - some columns need parsing |
| Schema design | ⭐⭐⭐⭐⭐ | Well-documented, versioned |
| Import complexity | ⭐⭐⭐ | Moderate - text parsing needed |
| Business value | ⭐⭐⭐⭐⭐ | High - comprehensive lender data |

**The data is import-ready with moderate preprocessing required, primarily around text extraction and data type standardization.**

---

# Comprehensive Data Assessment: Secured Tracker FY 26-27 (2).xlsx

## 1. EXECUTIVE SUMMARY

| Aspect | Assessment |
|--------|------------|
| **File Type** | Excel Workbook (.xlsx) |
| **Total Sheets** | 3 (Tracker, Mastersheet, Bank Account Master) |
| **Primary Purpose** | Loan case tracking, payout management, and commission reconciliation |
| **Data Volume** | ~384 rows of loan cases (Tracker) + reference data |
| **Data Quality** | Mixed - clean structured data with some inconsistencies |
| **Complexity** | High - multiple payee types, intricate formula chains, cross-sheet dependencies |

---

## 2. SHEET STRUCTURE OVERVIEW

### 2.1 Sheet: "Tracker" (Primary Data Sheet)
**Purpose**: Main transactional data for all loan cases

| Attribute | Details |
|-----------|---------|
| Row Count | ~384 active rows + summary rows |
| Column Count | 79 columns (A to CA) |
| Key Columns | A (SR NO), D (Case No), E (Enquiry No), T (Status), U (Total Disb Amount), Y (Bank Payout Amt), AA (Connector Payout Amt), AC (Connector 2 Payout Amt), etc. |

### 2.2 Sheet: "Mastersheet" (Reference Data)
**Purpose**: Lookup/reference data for validation

| Attribute | Details |
|-----------|---------|
| Key Columns | Bank Name, Payment Approval, Code, Entry by, Product, Case Status, Bill Status, Region |
| Data Type | Lookup/master data for dropdown validation |

### 2.3 Sheet: "Bank Account Master" (Vendor/Payee Master)
**Purpose**: Bank details for payees (Connectors, Unit Heads, SMs)

| Attribute | Details |
|-----------|---------|
| Key Fields | Connector Code, Connector Name, PAN, Bank, Account No, IFSC, Unit Head, GST |
| Data Source | Imports from Google Sheets (IMPORTRANGE functions) |
| **Critical Issue** | Contains #REF! errors - data source inaccessible |

---

## 3. ATTRIBUTE INVENTORY & CLASSIFICATION

### 3.1 Case Identification Attributes

| Column | Field Name | Data Type | Description | Import Priority |
|--------|------------|-----------|-------------|-----------------|
| A | SR NO | Integer (Formula) | Sequential case counter | System-generated |
| D | CASE NO | String | Unique case identifier (FY26-27/SC/XXXX) | **Primary Key** |
| E | ENQUIRY NO | String | Enquiry reference | High |
| F | APPLICATION NUMBER | String | Bank/application reference | High |
| B | ENTRY DATE | Date | Date of entry | High |
| C | ENTRY DONE BY | String | Person who entered data | Medium |

### 3.2 Party Information Attributes

| Column | Field Name | Data Type | Description | Import Priority |
|--------|------------|-----------|-------------|-----------------|
| G | COMPANY NAME | String | Company name (if corporate) | Medium |
| H | CUSTOMER NAME | String | Customer name | High |
| I | BANK NAME | String | Lending bank/financial institution | High |
| J | CODE | String | Branch/code identifier | Medium |
| K | BRANCH | String | Branch name | Medium |
| L | RM NAME | String | Relationship manager | Low |
| M | PRODUCT | String | Product type (LAP, HL, WC/OD, etc.) | High |
| N | CONNECTOR | String | Primary connector/agent | High |
| O | CONNECTOR 2 | String | Secondary connector | Medium |
| P | Referred by | String | Referral source | Low |
| Q | UNIT HEAD | String | Unit head name | Medium |
| R | SM NAME | String | Sales manager name | Medium |
| S | REGION | String | Geographic region | High |

### 3.3 Financial/Payout Attributes

| Column | Field Name | Data Type | Description | Import Priority |
|--------|------------|-----------|-------------|-----------------|
| T | STATUS | String (Dropdown) | DISBURSED/PART DISBURSED/CANCELLED/DUPLICATE/PENDING | High |
| U | TOTAL DISB AMOUNT | Numeric | Total disbursement amount | High |
| V | DISB DATE | Date | Disbursement date | High |
| W | PROFILE | String | Profile type (SENP, SALARIED, N/A) | Medium |
| X | BANK PAYOUT% | Numeric/Formula | Bank payout percentage | Medium |
| Y | BANK PAYOUTAMT | Numeric/Formula | Bank payout amount | High |
| Z | CONNECTOR PAYOUT% | Numeric/Formula | Connector-1 payout percentage | Medium |
| AA | CONNECTOR PAYOUT AMT | Numeric/Formula | Connector-1 payout amount | High |
| AB | CONNECTOR 2 PAYOUT% | Numeric/Formula | Connector-2 payout percentage | Medium |
| AC | CONNECTOR 2 PAYOUT AMT | Numeric/Formula | Connector-2 payout amount | High |
| AE | UNIT HEAD% | Numeric/Formula | Unit head payout percentage | Medium |
| AG | SM PAYOUT% | Numeric/Formula | Sales manager payout percentage | Medium |
| AI | Taxable Amount | Numeric | Taxable invoice amount | High |

### 3.4 Invoice & Payment Tracking Attributes

| Column | Field Name | Data Type | Description | Import Priority |
|--------|------------|-----------|-------------|-----------------|
| AJ | INVOICE DATE | Date | Invoice generation date | High |
| AK | INVOICE NO | String/Number | Invoice reference number | High |
| AL | Bill Status | String | RECEIVED/PENDING/RAISED/DUPLICATE/CANCELLED | High |
| AM | Receive date | Date | Date payment received | Medium |
| AN | Case wise P&L | Numeric (Formula) | Profit/Loss calculation per case | High |
| AO | Payout % | Numeric/Formula | Total payout percentage | Medium |

### 3.5 Connector-1 Payment Details

| Column | Field Name | Data Type | Description |
|--------|------------|-----------|-------------|
| AV | Advance/Recovery | Numeric | Adjustment for advance/recovery |
| AW | PAYMENT AMT | Numeric (Formula) | Net payable amount |
| AX | TDS@2% | Numeric (Formula) | TDS deduction at 2% |
| AY | FINAL PAYABLE AMT | Numeric (Formula) | Final amount after TDS |
| AZ | Connector Name -1 | String (VLOOKUP) | Connector-1 name |
| BA | C-1 UTR | String | UTR number for payment |

### 3.6 Connector-2 Payment Details

| Column | Field Name | Data Type | Description |
|--------|------------|-----------|-------------|
| BD | Connector 2 PAYMENT DATE | Date | Payment date for connector-2 |
| BF | Connector 2 PAYMENT AMT | Numeric | Amount for connector-2 |
| BG | Connector 2 TDS@2% | Numeric (Formula) | TDS at 2% on connector-2 |
| BH | Connector 2 FINAL PAYABLE AMT | Numeric (Formula) | Final amount for connector-2 |
| BI | Connector 2 Name | String | Secondary connector name |

### 3.7 Unit Head & Sales Manager Payment Details

| Column | Field Name | Data Type | Description |
|--------|------------|-----------|-------------|
| BO | PAID TO UNIT HEAD | String | Unit head payment status |
| BP | Payee Name (UH) | String | Payee name from Bank Account Master |
| BR | PAYMENT AMT | Numeric | Unit head payment amount |
| BS | TDS@2% | Numeric (Formula) | TDS on unit head payment |
| BT | FINAL PAYABLE AMT | Numeric (Formula) | Final unit head amount |
| BU | PAID TO SM | String | SM payment status |
| BX | PAYMENT AMT | Numeric | SM payment amount |
| BY | TDS@2% | Numeric (Formula) | TDS on SM payment |
| BZ | FINAL PAYABLE AMT | Numeric (Formula) | Final SM amount |

### 3.8 Approval & Process Tracking

| Column | Field Name | Data Type | Description |
|--------|------------|-----------|-------------|
| AP | Remarks | String | Free text notes/remarks |
| AQ | Payment Approval | String (YES/NO) | Approval status |
| AR | Approval Date 1 | Date | First approval date |
| AS | Approval Date 2 | Date | Second approval date |
| AT | Payment Request Date C-1 | Date | Payment request date for connector-1 |
| AU | Percentage Formula | String | Formula reference |

---

## 4. DATA CHARACTERISTICS ANALYSIS

### 4.1 Data Types Found

| Data Type | Examples | Frequency |
|-----------|----------|-----------|
| **String/Text** | Case IDs, Names, Bank Names, Status | ~60% of columns |
| **Numeric** | Amounts, Percentages, Counts | ~25% of columns |
| **Date** | Disbursement, Invoice, Payment dates | ~10% of columns |
| **Formula** | Calculations, VLOOKUPs, Conditional logic | ~5% of columns |
| **Boolean** | YES/NO, PAID TO flags | ~5% of columns |

### 4.2 Key Relationships & Dependencies

```
┌─────────────────────────────────────────────────────────────┐
│                      TRACKER (Main)                        │
├─────────────────────────────────────────────────────────────┤
│  Case ID ──────────────────────────────────────────────┐   │
│  Invoice # ───────────────────────────────────────┐    │   │
│  Connector Name ───┐                            │    │   │
│  Connector 2 Name ──┼── VLOOKUP ────────────────┼────┼───┤
│  Unit Head ─────────┤                            │    │   │
│  SM Name ───────────┤                            │    │   │
└─────────────────────┼────────────────────────────┼────┼───┘
                      │                            │    │
                      ▼                            ▼    ▼
┌─────────────────────────────────────────────────────────────┐
│                 BANK ACCOUNT MASTER                        │
├─────────────────────────────────────────────────────────────┤
│  Connector Name ──► Connector PAN                         │
│                   ──► Bank                                │
│                   ──► Account No                         │
│                   ──► IFSC                               │
│                   ──► Unit Head                          │
│                   ──► GST                                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   MASTERSHEET                              │
├─────────────────────────────────────────────────────────────┤
│  Bank Name ──► Lookup for validation                      │
│  Status ─────► Lookup for dropdown                        │
│  Region ─────► Lookup for geographic mapping              │
│  Product ────► Lookup for product classification          │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 Formula Patterns

| Column | Formula Pattern | Purpose |
|--------|-----------------|---------|
| **Row Numbers** | `=ROW()-ROW($A$1)` | Auto-generate sequential numbers |
| **Bank Payout** | `=Y4/U4` | % of disbursement amount |
| **TDS Calculation** | `=round(AW4*2%,)` | TDS at 2% on payment |
| **Final Payable** | `=AW4-AX4` | Net amount after TDS |
| **Summary** | `=SUBTOTAL(9,U4:U5522)` | Sum of filtered values |
| **VLOOKUP** | `=VLOOKUP(AZ4,'Bank Account Master'!B:F,3,0)` | Fetch bank details |

---

## 5. DATA QUALITY ASSESSMENT

### 5.1 Identified Issues

| Issue Type | Severity | Location | Description |
|------------|----------|----------|-------------|
| **#REF! Errors** | High | Rows 14, 290, 357, 383-5000+ | VLOOKUP references to missing data |
| **#N/A Errors** | Medium | Row 357 | VLOOKUP reference not found |
| **Mixed Date Formats** | Medium | Various | DD-MM-YYYY vs DD/MM/YYYY formats |
| **Inconsistent Naming** | Low | Various | "N/A" vs blank vs NULL values |
| **Zero Amount Cases** | Medium | Rows with `*0` in formulas | Disbursements set to zero intentionally |
| **Duplicate Entries** | Medium | SE/26-27/0015, 0080, 0090, etc. | Multiple entries for same case |
| **Incomplete Data** | High | Rows 383-1000+ | Empty template rows with formulas |
| **Cross-Sheet Dependency** | High | Bank Account Master | Relies on external Google Sheets |

### 5.2 Data Completeness (Sample of 40 rows)

| Category | Complete | Partial | Empty |
|----------|----------|---------|-------|
| Case IDs (D,E) | 95% | 5% | 0% |
| Customer/Borrower | 85% | 10% | 5% |
| Bank Details | 90% | 5% | 5% |
| Financial Data | 80% | 15% | 5% |
| Payment Status | 75% | 15% | 10% |
| Connector Details | 70% | 20% | 10% |

---

## 6. DATABASE IMPORT RECOMMENDATIONS

### 6.1 Recommended Table Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                         SCHEMA DESIGN                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. loan_cases (Primary Table)                                 │
│     ├── case_id (PK) - VARCHAR(20)                             │
│     ├── enquiry_no - VARCHAR(20)                              │
│     ├── application_no - VARCHAR(50)                          │
│     ├── entry_date - DATE                                     │
│     ├── entry_by - VARCHAR(50)                                │
│     ├── company_name - VARCHAR(200)                           │
│     ├── customer_name - VARCHAR(200)                          │
│     ├── bank_id (FK) - INT                                    │
│     ├── branch - VARCHAR(100)                                 │
│     ├── rm_name - VARCHAR(100)                                │
│     ├── product_id (FK) - INT                                 │
│     ├── status_id (FK) - INT                                  │
│     ├── total_disb_amount - DECIMAL(18,2)                    │
│     ├── disb_date - DATE                                     │
│     ├── profile - VARCHAR(50)                                 │
│     ├── taxable_amount - DECIMAL(18,2)                       │
│     ├── invoice_date - DATE                                  │
│     ├── invoice_no - VARCHAR(50)                             │
│     ├── bill_status_id (FK) - INT                            │
│     ├── receive_date - DATE                                  │
│     ├── payout_percentage - DECIMAL(10,4)                    │
│     ├── remarks - TEXT                                       │
│     ├── payment_approval - BOOLEAN                           │
│     ├── approval_date_1 - DATE                               │
│     ├── approval_date_2 - DATE                               │
│     └── region_id (FK) - INT                                 │
│                                                                 │
│  2. payouts (Child Table - One-to-Many)                         │
│     ├── payout_id (PK) - INT                                   │
│     ├── case_id (FK) - VARCHAR(20)                             │
│     ├── payee_type - ENUM('BANK','CONNECTOR_1','CONNECTOR_2',  │
│     │                    'UNIT_HEAD','SM')                      │
│     ├── payee_name - VARCHAR(200)                              │
│     ├── payout_percentage - DECIMAL(10,4)                      │
│     ├── payout_amount - DECIMAL(18,2)                          │
│     ├── tds_amount - DECIMAL(18,2)                            │
│     ├── net_amount - DECIMAL(18,2)                            │
│     ├── payment_date - DATE                                    │
│     ├── utr_number - VARCHAR(50)                              │
│     ├── request_date - DATE                                    │
│     └── advance_recovery - DECIMAL(18,2)                       │
│                                                                 │
│  3. banks (Lookup Table)                                       │
│     ├── bank_id (PK) - INT                                     │
│     ├── bank_name - VARCHAR(100)                               │
│     ├── bank_code - VARCHAR(20)                                │
│     └── is_active - BOOLEAN                                    │
│                                                                 │
│  4. connectors (Lookup Table)                                  │
│     ├── connector_id (PK) - INT                                │
│     ├── connector_code - VARCHAR(20)                           │
│     ├── connector_name - VARCHAR(200)                          │
│     ├── pan - VARCHAR(10)                                      │
│     ├── bank_name - VARCHAR(100)                              │
│     ├── account_no - VARCHAR(50)                              │
│     ├── ifsc_code - VARCHAR(20)                               │
│     ├── unit_head - VARCHAR(200)                              │
│     ├── gst - VARCHAR(20)                                     │
│     └── is_active - BOOLEAN                                    │
│                                                                 │
│  5. products (Lookup Table)                                    │
│     ├── product_id (PK) - INT                                  │
│     ├── product_name - VARCHAR(50)                             │
│     └── product_code - VARCHAR(20)                             │
│                                                                 │
│  6. statuses (Lookup Table)                                    │
│     ├── status_id (PK) - INT                                   │
│     ├── status_name - VARCHAR(50)                              │
│     └── status_type - VARCHAR(20)                              │
│                                                                 │
│  7. regions (Lookup Table)                                     │
│     ├── region_id (PK) - INT                                   │
│     ├── region_name - VARCHAR(100)                             │
│     └── city - VARCHAR(100)                                    │
│                                                                 │
│  8. approvals (Audit/Process Table)                            │
│     ├── approval_id (PK) - INT                                 │
│     ├── case_id (FK) - VARCHAR(20)                             │
│     ├── approval_stage - INT                                   │
│     ├── approval_date - DATE                                   │
│     ├── approved_by - VARCHAR(100)                            │
│     └── status - VARCHAR(20)                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 Data Migration Mapping

| Excel Column | Target Field | Transformation Required |
|--------------|--------------|------------------------|
| D (CASE NO) | loan_cases.case_id | String cleanup |
| E (ENQUIRY NO) | loan_cases.enquiry_no | Direct mapping |
| F (APPLICATION NUMBER) | loan_cases.application_no | Direct mapping |
| B (ENTRY DATE) | loan_cases.entry_date | Date parse (DD-MM-YYYY) |
| C (ENTRY DONE BY) | loan_cases.entry_by | Direct mapping |
| G (COMPANY NAME) | loan_cases.company_name | Handle empty as NULL |
| H (CUSTOMER NAME) | loan_cases.customer_name | Direct mapping |
| I (BANK NAME) | banks.bank_name | Lookup/match |
| M (PRODUCT) | products.product_name | Lookup/match |
| T (STATUS) | statuses.status_name | Lookup/match |
| U (TOTAL DISB AMOUNT) | loan_cases.total_disb_amount | Convert to number |
| V (DISB DATE) | loan_cases.disb_date | Date parse |
| AJ (INVOICE DATE) | loan_cases.invoice_date | Date parse |
| AK (INVOICE NO) | loan_cases.invoice_no | Direct mapping |
| AL (Bill Status) | loan_cases.bill_status | Lookup/match |
| AM (Receive date) | loan_cases.receive_date | Date parse |
| AP (Remarks) | loan_cases.remarks | Direct mapping |
| AQ (Payment Approval) | loan_cases.payment_approval | YES/NO → BOOLEAN |
| AR/AS (Approval Dates) | approvals.approval_date | Split into rows |

### 6.3 Payout Mapping

| Excel Field | Payee Type | Target Table |
|-------------|------------|--------------|
| Y (BANK PAYOUTAMT) | BANK | payouts |
| AA (CONNECTOR PAYOUT AMT) | CONNECTOR_1 | payouts |
| AC (CONNECTOR 2 PAYOUT AMT) | CONNECTOR_2 | payouts |
| AE (UNIT HEAD AMT) | UNIT_HEAD | payouts |
| AG (SM PAYOUT AMT) | SM | payouts |
| BA (C-1 UTR) | CONNECTOR_1 | payouts.utr_number |

---

## 7. IMPORT CHALLENGES & SOLUTIONS

### 7.1 Primary Challenges

| Challenge | Impact | Solution |
|-----------|--------|----------|
| **#REF! Errors in Bank Account Master** | High - Cannot resolve payee details | Clean or re-establish Google Sheets connection; Fallback to manual data entry |
| **Formula Dependencies** | Medium - Calculated fields need transformation | Implement business logic in ETL/DB layer |
| **Duplicate Case IDs** | Medium - Multiple entries for same case (e.g., SE/26-27/0015, 0015A, 0015B) | Use composite key or versioning; Consolidate or track as separate disbursements |
| **Incomplete Template Rows** | Low - Rows 383+ are empty | Filter out rows with NULL case_id or zero disbursement |
| **Mixed Date Formats** | Low - Parsing variations | Standardize to YYYY-MM-DD during ETL |
| **External Data Source** | High - Bank Account Master imports from Google Sheets | Export static copy; Schedule periodic refresh |

### 7.2 Recommended ETL Process

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Excel     │───▶│   Clean     │───▶│  Transform  │
│   Source    │    │   Extract   │    │   & Map     │
└─────────────┘    └─────────────┘    └─────────────┘
                                             │
                                             ▼
                                    ┌─────────────────┐
                                    │   Data Quality  │
                                    │    Checks       │
                                    └─────────────────┘
                                             │
                                             ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Validate  │◀───│   Load to   │◀───│   Stage     │
│   & Verify  │    │   Database  │    │   Tables    │
└─────────────┘    └─────────────┘    └─────────────┘
```

---

## 8. RECOMMENDED DATA CLEANING STEPS

### 8.1 Pre-Import Data Cleansing

| Step | Action | Priority |
|------|--------|----------|
| 1 | Replace #REF! and #N/A with NULL/empty values | High |
| 2 | Standardize date formats to ISO (YYYY-MM-DD) | High |
| 3 | Trim whitespace from all text fields | Medium |
| 4 | Convert YES/NO to BOOLEAN (1/0) | Medium |
| 5 | Normalize "N/A" and empty strings to NULL | Medium |
| 6 | Remove rows with empty case_id | Low |
| 7 | Separate multi-part cases (A, B, C suffixes) | Low |
| 8 | Validate bank names against master list | Medium |
| 9 | Normalize product names to standard values | Medium |
| 10 | Create static copy of Bank Account Master | High |

### 8.2 Data Validation Rules

```sql
-- Example validation rules
1. case_id_format: ~/^FY\d{2}-\d{2}/SC/\d{4}$/
2. amount_positive: total_disb_amount >= 0
3. date_order: disb_date <= invoice_date <= receive_date
4. payout_sum: SUM(payouts) <= total_disb_amount * 0.10 (approx)
5. status_valid: IN ('DISBURSED', 'PART DISBURSED', 'CANCELLED', 'DUPLICATE', 'PENDING')
```

---

## 9. INDEX RECOMMENDATIONS

```sql
-- For optimal query performance
CREATE INDEX idx_case_id ON loan_cases(case_id);
CREATE INDEX idx_enquiry_no ON loan_cases(enquiry_no);
CREATE INDEX idx_bank_id ON loan_cases(bank_id);
CREATE INDEX idx_region_id ON loan_cases(region_id);
CREATE INDEX idx_status_id ON loan_cases(status_id);
CREATE INDEX idx_disb_date ON loan_cases(disb_date);
CREATE INDEX idx_invoice_date ON loan_cases(invoice_date);
CREATE INDEX idx_payout_case ON payouts(case_id);
CREATE INDEX idx_payout_type ON payouts(payee_type);
CREATE INDEX idx_connector_name ON connectors(connector_name);
CREATE INDEX idx_bank_name ON banks(bank_name);
```

---

## 10. UNIQUE IDENTIFIERS

| Key Type | Columns | Usage |
|----------|---------|-------|
| **Primary Key** | CASE NO | Unique case identifier in the system |
| **Composite Key** | CASE NO + VERSION (A/B/C suffix) | Handle duplicate case entries |
| **Natural Key** | INVOICE NO | Unique invoice per case |
| **Foreign Key** | Bank Name → Banks table | For normalization |
| **Foreign Key** | Product → Products table | Product categorization |
| **Foreign Key** | Connector Name → Connectors table | Payee master linkage |

---

## 11. SUMMARY STATISTICS

| Metric | Value |
|--------|-------|
| **Total Cases** | ~370 |
| **Unique Banks** | ~50+ |
| **Unique Connectors** | ~75+ |
| **Unique Products** | ~15 |
| **Unique Regions** | ~20 |
| **Date Range** | April 2026 - July 2026 |
| **Total Disbursements** | ~₹50-60 Cr (estimated) |

---

## 12. NEXT STEPS CHECKLIST

- [ ] Fix #REF! errors in Bank Account Master sheet
- [ ] Export/convert formulas to static values where needed
- [ ] Create backup of current workbook
- [ ] Develop ETL scripts for data extraction
- [ ] Build staging tables matching recommended schema
- [ ] Implement data validation rules
- [ ] Test import with a sample subset (20 rows)
- [ ] Verify data integrity after import
- [ ] Create reconciliation reports
- [ ] Document import process for repeat use

---

## 13. RECOMMENDATION FOR UNECURED FILE

Based on the structure of this secured loan file, the **unsecured loans file** should follow an identical structure with:

| Modification | Purpose |
|--------------|---------|
| Different Sheet Name | Distinguish between secured/unsecured |
| Additional Product Types | Include unsecured products (Personal Loan, Business Loan, etc.) |
| Different Bank/Payout Rates | Reflect unsecured lending rates |
| Additional Fields | Include credit score, income proof flags, etc. |

**Suggested filename:** `Unsecured Tracker FY 26-27.xlsx`

---

*Assessment prepared by Data Migration Team | Date: [Current Date]*

---
