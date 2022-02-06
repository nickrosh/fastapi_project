import pytest
from app import calculations


@pytest.fixture
def zero_bank_account() -> calculations.BankAccount:
    return calculations.BankAccount()


@pytest.fixture
def bank_account() -> calculations.BankAccount:
    return calculations.BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (6, 7, 13),
    (12, 4, 16)
])
def test_add(num1, num2, expected):
    assert calculations.add(num1, num2) == expected


def test_subtract():
    assert calculations.subtract(5, 3) == 2


def test_multiply():
    assert calculations.multiply(2, 13) == 26


def test_divide():
    assert calculations.divide(10, 2) == 5


def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50


def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_withdraw(bank_account):
    bank_account.withdraw(10)
    assert bank_account.balance == 40


def test_deposit(bank_account):
    bank_account.deposit(10)
    assert bank_account.balance == 60


def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert bank_account.balance == 55

@pytest.mark.parametrize("deposited, withdrew, expected", [
    (100, 25, 75),
    (200, 200, 0),
    (8000, 200, 7800),
    (100, 50, 50)
])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected


def test_insufficient_funds(bank_account):
    with pytest.raises(calculations.InsufficientFunds):
        bank_account.withdraw(200)
