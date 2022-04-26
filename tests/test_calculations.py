import pytest
from app.calculations import add, BankAccount, InsufficientFunds


@pytest.fixture
def zero_bank_account():
    print('creating zero bank account with zero balance')
    return BankAccount(0)


@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
])
def test_add(num1, num2, expected):
    print('testing add function')
    assert add(num1, num2) == expected


def test_bank_set_initial_amount():
    bank_account = BankAccount(50)
    assert bank_account.balance == 50


def test_bank_set_default_amount(zero_bank_account):
    print('testing default amount')
    assert zero_bank_account.balance == 0


def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30


def test_deposit(bank_account):
    bank_account.deposit(20)
    assert bank_account.balance == 70


def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55


@pytest.mark.parametrize("deposit, withdraw, expected", [
                         [200, 100, 100],
                         [150, 50, 100],
                         [1200, 200, 1000]
                         ])
def test_bank_transaction(zero_bank_account, deposit, withdraw, expected):
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected


def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)
