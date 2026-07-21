# FCPL Lender Payout Master - Execution Diagnosis

Date: 2026-07-20
Input file tested: C:/Users/etsin/OneDrive/Documents/FCPL Lender Payout N Master.xlsx
Workspace test copy: samples/FCPL_Lender_Payout_N_Master.xlsx
Sheet used: Master

## 1. What Was Executed
1. Verified file path exists and copied into workspace sample path.
2. Ran analyzer on Master sheet.
3. Created template from provided mapping intent and activated it.
4. Uploaded file through ETL.
5. Promoted batch after hardening fix.

## 2. Observed Test Facts
- Sheet list: Master
- Actual columns detected: 39 (not 41 in this workbook copy)
- Analyzer auto-proposal:
  - mapped: 19
  - ignored: 20
- Custom template created from your mapping:
  - template_id: 16
  - mapping rows stored: 32
  - target table distribution:
    - MST_Company: 1
    - MST_Lender: 3
    - REF_LoanType: 1
    - REF_ProductCategory: 1
    - MST_Product: 2
    - REF_Channel: 1
    - REF_BorrowerProfile: 1
    - REF_LoanNature: 1
    - REF_Location: 1
    - RUL_CommissionRule: 9
    - RUL_CommissionSlab: 11
- Upload run with entity_type=MST_Lender:
  - batch_guid: 4c650df8-7168-4d21-abb8-d1f9e26b916a
  - staged_rows: 270
  - deduplicated_rows: 2423
  - staged table counts:
    - MST_Lender: 137
    - RUL_CommissionSlab: 133

## 3. Why Expected Outcome Was Not Achieved

### Root Cause A: Single-entity upload path
Current ETL upload stages only:
- the entity table chosen in upload request, and
- slab rows when RUL_CommissionSlab mappings exist.

So with entity_type=MST_Lender, mappings for MST_Product, RUL_CommissionRule, MST_Company, and REF_* are not staged in this flow.

Code evidence:
- single target table mapping path: src/masters/api/etl.py#L124
- entity table derived from request: src/masters/api/etl.py#L366
- only slab has special additional staging path: src/masters/api/etl.py#L408

### Root Cause B: Mapping references tables not present in current runtime schema
Your mapping includes MST_Company and several REF_* tables. These models are not present in the current runtime src models, so even with multi-entity staging they cannot be promoted yet without schema/model additions.

Code evidence:
- runtime master models currently available: src/masters/models.py
- rules model has RUL_CommissionRule, but promote path currently handles only MST_Connector/MST_Lender/TRN_Case/RUL_CommissionSlab: src/masters/api/etl.py#L629

### Root Cause C: Slab promotion failure with NaN values (fixed now)
During promotion, NaN slab rates caused NOT NULL constraint failures on rul_commission_slab.rate.
I applied a fix so non-finite values are treated as invalid and skipped.

Code fix applied:
- numeric hardening in float parser: src/masters/api/etl.py#L109
- skip non-finite slab rates: src/masters/api/etl.py#L172

Post-fix verification:
- promotion succeeded for batch 4c650df8-7168-4d21-abb8-d1f9e26b916a
- API result: promoted_count=270, failed=0

## 4. Current Status After Fix
- Pipeline stability: improved (no slab NaN crash)
- Your full cross-table mapping target: still not fully achievable in one run with current ETL architecture and current schema coverage.

## 5. What To Change To Reach Your Target Behavior
P0:
1. Add multi-target staging in upload:
   - stage rows per target_table present in template mappings (not only entity_type table + slabs).
2. Extend promote path for RUL_CommissionRule and MST_Product at minimum.
3. Decide policy for MST_Company and REF_*:
   - either add models/tables,
   - or map these fields temporarily into supported tables/metadata structure.

P1:
4. Add validation guards for required mapped fields (for example lender_name, slab_type, base/headline percentages where needed).
5. Add explicit ignored-column audit logging per batch.

## 6. Validation Data For You
- Template used: 16
- Batch used: 4c650df8-7168-4d21-abb8-d1f9e26b916a
- You can verify current promotion completion from ETL_ImportBatch and staged table distribution from ETL_StagingRawData.
