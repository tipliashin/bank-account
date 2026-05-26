import pytest
from bank_account import BankAccount


@pytest.fixture
def account():
    """Создаёт счёт с начальным балансом 1000."""
    return BankAccount("Иван", 1000)


def test_create_acc():
    acc = BankAccount("Andrey", 500)
    acc1 = BankAccount("Kristina")
    assert acc.balance == 500
    assert acc.owner == "Andrey"
    assert acc1.balance == 0
    assert acc1.owner == "Kristina"


def test_deposit_positive(account):
    account.deposit(500)
    assert account.balance == 1500


def test_deposit_negative_raises(account):
    with pytest.raises(ValueError, match="Сумма должна быть положительной"):
        account.deposit(-50)


def test_deposit_zero_raises(account):
    with pytest.raises(ValueError, match="Сумма должна быть положительной"):
        account.deposit(0)


def test_withdraw_positive(account):
    account.withdraw(500)
    assert account.balance == 500


def test_withdraw_insufficient_funds_raises(account):
    with pytest.raises(ValueError, match="Недостаточно средств"):
        account.withdraw(1500)
    assert account.balance == 1000


def test_withdraw_negative_raises(account):
    with pytest.raises(ValueError, match="Сумма должна быть положительной"):
        account.withdraw(-500)
    assert account.balance == 1000


def test_iadd(account):
    account += 500
    assert account.balance == 1500


def test_isub(account):
    account -= 500
    assert account.balance == 500


def test_eq_ne():
    a1 = BankAccount("A", 100)
    a2 = BankAccount("A", 100)
    a3 = BankAccount("B", 99)
    assert a1 == a2
    assert a1 != a3


def test_lt_gt():
    a1 = BankAccount("A", 100)
    a2 = BankAccount("B", 99)
    assert a2 < a1
    assert a1 > a2


def test_setter_balance_negative_raises():
    acc = BankAccount("Test", 100)
    with pytest.raises(ValueError, match="Balance can't be negative"):
        acc.balance = -2000
    assert acc.balance == 100


def test_from_string_with_balance():
    acc = BankAccount.from_string("Анна:500")
    assert acc.owner == "Анна"
    assert acc.balance == 500.0


def test_from_string_without_balance():
    acc = BankAccount.from_string("Просто имя")
    assert acc.owner == "Просто имя"
    assert acc.balance == 0.0
