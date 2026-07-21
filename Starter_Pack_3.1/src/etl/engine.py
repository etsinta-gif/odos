# src/etl/engine.py
from typing import Dict, Any, List
from src.etl.services.excel_extractor import extract_excel
from src.etl.services.csv_extractor import extract_csv
from src.etl.services.api_extractor import extract_api
from src.etl.models import ETL_ImportBatch, ETL_StagingRawData
from src.core.database import SessionLocal

class ETLPipeline:
    def __init__(self, batch_id: str, company_id: int):
        self.batch_id = batch_id
        self.company_id = company_id
        self.db = SessionLocal()

    def extract(self, source_type: str, source_path: str, **kwargs) -> List[Dict[str, Any]]:
        """Extract data from source and return list of rows."""
        if source_type == "excel":
            return extract_excel(source_path, **kwargs)
        elif source_type == "csv":
            return extract_csv(source_path, **kwargs)
        elif source_type == "api":
            return extract_api(source_path, **kwargs)
        else:
            raise ValueError(f"Unsupported source type: {source_type}")

    def load_staging(self, rows: List[Dict[str, Any]], target_table: str):
        """Store extracted rows into staging table."""
        # We will implement this in later sprints (3.4)
        pass

    def close(self):
        self.db.close()
