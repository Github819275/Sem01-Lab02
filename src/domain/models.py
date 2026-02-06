"""Create the DTO for financial transactions"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Transaction:
    """Object that carries all data of the financial transaction""" 
    type: str  # "i for income" or "e for expense"
    amount: float
    category: str
    description: str = ""
    date: datetime = field(default_factory=datetime.now)

