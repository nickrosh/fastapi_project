import pytest
from app import calculations


@pytest.mark.parametrize()
def test_add():
    assert calculations.add(5, 3) == 8


def test_subtract():
    assert calculations.subtract(5, 3) == 2


def test_multiply():
    assert calculations.multiply(2, 13) == 26


def test_divide():
    assert calculations.divide(10, 2) == 5