import argparse
import json
import os
import sys
from datetime import datetime

import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import SessionLocal
from src.rules.api.rules import RuleExecutionRequest, execute_validation_rules
from src.transactions.models import ETL_ErrorLog, ETL_StagingRawData


def validate_staging(batch_guid: str | None = None) -> None:
    db = SessionLocal()
    try:
        query = db.query(ETL_StagingRawData).filter(ETL_StagingRawData.validation_status == "PENDING")
        if batch_guid:
            query = query.filter(ETL_StagingRawData.batch_guid == batch_guid)

        staged = query.all()
        if not staged:
            print("No pending staging records found.")
            return

        warnings = 0
        critical = 0
        passed = 0
        for rec in staged:
            try:
                data = json.loads(rec.stored_value or "{}")
            except Exception:
                data = {}

            if not data:
                critical += 1
                rec.validation_status = "FAILED"
                db.add(
                    ETL_ErrorLog(
                        batch_guid=rec.batch_guid,
                        company_id=rec.company_id,
                        table_name=rec.table_name,
                        row_number=rec.source_row_number,
                        column_name=rec.column_name,
                        error_type="VALIDATION",
                        error_message="Empty or invalid row data",
                        error_datetime=datetime.utcnow(),
                    )
                )
                continue

            api_base = os.getenv("API_BASE", "http://localhost:8000")
            result_obj = None
            try:
                response = requests.post(
                    f"{api_base}/api/v1/rules/execute",
                    json={"table_name": rec.table_name, "row_data": data, "rule_ids": []},
                    timeout=5,
                )
                if response.status_code == 200:
                    result_obj = response.json()
            except Exception:
                result_obj = None

            if result_obj is None:
                fallback = execute_validation_rules(
                    RuleExecutionRequest(table_name=rec.table_name, row_data=data, rule_ids=[]),
                    db,
                )
                result_obj = {
                    "passed": fallback.passed,
                    "errors": fallback.errors,
                    "warnings": fallback.warnings,
                }

            if result_obj.get("passed"):
                rec.validation_status = "PASSED"
                passed += 1
            else:
                critical += len(result_obj.get("errors", []))
                rec.validation_status = "FAILED"
                for err in result_obj.get("errors", []):
                    db.add(
                        ETL_ErrorLog(
                            batch_guid=rec.batch_guid,
                            company_id=rec.company_id,
                            table_name=rec.table_name,
                            row_number=rec.source_row_number,
                            column_name=rec.column_name,
                            error_type="VALIDATION",
                            error_message=err,
                            error_datetime=datetime.utcnow(),
                        )
                    )

            for warn in result_obj.get("warnings", []):
                warnings += 1
                db.add(
                    ETL_ErrorLog(
                        batch_guid=rec.batch_guid,
                        company_id=rec.company_id,
                        table_name=rec.table_name,
                        row_number=rec.source_row_number,
                        column_name=rec.column_name,
                        error_type="WARNING",
                        error_message=warn,
                        error_datetime=datetime.utcnow(),
                    )
                )

        db.commit()
        print(f"Validation complete. passed={passed}, warnings={warnings}, critical_errors={critical}")
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate ETL staging records")
    parser.add_argument("--batch-guid", dest="batch_guid", default=None)
    args = parser.parse_args()
    validate_staging(batch_guid=args.batch_guid)