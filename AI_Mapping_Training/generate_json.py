import csv
import json
from pathlib import Path

path = Path(__file__).parent
csv_file = path / 'AI_Mapping_Training.csv'
json_file = path / 'AI_Mapping_Training.json'

with open(csv_file, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = [
        {
            'source_system': r['source_system'],
            'source_header': r['source_header'],
            'target_table': r['target_table'],
            'target_field': r['target_field'],
            'confidence_score': float(r['confidence_score']),
            'is_verified': r['is_verified'].strip().upper() == 'TRUE',
            'usage_count': int(r['usage_count']),
            'source_file_example': r['source_file_example']
        }
        for r in reader
    ]

with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(rows, f, indent=2)

print('JSON created:', json_file)
