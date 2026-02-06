import os
import sqlite3
import tempfile
import pytest
from datetime import datetime
from src.application.transaction_service import TransactionService
from src.infrastructure.sqlite_repository import SQLiteRepository


@pytest.fixture
def temp_repo():
    """Fixture to create a temporary SQLiteRepository."""
    db_path = tempfile.mktemp()
    repo = SQLiteRepository(db_path)
    yield repo
    os.remove(db_path)


@pytest.fixture
def service(temp_repo):
    """Fixture that provides a TransactionService wired to a temp repo."""
    return TransactionService(temp_repo)


def test_add_transaction_inserts_row_correctly(service, temp_repo):
    """Verify that add_transaction inserts correct data into the database."""
    tx_id = service.add_transaction(
        amount=100.5,
        type="i",
        category="salary",
        description="monthly pay",
        date=datetime(2025, 11, 9),
    )

    assert tx_id == 1

    conn = sqlite3.connect(temp_repo.db_path)
    row = conn.execute(
        "SELECT amount, type, category, description, date FROM transactions"
    ).fetchone()
    conn.close()

    assert row == (
        100.5,
        "i",
        "salary",
        "monthly pay",
        "2025/11/09", 
    )


def test_add_transaction_defaults_description_and_date(service, temp_repo):
    """Ensure description defaults to '' and date defaults to now."""
    tx_id = service.add_transaction(amount=50, type="e", category="food")

    assert tx_id == 1

    conn = sqlite3.connect(temp_repo.db_path)
    row = conn.execute(
        "SELECT amount, type, category, description, date FROM transactions"
    ).fetchone()
    conn.close()

    assert row[0] == 50
    assert row[1] == "e"
    assert row[2] == "food"
    assert row[3] == ""
    assert isinstance(row[4], str)
    assert len(row[4].split("/")) == 3