def add(num1: int, num2: int):
    return num1 + num2


def subtract(num1: int, num2: int):
    return num1 - num2


def multiply(num1: int, num2: int):
    return num1*num2


def divide(num1: int, num2: int):
    return num1/num2


class InsufficientFunds(Exception):
    pass


class BankAccount():

    def __init__(self, starting_balance: int = 0) -> None:
        self.balance = starting_balance

    def deposit(self, amount: int):
        self.balance += amount

    def withdraw(self, amount: int):
        if amount > self.balance:
            raise InsufficientFunds("insufficient funds in account")
        self.balance -= amount

    def collect_interest(self):
        self.balance = round(1.1*self.balance, 2)
        