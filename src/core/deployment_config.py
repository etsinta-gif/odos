from __future__ import annotations

import ipaddress
from urllib.parse import urlparse


def public_http_url(value: str) -> str | None:
    """Return a normalized public HTTP(S) URL, or None for local/invalid values."""
    candidate = value.strip()
    parsed = urlparse(candidate)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return None
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        return None

    hostname = (parsed.hostname or "").rstrip(".").lower()
    if not hostname or hostname in {"localhost", "localhost.localdomain"} or hostname.endswith(".local"):
        return None

    try:
        address = ipaddress.ip_address(hostname)
    except ValueError:
        address = None
    if address is not None and (
        address.is_loopback
        or address.is_private
        or address.is_link_local
        or address.is_unspecified
        or address.is_reserved
    ):
        return None

    return candidate.rstrip("/")


def database_url_from_environment(environ: dict[str, str] | None = None) -> str:
    values = environ if environ is not None else {}
    configured = (values.get("DATABASE_URL") or "").strip()
    if configured:
        return configured

    app_env = (values.get("APP_ENV") or "development").strip().lower()
    if app_env in {"production", "prod", "staging"}:
        raise RuntimeError(
            "DATABASE_URL must be configured for production or staging; "
            "refusing to use local SQLite persistence."
        )
    return "sqlite:///./odos.db"