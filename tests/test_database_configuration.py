import pytest

from src.core.database import engine_options, normalize_database_url
from src.core.deployment_config import database_url_from_environment, public_http_url


def test_sqlite_engine_uses_thread_compatibility_option() -> None:
    assert engine_options("sqlite:///./test.db") == {"connect_args": {"check_same_thread": False}}


def test_postgresql_engine_omits_sqlite_connection_arguments() -> None:
    assert engine_options("postgresql+psycopg://odos:odos@db:5432/odos") == {}


def test_supabase_pooler_url_uses_psycopg_and_ssl() -> None:
    normalized = normalize_database_url(
        "postgresql://postgres.project:password@aws-0-region.pooler.supabase.com:6543/postgres?pgbouncer=true"
    )
    assert normalized.startswith("postgresql+psycopg://")
    assert "pgbouncer=true" in normalized
    assert "sslmode=require" in normalized


def test_database_url_does_not_change_sqlite() -> None:
    assert normalize_database_url("sqlite:///./odos.db") == "sqlite:///./odos.db"


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("https://odos.example.com/", "https://odos.example.com"),
        ("http://localhost:3001", None),
        ("http://127.0.0.1:3001", None),
        ("https://192.168.1.20", None),
        ("https://app.example.com/path?local=1", None),
        ("not-a-url", None),
    ],
)
def test_public_http_url_rejects_local_or_unsafe_values(value: str, expected: str | None) -> None:
    assert public_http_url(value) == expected


def test_database_url_defaults_to_sqlite_for_local_development() -> None:
    assert database_url_from_environment({"APP_ENV": "development"}) == "sqlite:///./odos.db"


def test_database_url_requires_external_database_in_production() -> None:
    with pytest.raises(RuntimeError, match="DATABASE_URL must be configured"):
        database_url_from_environment({"APP_ENV": "production"})


def test_database_url_uses_configured_external_database() -> None:
    database_url = "postgresql+psycopg://user:password@db.example.com:5432/odos"
    assert database_url_from_environment({"APP_ENV": "production", "DATABASE_URL": database_url}) == database_url