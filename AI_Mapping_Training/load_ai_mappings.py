#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Load AI Mapping Training Data
Populates the AI_Mapping table with known good mappings.
"""

import csv
import logging
import os
import sys
from pathlib import Path

try:
    import psycopg2
except ImportError:
    print("psycopg2 is required. Install with: pip install psycopg2-binary")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("python-dotenv is required. Install with: pip install python-dotenv")
    sys.exit(1)

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            dbname=os.getenv('DB_NAME', 'odos_dev'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', '')
        )
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        sys.exit(1)


def load_mappings_from_csv(conn, csv_file):
    logger.info(f"Loading mappings from: {csv_file}")

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        mappings = list(reader)

    logger.info(f"Found {len(mappings)} mappings to load.")

    insert_sql = """
        INSERT INTO AI_Mapping (
            CompanyID, SourceSystem, SourceHeader,
            TargetTable, TargetField,
            ConfidenceScore, IsVerified, UsageCount,
            SourceFileExample, CreatedBy, CreatedDateTime,
            LastModifiedBy, LastModifiedDateTime,
            EffectiveFrom
        ) VALUES (
            1, %s, %s,
            %s, %s,
            %s, %s, %s,
            %s, 'ETL_LOAD', CURRENT_TIMESTAMP,
            'ETL_LOAD', CURRENT_TIMESTAMP,
            CURRENT_TIMESTAMP
        )
        ON CONFLICT (CompanyID, SourceSystem, SourceHeader, TargetTable, TargetField)
        DO UPDATE SET
            ConfidenceScore = EXCLUDED.ConfidenceScore,
            IsVerified = EXCLUDED.IsVerified,
            UsageCount = EXCLUDED.UsageCount,
            LastModifiedBy = 'ETL_LOAD',
            LastModifiedDateTime = CURRENT_TIMESTAMP
    """

    cur = conn.cursor()
    count = 0
    for row in mappings:
        try:
            cur.execute(insert_sql, (
                row['source_system'],
                row['source_header'],
                row['target_table'],
                row['target_field'],
                float(row['confidence_score']),
                row['is_verified'].strip().upper() == 'TRUE',
                int(row['usage_count']),
                row.get('source_file_example', '')
            ))
            count += 1
        except Exception as e:
            logger.warning(f"Failed to load mapping: {row} - {e}")

    conn.commit()
    cur.close()
    logger.info(f"Loaded {count} mappings successfully.")


def main():
    print("=" * 60)
    print("Load AI Mapping Training Data")
    print("=" * 60)

    conn = get_db_connection()
    logger.info("Connected to database.")

    csv_file = Path("AI_Mapping_Training.csv")
    if not csv_file.exists():
        logger.error(f"Training file not found: {csv_file}")
        logger.info("Please ensure AI_Mapping_Training.csv is in this folder.")
        sys.exit(1)

    try:
        load_mappings_from_csv(conn, csv_file)
    except Exception as e:
        logger.error(f"Load failed: {e}")
        conn.rollback()
        sys.exit(1)
    finally:
        conn.close()

    print("\n✅ Done.")
    print("AI_Mapping table has been seeded with training data.")


if __name__ == '__main__':
    main()
