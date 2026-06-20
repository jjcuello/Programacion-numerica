from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


DEFAULT_DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/programacion_numerica"
DEFAULT_SQLITE_PATH = Path(__file__).resolve().parents[3] / "data" / "dev.sqlite3"


def _default_database_url() -> str:
    app_env = os.getenv("APP_ENV", "development").strip().lower()
    if app_env in {"development", "dev", "test", "local"}:
        DEFAULT_SQLITE_PATH.parent.mkdir(parents=True, exist_ok=True)
        return f"sqlite+pysqlite:///{DEFAULT_SQLITE_PATH}"
    return DEFAULT_DATABASE_URL


@dataclass(frozen=True)
class DatabaseSettings:
    url: str = _default_database_url()
    echo: bool = False
    auto_create_schema: bool = False

    @classmethod
    def from_env(cls) -> "DatabaseSettings":
        raw_echo = os.getenv("DATABASE_ECHO", "false").strip().lower()
        raw_auto_create = os.getenv("AUTO_CREATE_SCHEMA", "").strip().lower()
        app_env = os.getenv("APP_ENV", "development").strip().lower()
        default_auto_create = app_env in {"development", "dev", "local", "test"}
        return cls(
            url=os.getenv("DATABASE_URL", _default_database_url()),
            echo=raw_echo in {"1", "true", "yes", "on"},
            auto_create_schema=(raw_auto_create in {"1", "true", "yes", "on"}) if raw_auto_create else default_auto_create,
        )


def create_engine_from_settings(settings: DatabaseSettings) -> Engine:
    connect_args = {"check_same_thread": False} if settings.url.startswith("sqlite+") else {}
    return create_engine(settings.url, echo=settings.echo, future=True, connect_args=connect_args)


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


def initialize_database(engine: Engine) -> None:
    from src.infrastructure.storage.sql_models import Base

    Base.metadata.create_all(engine)
