"""Main code for CLI"""
from datetime import datetime

import typer

from src.application.transaction_service import TransactionService

service = TransactionService()


app = typer.Typer(help="Personal finance tracker CLI")

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Welcome message for the finance CLI."""
    if ctx.invoked_subcommand is None:
        typer.echo("===================================")
        typer.echo("Personal Finance Tracker CLI...")
        typer.echo("===================================")
        typer.echo("Use 'python -m finance.cli.main --help' to see available commands.")


DESCRIPTION_OPTION_ADD = typer.Option("", "--description", "-d", help="Optional description")
DATE_OPTION_ADD = typer.Option(None, "--date", "-t", help="Optional date in YYYY-MM-DD format")


@app.command()
def add(
    amount: float = typer.Argument(..., help="Transaction amount (must be positive)"),
    type: str = typer.Argument
    (..., help="Transaction type: 'i for income' or 'e for expense'"),
    category: str = typer.Argument
    (..., help=f"Transaction category ({service.return_categories()})"),
    description: str = DESCRIPTION_OPTION_ADD,
    date: datetime | None = DATE_OPTION_ADD,
) -> None:
    """Add a new financial transaction."""
    transaction_id = service.add_transaction(
        amount=amount,
        type=type,
        category=category,
        description=description,
        date=date,
    )

    typer.secho(f"Transaction #{transaction_id} added successfully.")



@app.command()
def remove(
    transaction_id: int = typer.Argument(..., help="ID of the transaction to remove")
) -> None:
    """Remove a financial transaction by its ID."""
    if service.remove_transaction(transaction_id):
        typer.secho(f"Transaction #{transaction_id} removed successfully.")
    else:
        typer.secho(f"Transaction ID {transaction_id} does not exist.", fg=typer.colors.RED)


AFTER_OPTION_LIST = typer.Option(
            None, "--after", "-a", help="List transactions after this date (YYYY-MM-DD)")
BEFORE_OPTION_LIST = typer.Option(
            None, "--before", "-b", help="List transactions before this date (YYYY-MM-DD)")

@app.command()
def list(
        after: datetime | None = AFTER_OPTION_LIST,
        before: datetime | None = BEFORE_OPTION_LIST,
        category: str | None = typer.Option(
            None, "--category", "-c", help="List transactions of this category"),
        type: str | None = typer.Option(
            None, "--type", "-t", help="List transactions of this type ('i' or 'e')")
) -> None:
    """List all financial transactions."""
    transactions = service.list()

    if not transactions:
        typer.secho("No transactions found.", fg=typer.colors.YELLOW)
        return
    
    transactions.sort(key=lambda tx: tx[1].date)

    if after:
        transactions = [
            transaction for transaction in transactions
            if transaction[1].date > after
        ]
    if before:
        transactions = [
            transaction for transaction in transactions
            if transaction[1].date < before
        ]
    if category:
        transactions = [
            transaction for transaction in transactions
            if transaction[1].category == category
        ]
    if type:
        transactions = [
            transaction for transaction in transactions
            if transaction[1].type == type
        ]

    for transaction_id, transaction in transactions:
        typer.secho(
            f"ID: {transaction_id} | "
            f"[{transaction.date.strftime('%Y/%m/%d')}] "
            f"Type: {transaction.type.upper()}, Amount: {transaction.amount}, "
            f"Category: {transaction.category}, Description: {transaction.description}",
            fg=typer.colors.GREEN
        )
    
@app.command()
def add_category(
    new_category: str = typer.Argument(..., help="Name of the new category to add")
) -> None:
    """Add a new category to the category list."""
    service.add_category(new_category)
    typer.secho(f"Category '{new_category}' added successfully.")


@app.command()
def list_categories() -> None:
    """List all available categories."""
    categories = service.return_categories()
    typer.secho("Available Categories:", fg=typer.colors.BLUE)
    for category in categories.split(", "):
        typer.secho(f"- {category}", fg=typer.colors.BLUE)

@app.command()
def remove_category(
    category_to_remove: str = typer.Argument(..., help="Name of the category to remove")
) -> None:
    """Remove a category from the category list."""
    if service.remove_category(category_to_remove):
        typer.secho(f"Category '{category_to_remove}' removed successfully.")
    else:
        typer.secho(f"Category '{category_to_remove}' does not exist.", fg=typer.colors.RED)


@app.command()
def report() -> None:
    """Print reports and save spending plot"""
    service.report()


if __name__ == "__main__":
    app()