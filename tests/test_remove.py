import os
import sqlite3
import tempfile
import pytest
from datetime import datetime
from src.application.transaction_service import TransactionService
from src.infrastructure.sqlite_repository import SQLiteRepository


@pytest.fixture
def temp_repo():
    db_path = tempfile.mktemp()
    repo = SQLiteRepository(db_path)
    yield repo
    os.remove(db_path)


@pytest.fixture
def service(temp_repo):
    return TransactionService(temp_repo)


def test_remove_existing_transaction(service, temp_repo):
    tx_id = service.add_transaction(
        amount=10,
        type="i",
        category="salary",
        description="test",
        date=datetime(2024, 1, 1),
    )

    removed = service.remove_transaction(tx_id)
    assert removed is True

    conn = sqlite3.connect(temp_repo.db_path)
    rows = conn.execute("SELECT id FROM transactions").fetchall()
    conn.close()

    assert rows == []


def test_remove_nonexistent_transaction(service):
    removed = service.remove_transaction(9999)
    assert removed is False
