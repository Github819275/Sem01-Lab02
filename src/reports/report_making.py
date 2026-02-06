"""Class responsible for making images/reports about the data"""
import matplotlib.pyplot as plt

from src.domain.models import Transaction


class ReportMaking:
    """Class which has functions to make summary tables and spending plots"""

    def __init__(self, file_path: str = "docs") -> None:
        """Initialize the file path"""
        self.file_path = file_path

    def print_reports(self, values: list[tuple[int, Transaction]]) -> None:
        """Print the reports and save the bar chart to docs folder"""
        transactions = [transaction[1] for transaction in values]
        transaction_tuples = [
            (t.amount, t.type, t.category)
            for t in transactions
        ]

        total_income = sum(amount for amount, ttype, _ in transaction_tuples if ttype == "i")
        total_expense = sum(amount for amount, ttype, _ in transaction_tuples if ttype == "e")
        net = total_income - total_expense

        print("=== Income vs Expense ===")
        print(f"Total Income : {total_income:.2f}")
        print(f"Total Expense: {total_expense:.2f}")
        print(f"Net Balance  : {net:.2f}\n")

        
        expense_by_category = {}
        for amount, ttype, category in transaction_tuples:
            if ttype == "e":
                expense_by_category[category] = expense_by_category.get(category, 0) + amount

        print("=== Expenses by Category ===")
        if expense_by_category:
            for cat, amount in expense_by_category.items():
                print(f"{cat:<20} {amount:.2f}")
        else:
            print("No expenses recorded.")
        print()

        
        category_counts = {}
        for _, _, category in transaction_tuples:
            category_counts[category] = category_counts.get(category, 0) + 1

        print("=== Transactions per Category ===")
        for cat, count in category_counts.items():
            print(f"{cat:<20} {count}")

        print()

        if expense_by_category:
            categories = list(expense_by_category.keys())
            amounts = list(expense_by_category.values())

            plt.figure(figsize=(8, 5))
            plt.bar(categories, amounts, color='#11BCC3')
            plt.xlabel('Category')
            plt.ylabel('Amount Spent')
            plt.title('Expenses by Category')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout() 

            
            plot_path = f"{self.file_path}/report.png"
            plt.savefig(plot_path)
            plt.close()