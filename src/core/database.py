import os

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src.core.deployment_config import database_url_from_environment

def normalize_database_url(database_url: str) -> str:
    parsed = make_url(database_url)
    if parsed.get_backend_name() == "sqlite":
        return database_url

    if parsed.drivername == "postgresql":
        parsed = parsed.set(drivername="postgresql+psycopg")
    if parsed.get_backend_name() == "postgresql" and "sslmode" not in parsed.query:
        parsed = parsed.update_query_dict({"sslmode": "require"})
    return parsed.render_as_string(hide_password=False)


DATABASE_URL = normalize_database_url(database_url_from_environment(dict(os.environ)))


def engine_options(database_url: str) -> dict:
    if make_url(database_url).get_backend_name() == "sqlite":
        return {"connect_args": {"check_same_thread": False}}
    return {}


engine_kwargs = engine_options(DATABASE_URL)
if make_url(DATABASE_URL).query.get("pgbouncer") == "true":
    engine_kwargs["poolclass"] = NullPool

engine = create_engine(DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
