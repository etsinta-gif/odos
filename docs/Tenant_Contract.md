# ODOS Tenant Contract - What a DSA Owns

## Owner (Tenant-Scoped) Tables

These tables contain data that belongs exclusively to one DSA. All queries must filter by `company_id`.

### Masters
- `mst_dsa` (tenant anchor)
- `mst_customer`
- `mst_lender`
- `mst_product`
- `mst_employee`
- `mst_connector`
- `mst_vendor`
- `mst_expense_category`
- `mst_cost_center`
- `mst_company_bank_account`

### Transactions
- `trn_case`
- `trn_revenue`
- `trn_commission`
- `trn_expense`
- `trn_payment`
- `trn_recurring_expense`
- `trn_expense_claim`

### Rules
- `rul_validation_rule`
- `rul_commission_rule`
- `rul_commission_slab`
- `rul_gst_rule`
- `rul_tds_rule`

### ETL
- `etl_import_batch`
- `etl_staging_raw_data`
- `etl_error_log`
- `etl_data_lineage`

### Security
- `sec_users`
- `sec_login_history`

---

## Shared (Global) Tables

These tables are shared across all DSAs and should not be tenant-owned business records.

### Reference Data
- `ref_loan_type`
- `ref_channel`
- `ref_product_category`
- `ref_status`
- `ref_region`
- `ref_borrower_profile`
- `ref_loan_nature`
- `ref_location`

### Metadata
- `meta_table_definition`
- `meta_field_definition`
- `meta_import_template` (if `shared = True`)
- `meta_field_mapping` (if `shared = True`)

### Security (System)
- `sec_roles`
- `sec_permissions`
- `user_roles`
- `role_permissions`

### AI
- `ai_metadata`
- `ai_mapping` (if `shared = True`)

---

## Data Isolation Rules

1. All tenant-scoped tables MUST have `company_id`.
2. All tenant-scoped queries MUST filter by `company_id`.
3. Shared tables MUST NOT store tenant-owned business records.
4. Cross-tenant reads and writes are prohibited.
5. Templates can be shared (`shared = True`) or tenant-specific (`shared = False`).
