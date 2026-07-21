import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote
from uuid import uuid4

import requests


BASE_URL = "http://localhost:8000"


def register_tenant(company_name: str, username: str, password: str) -> dict:
    payload = {
        "dsa_code": f"{company_name[:6].upper()}-{uuid4().hex[:6]}",
        "dsa_name": company_name,
        "username": username,
        "password": password,
        "email": f"{username}@example.com",
        "full_name": f"{company_name} Admin",
    }
    response = requests.post(f"{BASE_URL}/api/auth/register", json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def login(username: str, password: str) -> dict:
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"username": username, "password": password},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return {"Authorization": f"Bearer {data['access_token']}"}


def _extract_batch_guid(value: str | None) -> str | None:
    if not value:
        return None
    match = re.search(r"Batch\s+([0-9a-fA-F-]{36})\s+staged", unquote(value))
    return match.group(1) if match else None


def upload_file(
    headers: dict,
    file_path: Path,
    entity_type: str = "MST_Connector",
    template_name: str | None = None,
) -> dict:
    with file_path.open("rb") as handle:
        if template_name:
            response = requests.post(
                f"{BASE_URL}/masters/etl/upload",
                files={"file": (file_path.name, handle, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
                data={"template_name": template_name, "intent": "upload"},
                headers=headers,
                timeout=120,
                allow_redirects=False,
            )
            if response.status_code not in {200, 302, 303}:
                response.raise_for_status()

            location = response.headers.get("location")
            batch_guid = _extract_batch_guid(location)
            if not batch_guid and response.status_code == 200:
                batch_guid = _extract_batch_guid(response.text)

            if batch_guid:
                return {
                    "status_code": response.status_code,
                    "message": "Staged successfully",
                    "batch_guid": batch_guid,
                    "template_name": template_name,
                }

            return {
                "status_code": response.status_code,
                "message": "Template upload did not stage a batch",
                "template_name": template_name,
                "location": location,
                "body_head": response.text[:1200],
            }

        response = requests.post(
            f"{BASE_URL}/api/v1/etl/upload",
            files={"file": handle},
            data={"entity_type": entity_type},
            headers=headers,
            timeout=120,
        )
    response.raise_for_status()
    return response.json()


def promote_batch(headers: dict, batch_guid: str) -> dict:
    response = requests.post(
        f"{BASE_URL}/api/v1/etl/promote",
        data={"batch_guid": batch_guid},
        headers=headers,
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def me(headers: dict) -> dict:
    response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def verify_batch_visible(headers: dict, batch_guid: str) -> bool:
    response = requests.get(f"{BASE_URL}/api/v1/etl/batches", headers=headers, timeout=30)
    response.raise_for_status()
    batches = response.json()
    return any(str(row.get("batch_guid")) == batch_guid for row in batches)


def main() -> None:
    parser = argparse.ArgumentParser(description="Smoke test for new tenant onboarding flow")
    parser.add_argument("--company", required=True, help="Company/DSA name for the run")
    parser.add_argument("--file", required=True, help="Path to source workbook")
    parser.add_argument("--username", default=None, help="Optional username override")
    parser.add_argument("--password", default="Admin@12345", help="Password for the new tenant admin")
    parser.add_argument("--entity-type", default="MST_Connector", help="Entity type for legacy /api/v1/etl/upload path")
    parser.add_argument("--template-name", default=None, help="Optional fixed template name for strict /masters/etl/upload path")
    args = parser.parse_args()

    source_file = Path(args.file)
    if not source_file.exists():
        raise SystemExit(f"Input file not found: {source_file}")

    username = args.username or f"admin_{uuid4().hex[:8]}"

    print(f"Starting smoke test for company: {args.company}")
    registration = register_tenant(args.company, username, args.password)
    print("Registration succeeded")
    print(json.dumps(registration, indent=2))

    headers = login(username, args.password)
    print("Login succeeded")

    profile = me(headers)
    print("Me endpoint result:")
    print(json.dumps(profile, indent=2))

    inferred_template_name = args.template_name
    if inferred_template_name is None:
        template_match = re.search(r"(MIS_TEMPLATE_[^\\/]+\.xlsx)", source_file.name)
        if template_match:
            inferred_template_name = template_match.group(1)

    upload = upload_file(
        headers,
        source_file,
        entity_type=args.entity_type,
        template_name=inferred_template_name,
    )
    print("Upload result:")
    print(json.dumps(upload, indent=2))

    batch_guid = upload.get("batch_guid")
    if not batch_guid:
        raise SystemExit(f"Upload did not return batch_guid. Details: {json.dumps(upload)[:800]}")

    promote = promote_batch(headers, batch_guid)
    print("Promotion result:")
    print(json.dumps(promote, indent=2))

    if not verify_batch_visible(headers, batch_guid):
        raise SystemExit("Tenant batch visibility verification failed")
    print("Tenant-scoped batch visibility verified")

    print("Smoke test completed")


if __name__ == "__main__":
    main()
