"""
Module testing bank account module
"""
# pylint: disable=missing-docstring
from datetime import date
from banking import Account, Transaction


def test_transaction():
    assert str(Transaction(100)) == f"$100.00 on {date.today()}"


def test_timestamp():
    assert str(Transaction(100, date(2020, 1, 1))) == "$100.00 on 2020-01-01"


def test_deposit():
    account = Account()
    assert account.deposit(100) == f"$100.00 on {date.today()}"


def test_withdrawal():
    account = Account()
    assert account.withdrawal(100) == f"$-100.00 on {date.today()}"


def test_get_balance():
    account = Account()
    account.deposit(75)
    assert account.get_balance() == "Balance: $75.00"
    account.withdrawal(25)
    assert account.get_balance() == "Balance: $50.00"


def test_transaction_list():
    account = Account()
    account.deposit(145.66)
    account.withdrawal(34.34)
    account.deposit(25.00)
    account.deposit(1345.78)
    account.withdrawal(98)
    assert account.print_transactions() == [
        f'$145.66 on {date.today()}',
        f'$-34.34 on {date.today()}',
        f'$25.00 on {date.today()}',
        f'$1,345.78 on {date.today()}',
        f'$-98.00 on {date.today()}']
