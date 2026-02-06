import os
import tempfile
import pytest
from datetime import datetime
from src.application.transaction_service import TransactionService
from src.infrastructure.sqlite_repository import SQLiteRepository
from src.domain.models import Transaction


@pytest.fixture
def temp_repo():
    db_path = tempfile.mktemp()
    repo = SQLiteRepository(db_path)
    yield repo
    os.remove(db_path)


@pytest.fixture
def service(temp_repo):
    return TransactionService(temp_repo)


def test_list_empty_returns_empty_list(service):
    result = service.list()
    assert result == []


def test_list_single_transaction(service):
    service.add_transaction(
        amount=100,
        type="i",
        category="salary",
        description="one",
        date=datetime(2024, 1, 1),
    )

    result = service.list()

    assert len(result) == 1

    tx_id, tx = result[0]

    assert tx_id == 1
    assert isinstance(tx, Transaction)

    assert tx.amount == 100
    assert tx.type == "i"
    assert tx.category == "salary"
    assert tx.description == "one"
    assert tx.date == datetime(2024, 1, 1)


def test_list_multiple_transactions(service):
    service.add_transaction(
        amount=50,
        type="e",
        category="food",
        description="first",
        date=datetime(2024, 1, 1),
    )
    service.add_transaction(
        amount=200,
        type="i",
        category="salary",
        description="second",
        date=datetime(2024, 1, 2),
    )

    result = service.list()

    assert len(result) == 2

    (id1, tx1) = result[0]
    (id2, tx2) = result[1]

    assert id1 == 1
    assert id2 == 2

    assert tx1.amount == 50
    assert tx1.type == "e"
    assert tx1.category == "food"

    assert tx2.amount == 200
    assert tx2.type == "i"
    assert tx2.category == "salary"
