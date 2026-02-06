"""Class that will write the transactions to the database"""
import sqlite3
from datetime import datetime

from src.domain.models import Transaction


class SQLiteRepository:
    """Class that will handle the database operations"""

    def __init__(self, db_path: str = "finance.db") -> None: 
        """Initialize the repository with the database path"""
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        """Initialize the database"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL,
                type TEXT,
                category TEXT,
                description TEXT,
                date TEXT
            )
        """)
        conn.commit()
        conn.close()

    def add(self, tx: Transaction) -> int | None:
        """Add a new transaction to the database"""
        conn = sqlite3.connect(self.db_path)
        cur = conn.execute(
            "INSERT INTO transactions\
                  (amount, type, category, description, date) VALUES (?, ?, ?, ?, ?)",
            (tx.amount, tx.type, tx.category, tx.description, tx.date.strftime('%Y/%m/%d'))
        )
        conn.commit()
        tx_id = cur.lastrowid
        conn.close()
        return tx_id
    
    def remove(self, tx_id: int) -> bool:
        """Remove a transaction from the database by its ID"""
        conn = sqlite3.connect(self.db_path)
        
        list_of_ids = [row[0] for row in conn.execute("SELECT id FROM transactions").fetchall()]
        if tx_id not in list_of_ids:
            conn.close()
            return False
        conn.execute("DELETE FROM transactions WHERE id = ?", (tx_id,))
        conn.commit()
        conn.close()
        return True

    def list(self) -> list[tuple[int, Transaction]]:
        """List all transactions in the database"""
        conn = sqlite3.connect(self.db_path)
        cur = conn.execute("SELECT id, amount, type, category, description, date FROM transactions")
        rows = cur.fetchall()
        conn.close()

        transactions = []
        
        for row in rows:
            tx = Transaction(
                amount=row[1],
                type=row[2],
                category=row[3],
                description=row[4],
                date=datetime.strptime(row[5], '%Y/%m/%d')
            )
            transactions.append((row[0],tx))
        return transactions