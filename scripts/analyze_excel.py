import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.admin.services.file_analyzer import analyze_excel_bytes
from src.admin.services.mapper import generate_mapping_proposal


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze an Excel file and generate a mapping proposal.")
    parser.add_argument("--file", "-f", required=True, help="Path to the Excel file")
    parser.add_argument("--sheet", "-s", help="Optional specific sheet name")
    parser.add_argument("--header", type=int, default=1, help="Header row number (default: 1)")
    parser.add_argument("--output", "-o", help="Output JSON file path")
    parser.add_argument("--generate-mapping", "-g", action="store_true", help="Generate mapping proposal")
    args = parser.parse_args()

    with open(args.file, "rb") as handle:
        file_bytes = handle.read()

    analysis = analyze_excel_bytes(file_bytes, sheet_name=args.sheet, header_row=args.header)
    output = generate_mapping_proposal(analysis) if args.generate_mapping else analysis

    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            json.dump(output, handle, indent=2, default=str)
        print(f"Analysis saved to {args.output}")
    else:
        print(json.dumps(output, indent=2, default=str))


if __name__ == "__main__":
    main()
