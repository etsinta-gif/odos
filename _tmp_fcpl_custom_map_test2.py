from pathlib import Path
import pandas as pd
from fastapi.testclient import TestClient

from app.main import app
from scripts.validate_staging import validate_staging
from src.core.database import SessionLocal
from src.transactions.models import ETL_StagingRawData, ETL_ErrorLog

src = Path('samples/FCPL_Lender_Payout_N_Master.xlsx')
b = src.read_bytes()
client = TestClient(app)

# dynamic columns (avoid unicode literal issues)
df = pd.read_excel(src, sheet_name='Master', header=0)
cols = [str(c) for c in df.columns]
slab_cols = [c for c in cols if ('?' in c) or ('<' in c and 'L' in c) or ('Cr' in c)]

an = client.post('/api/admin/mapping/analyze', files={'file': (src.name, b, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}, data={'header_row':'1'})
fp = an.json().get('workbook_fingerprint')
print('FINGERPRINT', fp)

mappings = [
    {'source_column':'DSA','target_table':'MST_Company','target_field':'company_code','confidence_score':90,'is_verified':True,'is_natural_key':False},
    {'source_column':'Lender / NBFC','target_table':'MST_Lender','target_field':'lender_name','confidence_score':95,'is_verified':True,'is_natural_key':False},
    {'source_column':'NBFC?','target_table':'MST_Lender','target_field':'is_nbfc','confidence_score':95,'is_verified':True,'is_natural_key':False},
    {'source_column':'Type','target_table':'REF_LoanType','target_field':'type_code','confidence_score':85,'is_verified':True,'is_natural_key':False},
    {'source_column':'Category','target_table':'REF_ProductCategory','target_field':'category_code','confidence_score':85,'is_verified':True,'is_natural_key':False},
    {'source_column':'Sub-product','target_table':'MST_Product','target_field':'sub_product','confidence_score':80,'is_verified':True,'is_natural_key':False},
    {'source_column':'Channel','target_table':'REF_Channel','target_field':'channel_code','confidence_score':75,'is_verified':True,'is_natural_key':False},
    {'source_column':'Borrower','target_table':'REF_BorrowerProfile','target_field':'profile_code','confidence_score':75,'is_verified':True,'is_natural_key':False},
    {'source_column':'Nature','target_table':'REF_LoanNature','target_field':'nature_code','confidence_score':75,'is_verified':True,'is_natural_key':False},
    {'source_column':'Location','target_table':'REF_Location','target_field':'location_code','confidence_score':75,'is_verified':True,'is_natural_key':False},
    {'source_column':'ROI %','target_table':'MST_Product','target_field':'roi_percent','confidence_score':80,'is_verified':True,'is_natural_key':False},
    {'source_column':'DSA Code','target_table':'MST_Lender','target_field':'dsa_code','confidence_score':70,'is_verified':True,'is_natural_key':False},
    {'source_column':'Slab Type','target_table':'RUL_CommissionRule','target_field':'slab_type','confidence_score':90,'is_verified':True,'is_natural_key':False},
    {'source_column':'Base %','target_table':'RUL_CommissionRule','target_field':'base_percent','confidence_score':90,'is_verified':True,'is_natural_key':False},
    {'source_column':'Headline %','target_table':'RUL_CommissionRule','target_field':'headline_percent','confidence_score':90,'is_verified':True,'is_natural_key':False},
    {'source_column':'Qualifying','target_table':'RUL_CommissionRule','target_field':'qualifying_condition','confidence_score':80,'is_verified':True,'is_natural_key':False},
    {'source_column':'PF %','target_table':'RUL_CommissionRule','target_field':'pf_percent','confidence_score':85,'is_verified':True,'is_natural_key':False},
    {'source_column':'I %','target_table':'RUL_CommissionRule','target_field':'i_percent','confidence_score':85,'is_verified':True,'is_natural_key':False},
    {'source_column':'Qualifying Notes','target_table':'RUL_CommissionRule','target_field':'qualifying_notes','confidence_score':80,'is_verified':True,'is_natural_key':False},
    {'source_column':'Commercial','target_table':'RUL_CommissionRule','target_field':'commercial_terms','confidence_score':80,'is_verified':True,'is_natural_key':False},
    {'source_column':'Post-disbursement clawback conditions','target_table':'RUL_CommissionRule','target_field':'clawback_conditions','confidence_score':75,'is_verified':True,'is_natural_key':False},
]

for c in slab_cols:
    mappings.append({'source_column':c,'target_table':'RUL_CommissionSlab','target_field':'rate','confidence_score':90,'is_verified':True,'is_natural_key':False})

payload = {
    'template_name': 'Pilot FCPL Lender Payout Master v2',
    'file_pattern': '.*FCPL_Lender_Payout_N_Master.xlsx.*',
    'fingerprint': fp,
    'sheet_name': 'Master',
    'header_row': 1,
    'conflict_resolution': 'UPDATE',
    'mappings': mappings,
    'status': 'Draft'
}

c = client.post('/api/admin/mapping/confirm', json=payload)
print('CONFIRM', c.status_code, c.text[:200])
if c.status_code != 200:
    raise SystemExit(0)
tid = c.json().get('template_id')
print('TEMPLATE_ID', tid)
print('APPROVE', client.put(f'/api/admin/mapping/templates/{tid}', json={'status':'Approved'}).status_code)
print('ACTIVATE', client.put(f'/api/admin/mapping/templates/{tid}', json={'status':'Active'}).status_code)

u = client.post('/api/v1/etl/upload', files={'file': (src.name, b, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}, data={'entity_type':'MST_Lender','company_id':'1'})
print('UPLOAD', u.status_code)
print('UPLOAD_JSON', u.json() if u.headers.get('content-type','').startswith('application/json') else u.text[:300])
if u.status_code != 200:
    raise SystemExit(0)
batch = u.json()['batch_guid']
print('BATCH', batch)

with SessionLocal() as db:
    rows = db.query(ETL_StagingRawData).filter(ETL_StagingRawData.batch_guid==batch).all()
    counts = {}
    for r in rows:
        counts[r.table_name] = counts.get(r.table_name, 0) + 1
    print('STAGING_COUNTS', counts)
    # sample lender staged row
    lender = [r for r in rows if r.table_name=='MST_Lender']
    if lender:
        print('LENDER_ROW_SAMPLE', lender[0].stored_value[:500])

validate_staging(batch)
p = client.post('/api/v1/etl/promote', data={'batch_guid':batch,'conflict_resolution':'UPDATE'})
print('PROMOTE', p.status_code, p.text[:400])

with SessionLocal() as db:
    errs = db.query(ETL_ErrorLog).filter(ETL_ErrorLog.batch_guid==batch).all()
    print('ERROR_COUNT', len(errs))
    for e in errs[:20]:
        print('ERR', e.error_type, e.table_name, e.error_message)
