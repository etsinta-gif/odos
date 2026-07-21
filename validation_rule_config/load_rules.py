#!/usr/bin/env python3
"""
Validation Rule Engine Configuration Loader
For: Aniket (Fresher Friendly)
Version: 1.0
Date: July 2026
Phase: IMP-3.3 - Data Validation

This script loads validation rules into the ODOS Rule Engine database.

Usage:
    python load_rules.py
    python load_rules.py --force    # Force reload even if rules exist
    python load_rules.py --dry-run  # Preview what would be loaded
    python load_rules.py --test     # Test rules with sample data after loading
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("⚠️  'requests' module not found. Installing...")
    os.system("pip install requests")
    import requests

API_BASE_URL = "http://localhost:8000/api/v1"
TIMEOUT = 30


def print_header(text):
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60 + "\n")


def print_success(text):
    print(f"✅ {text}")


def print_error(text):
    print(f"❌ {text}")


def print_warning(text):
    print(f"⚠️  {text}")


def print_info(text):
    print(f"ℹ️  {text}")


def load_json_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print_success(f"Loaded {file_path}")
        return data
    except FileNotFoundError:
        print_error(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        print_error(f"Invalid JSON in {file_path}: {e}")
        return None


def check_api_health():
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def post_to_api(endpoint, data, description):
    url = f"{API_BASE_URL}/{endpoint}"
    try:
        print_info(f"Sending {description} to {url}")
        response = requests.post(
            url,
            json=data,
            timeout=TIMEOUT,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code in (200, 201):
            print_success(f"{description} loaded successfully!")
            return response.json()
        print_error(f"Error loading {description}: {response.status_code}")
        print(response.text[:500])
        return None
    except requests.exceptions.Timeout:
        print_error(f"Timeout loading {description}")
        return None
    except requests.exceptions.ConnectionError:
        print_error(f"Connection error loading {description}")
        print_info("Make sure the backend is running on http://localhost:8000")
        return None
    except Exception as e:
        print_error(f"Unexpected error loading {description}: {e}")
        return None


def test_validation_rules():
    print_header("TESTING VALIDATION RULES")
    script_dir = Path(__file__).parent.absolute()
    test_file = script_dir / "sample_test_data.json"
    if not test_file.exists():
        print_warning("No sample test data found. Skipping tests.")
        return
    test_data = load_json_file(test_file)
    if test_data is None:
        return
    print_info(f"Testing {len(test_data)} records...")
    response = post_to_api("rules/validation/test", test_data, "Validation Test")
    if response:
        print_success("Validation test completed!")
        results = response.get("results", [])
        passed = sum(1 for r in results if r.get("passed", False))
        failed = len(results) - passed
        print_info(f"Passed: {passed}, Failed: {failed}")
        if failed > 0:
            print_warning("Failed records:")
            for r in results:
                if not r.get("passed", False):
                    print(f"  Record {r.get('record_id', 'unknown')}: {r.get('errors', [])}")
    else:
        print_error("Validation test failed!")


def main():
    parser = argparse.ArgumentParser(
        description="Load validation rules into the ODOS Rule Engine"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force reload even if rules already exist"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be loaded without sending to API"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Test rules with sample data after loading"
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="API host (default: localhost)"
    )
    parser.add_argument(
        "--port",
        default="8000",
        help="API port (default: 8000)"
    )

    args = parser.parse_args()
    global API_BASE_URL
    API_BASE_URL = f"http://{args.host}:{args.port}/api/v1"

    print_header("VALIDATION RULE ENGINE - CONFIGURATION LOADER")
    print_info(f"API URL: {API_BASE_URL}")
    print_warning("Phase: IMP-3.3 - Data Validation")

    if args.dry_run:
        print_warning("DRY RUN MODE - No changes will be made")
    if args.force:
        print_warning("FORCE MODE - Will overwrite existing rules")

    print_info("Checking if API is reachable...")
    if not check_api_health():
        print_error("Cannot reach the API!")
        print_info("Make sure the backend is running on http://localhost:8000")
        print_info("Try running: python main.py")
        sys.exit(1)
    print_success("API is reachable!")

    script_dir = Path(__file__).parent.absolute()
    file_path = script_dir / "validation_rules.json"
    data = load_json_file(file_path)
    if data is None:
        sys.exit(1)

    count = 0
    if isinstance(data, list):
        count = len(data)
    elif isinstance(data, dict):
        count = len(data.get("validation_rules", []))
    print_info(f"Found {count} validation rule(s)")

    if args.dry_run:
        print_success(f"DRY RUN: Would load {count} rules")
        rules = data if isinstance(data, list) else data.get("validation_rules", [])
        print("Rules that would be loaded:")
        for idx, rule in enumerate(rules[:5], 1):
            print(f"  {idx}. {rule.get('RuleCode', 'Unknown')} - {rule.get('RuleName', 'Unknown')}")
        if count > 5:
            print(f"  ... and {count - 5} more")
        return

    endpoint = "rules/validation/bulk"
    if args.force:
        endpoint += "?force=true"
    response = post_to_api(endpoint, data, "Validation Rules")
    if not response:
        print_error("Failed to load Validation Rules")
        sys.exit(1)

    print_header("LOAD COMPLETE")
    print_success("ALL RULES LOADED SUCCESSFULLY! 🎉")
    print(f"\nSummary:\n  ✅ {count} validation rules loaded\n")
    if args.test:
        test_validation_rules()
    print("Next Steps:\n1. Verify rules are loaded by checking the database\n2. Run a test case to validate rule execution\n3. Notify the CTO that rules are loaded\n4. Proceed to IMP-3.3 implementation")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️  Interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as exc:
        print_error(f"Unexpected error: {exc}")
        sys.exit(1)
