from src.transactions.models import ETL_DataLineage


def test_lineage_model_has_company_id_column():
    assert hasattr(ETL_DataLineage, "company_id")
