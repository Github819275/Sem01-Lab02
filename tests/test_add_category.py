import os
import tempfile
import pytest
from src.application.transaction_service import TransactionService
from src.categories.category_repository import CategoryRepository


@pytest.fixture
def temp_category_repo():
    db_path = tempfile.mktemp()
    repo = CategoryRepository(db_path)
    yield repo
    os.remove(db_path)


@pytest.fixture
def service(temp_category_repo):
    s = TransactionService(repo=None)
    s.category_repo = temp_category_repo
    return s


def test_add_category(service):
    service.add_category("gaming")
    categories = service.return_categories().split(", ")

    assert "gaming" in categories


def test_return_categories_contains_defaults(service):
    categories = service.return_categories().split(", ")

    assert "food" in categories
    assert "salary" in categories
    assert "utilities" in categories
    assert "transportation" in categories


def test_remove_category(service):
    service.add_category("gaming")
    removed = service.remove_category("gaming")

    assert removed is True

    categories = service.return_categories().split(", ")
    assert "gaming" not in categories


def test_remove_category_nonexistent(service):
    removed = service.remove_category("ghost")

    assert removed is False
