from __future__ import annotations

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.main import app
from app.models.task import Task
from app.models.task_audit import TaskAudit
from app.core.database import get_db


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(autouse=True)
def clean_database(db_session: Session) -> Generator[None, None, None]:
    db_session.execute(delete(TaskAudit))
    db_session.execute(delete(Task))
    db_session.commit()
    yield
    db_session.execute(delete(TaskAudit))
    db_session.execute(delete(Task))
    db_session.commit()


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        session: Session = SessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
