"""
Module creating bank account and transaction history
"""
from dataclasses import dataclass
from datetime import date


@dataclass
class Transaction:
    """class representing a single transaction"""
    amount: float
    timestamp: date = None

    if timestamp is None:
        timestamp = date.today()

    def __str__(self):
        return f"${self.amount:,.2f} on {self.timestamp}"

    def __repr__(self):
        return f"Amount: {self.amount}  Timestamp: {self.timestamp}"


class Account:
    """class representing bank account"""
    def __init__(self):
        self.transactions = []
        self.amount = None
        self.balance = 0.00
        self.timestamp = None

    def deposit(self, amount: int):
        """Simple deposit function"""
        self.amount = abs(amount)
        transaction = f"{Transaction(self.amount)}"
        self.transactions.append(transaction)
        self.balance = self.balance + self.amount
        return transaction

    def withdrawal(self, amount: int):
        """Simple withdrawal function"""
        self.amount = -abs(amount)
        transaction = f"{Transaction(self.amount)}"
        self.transactions.append(transaction)
        self.balance = self.balance + self.amount
        return transaction

    def get_balance(self):
        """Print total balance"""
        print(f"Balance: ${self.balance:,.2f}")
        return f"Balance: ${self.balance:,.2f}"

    def print_transactions(self):
        """Prints a list of transactions"""
        print(self.transactions)
        return self.transactions
