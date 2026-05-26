# test_bank_account.py
import pytest
import logging
from bank_account import BankAccount


def test_initial_balance():
    acc = BankAccount("Test", 100)
    assert acc.balance == 100


def test_default_balance():
    acc = BankAccount("Test")
    assert acc.balance == 0


def test_deposit_negative():
    acc = BankAccount("Test", 50)
    with pytest.raises(ValueError):
        acc.withdraw(-10)


@pytest.fixture
def account():
    """Создаёт счёт с начальным балансом 1000."""
    return BankAccount("Иван", 1000)


def test_deposit(account):
    account.deposit(500)
    assert account.balance == 1500


def test_withdraw(account):
    account.withdraw(200)
    assert account.balance == 800


def test_balance_setter_negative(account):
    with pytest.raises(ValueError):
        account.balance = -100


def test_equality():
    a1 = BankAccount("A", 100)
    a2 = BankAccount("A", 100)
    a3 = BankAccount("B", 100)
    assert a1 == a2
    assert a1 != a3


@pytest.mark.parametrize(
    "initial,deposit_amount,expected",
    [
        (0, 500, 500),
        (100, 50, 150),
        (1000, 0, 1000),  # если 0 разрешён? у тебя запрещён, будет исключение
    ],
)
def test_deposit_variants(initial, deposit_amount, expected):
    acc = BankAccount("Test", initial)
    if deposit_amount <= 0:
        with pytest.raises(ValueError):
            acc.deposit(deposit_amount)
    else:
        acc.deposit(deposit_amount)
        assert acc.balance == expected


def test_withdraw_insufficient_funds(caplog, account):
    with caplog.at_level(logging.WARNING):
        with pytest.raises(ValueError):
            account.withdraw(10000)
    # Посмотреть все сообщения
    print("Messages:", caplog.messages)
    # Проверить конкретную запись
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "WARNING"
    assert "Insufficient funds" in caplog.records[0].message

