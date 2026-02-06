"""Class that will keep record of categories"""
import sqlite3


class CategoryRepository:
    """Class that will handle the category operations"""

    def __init__(self, db_path: str = "categories.db") -> None: 
        """Initialize the repository with the database path"""
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        """Initialize the database"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            )
        """)
        conn.commit()
        default_categories = ['food', 'salary', 'utilities', 'transportation']
        for category in default_categories:
            conn.execute(
                "INSERT OR IGNORE INTO categories (name) VALUES (?)",
                (category,)
            )
        conn.commit()
        conn.close()

    def add_category_to_file(self, category_name: str) -> int | None:
        """Add a new category to the database"""
        conn = sqlite3.connect(self.db_path)
        cur = conn.execute(
            "INSERT INTO categories (name) VALUES (?)",
            (category_name,)
        )
        conn.commit()
        category_id = cur.lastrowid
        conn.close()
        return category_id
    
    def read_categories(self) -> list[str]:
        """Read categories from the database"""
        conn = sqlite3.connect(self.db_path)
        cur = conn.execute("SELECT name FROM categories")
        categories = [row[0] for row in cur.fetchall()]
        conn.close()
        return categories
    
    def remove_category_from_file(self, category_name: str) -> bool:
        """Remove a category from the database"""
        conn = sqlite3.connect(self.db_path)
        cur = conn.execute("DELETE FROM categories WHERE name = ?", (category_name,))
        conn.commit()
        rows_affected = cur.rowcount
        conn.close()
        return rows_affected > 0