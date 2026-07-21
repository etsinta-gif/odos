#!/usr/bin/env python3
"""
Rule Engine Configuration Loader
For: Aniket (Fresher Friendly)
Version: 1.0
Date: July 2026

This script loads business rules (Commission, GST, TDS, Validation)
into the ODOS Rule Engine database.

Usage:
    python load_rules.py
    python load_rules.py --force    # Force reload even if rules exist
    python load_rules.py --dry-run  # Preview what would be loaded
"""

import json
import os
import sys
import argparse
from pathlib import Path

# Try to import requests, but handle gracefully if not installed
try:
    import requests
except ImportError:
    print("⚠️  'requests' module not found. Installing...")
    os.system("pip install requests")
    import requests

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"
TIMEOUT = 30  # seconds

# Color codes for pretty output
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def print_header(text):
    """Print a formatted header."""
    print(f"\n{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}\n")


def print_success(text):
    """Print a success message."""
    print(f"{Colors.GREEN}✅ {text}{Colors.RESET}")


def print_error(text):
    """Print an error message."""
    print(f"{Colors.RED}❌ {text}{Colors.RESET}")


def print_warning(text):
    """Print a warning message."""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.RESET}")


def print_info(text):
    """Print an info message."""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.RESET}")


def load_json_file(file_path):
    """Load and validate a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
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
    """Check if the API is reachable."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False


def post_to_api(endpoint, data, description):
    """Post data to an API endpoint."""
    url = f"{API_BASE_URL}/{endpoint}"
    
    try:
        print_info(f"Sending {description} to {url}")
        response = requests.post(
            url,
            json=data,
            timeout=TIMEOUT,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code in [200, 201]:
            print_success(f"{description} loaded successfully!")
            return response.json()
        else:
            print_error(f"Error loading {description}: {response.status_code}")
            print(f"Response: {response.text[:500]}")
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


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Load business rules into the ODOS Rule Engine"
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
    
    # Update API URL if host/port changed
    global API_BASE_URL
    API_BASE_URL = f"http://{args.host}:{args.port}/api/v1"
    
    # Print welcome header
    print_header("RULE ENGINE CONFIGURATION LOADER")
    print_info(f"API URL: {API_BASE_URL}")
    
    if args.dry_run:
        print_warning("DRY RUN MODE - No changes will be made")
    
    if args.force:
        print_warning("FORCE MODE - Will overwrite existing rules")
    
    # Check API health
    print_info("Checking if API is reachable...")
    if not check_api_health():
        print_error("Cannot reach the API!")
        print_info("Make sure the backend is running on http://localhost:8000")
        print_info("Try running: python main.py")
        sys.exit(1)
    print_success("API is reachable!")
    
    # Get the directory of this script
    script_dir = Path(__file__).parent.absolute()
    
    # Define files to load
    files_to_load = [
        {
            "filename": "commission_rules.json",
            "endpoint": "rules/commission/bulk",
            "description": "Commission Rules",
            "required": True
        },
        {
            "filename": "gst_tds_rules.json",
            "endpoint": "rules/tax/bulk",
            "description": "GST & TDS Rules",
            "required": True
        },
        {
            "filename": "validation_rules.json",
            "endpoint": "rules/validation/bulk",
            "description": "Validation Rules",
            "required": True
        }
    ]
    
    # Track results
    results = {
        "total": 0,
        "success": 0,
        "failed": 0,
        "details": []
    }
    
    # Load each file
    for file_info in files_to_load:
        file_path = script_dir / file_info["filename"]
        print_header(f"Loading {file_info['description']}")
        
        # Load JSON
        data = load_json_file(file_path)
        if data is None:
            if file_info["required"]:
                print_error(f"Required file {file_info['filename']} could not be loaded!")
                results["failed"] += 1
                results["details"].append({
                    "file": file_info["filename"],
                    "status": "failed",
                    "reason": "File not found or invalid JSON"
                })
            continue
        
        # Count records for preview
        if isinstance(data, list):
            count = len(data)
        elif isinstance(data, dict):
            # Try to find the rules array
            for key in ["rules", "commission_rules", "gst_rules", "tds_rules", "validation_rules"]:
                if key in data and isinstance(data[key], list):
                    count = len(data[key])
                    break
            else:
                count = 1  # Single rule object
        else:
            count = 1
        
        print_info(f"Found {count} rule record(s)")
        
        if args.dry_run:
            print_success(f"DRY RUN: Would load {count} rules from {file_info['filename']}")
            results["details"].append({
                "file": file_info["filename"],
                "status": "dry-run",
                "count": count
            })
            continue
        
        # Send to API
        response = post_to_api(
            file_info["endpoint"],
            data,
            file_info["description"]
        )
        
        if response:
            results["success"] += 1
            results["details"].append({
                "file": file_info["filename"],
                "status": "success",
                "response": response
            })
            print_success(f"✅ {file_info['description']} loaded successfully!")
        else:
            results["failed"] += 1
            results["details"].append({
                "file": file_info["filename"],
                "status": "failed",
                "reason": "API error"
            })
            print_error(f"❌ Failed to load {file_info['description']}")
    
    # Print summary
    print_header("LOAD COMPLETE")
    
    total = len(files_to_load)
    success = results["success"]
    failed = results["failed"]
    
    if failed == 0 and success > 0:
        print_success("ALL RULES LOADED SUCCESSFULLY! 🎉")
    elif failed > 0:
        print_warning(f"Loaded {success} of {total} rule sets. {failed} failed.")
        print_info("Check the errors above and try again.")
    else:
        print_warning("No rules were loaded. Check if files exist.")
    
    # Print detailed summary
    print(f"\n{Colors.BOLD}Summary:{Colors.RESET}")
    for detail in results["details"]:
        if detail["status"] == "success":
            status_color = Colors.GREEN
            status_text = "✅"
        elif detail["status"] == "failed":
            status_color = Colors.RED
            status_text = "❌"
        else:
            status_color = Colors.YELLOW
            status_text = "⏭️"
        
        print(f"  {status_color}{status_text} {detail['file']}{Colors.RESET}")
    
    print(f"\n{Colors.BOLD}Next Steps:{Colors.RESET}")
    print("1. Verify rules are loaded by checking the database")
    print("2. Run a test case to validate rule execution")
    print("3. Notify the CTO that rules are loaded")
    print("4. Proceed to Phase 4 development")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
