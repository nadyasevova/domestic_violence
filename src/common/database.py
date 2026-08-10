import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.engine import Engine

PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")


def get_required_env(variable_name: str) -> str:
    value = os.getenv(variable_name)

    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {variable_name}"
        )

    return value


def get_engine() -> Engine:
    database_url = URL.create(
        drivername="postgresql+psycopg",
        username=get_required_env("POSTGRES_USER"),
        password=get_required_env("POSTGRES_PASSWORD"),
        host=get_required_env("POSTGRES_HOST"),
        port=int(get_required_env("POSTGRES_PORT")),
        database=get_required_env("POSTGRES_DB"),
    )

    return create_engine(database_url)