"""Service that will call the functions from sqlite_repo and get called from CLI"""

from datetime import datetime

from src.categories.category_repository import CategoryRepository
from src.domain.models import Transaction
from src.infrastructure.sqlite_repository import SQLiteRepository
from src.reports.report_making import ReportMaking


class TransactionService:
    """Initialize all services"""

    def __init__(self, repo: SQLiteRepository | None = None) -> None:
        """Initialize a repository"""
        if repo is None:
            self.repo = SQLiteRepository()
        else:
            self.repo = repo
        self.category_repo = CategoryRepository()
        self.report_repo = ReportMaking()

    def add_category(self, new_category: str) -> None:
        """Add a new category to the category list."""
        self.category_repo.add_category_to_file(new_category)

    def return_categories(self) -> str:
        """Return the list of categories."""
        return ", ".join(self.category_repo.read_categories())
    
    def remove_category(self, category_to_remove: str) -> bool:
        """Remove a category from the category list."""
        return self.category_repo.remove_category_from_file(category_to_remove)

    def add_transaction(self, amount: float, type: str, category: str,
        description: str = "", date: datetime | None = None) -> int | None:
        """Add a new transaction after validation.

        Args:
            amount: The transaction amount.
            type: "i for income" or "e for expense".
            category: The category of the transaction ('food', 'salary', etc.)
            description: Optional description.
            date: Optional date (defaults to now).

        Returns:
            The auto-generated transaction ID.
        """
        date = date or datetime.now()

        new_transaction = Transaction(type=type, amount=amount, category=category,
                                       description=description, date=date)

        new_transaction_id = self.repo.add(new_transaction)
        return new_transaction_id
    
    def remove_transaction(self, tx_id: int) -> bool:
        """Remove a transaction by its ID.

        Args:
            tx_id: The ID of the transaction to remove.
        """
        return self.repo.remove(tx_id)

    def list(self) -> list[tuple[int, Transaction]]:
        """List all transactions.

        Returns:
            A list of all transactions.
        """
        return self.repo.list()
    
    def report(self) -> None:
        """Run the report function from reportclass"""
        self.report_repo.print_reports(self.list())
    
    