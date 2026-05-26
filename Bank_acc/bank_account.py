import logging

logger = logging.getLogger(__name__)  # только создали, не настраивали!

class BankAccount:
    def __init__(self, owner, initial_balance=0):
        self.owner = owner
        self._balance = initial_balance

    @property
    def balance(self):
        """Возвращает текущий баланс."""
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("Balance can't be negative")
        self._balance = value

    @staticmethod
    def _validate_amount(amount):
        """Проверяет, что сумма положительна. Выбрасывает ValueError."""
        if not isinstance(amount, (int, float)):
            raise TypeError("Сумма должна быть числом")
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")

    @classmethod
    def from_string(cls, string):
        try:
            owner, balance_str = string.split(":")
            balance = float(balance_str) if balance_str else 0.0
        except ValueError:
            owner = string
            balance = 0.0
        return cls(owner, balance)

    def deposit(self, amount):
        self._validate_amount(amount)
        self.balance += amount  # использует сеттер
        logger.info(f"Deposited {amount} to {self.owner}. Balance: {self.balance}")

    def withdraw(self, amount):
        self._validate_amount(amount)
        if amount > self.balance:  # использует геттер
            logger.warning(
                f"Insufficient funds for {self.owner}: "
                f"tried to withdraw {amount}, balance {self.balance}"
            )
            raise ValueError("Недостаточно средств")
        self.balance -= amount
        logger.info(f"Withdrew {amount} from {self.owner}. Balance: {self.balance}")

    def __str__(self):
        return f"Счёт владельца {self.owner}: баланс = {self.balance}"

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self._balance == other._balance and self.owner == other.owner

    def __ne__(self, other):
        # можно просто вернуть not self == other
        if not isinstance(other, BankAccount):
            return NotImplemented
        return not self == other

    def __lt__(self, other):
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self._balance < other._balance

    def __gt__(self, other):
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self._balance > other._balance

    def __iadd__(self, amount):
        self.deposit(amount)
        return self

    def __isub__(self, amount):
        self.withdraw(amount)
        return self


class SavingsAccount(BankAccount):
    def __init__(self, owner, initial_balance, interest_rate):
        super().__init__(owner, initial_balance)
        self.interest_rate = interest_rate

    def apply_interest(self):
        self._balance += self._balance * self.interest_rate

    def __str__(self):
        return (
            f"Накопительный счёт владельца {self.owner}: "
            f"баланс = {self._balance}, ставка = {self.interest_rate}"
        )


class CreditAccount(BankAccount):
    def __init__(self, owner, initial_balance, credit_limit=1000):
        super().__init__(owner, initial_balance)
        self.credit_limit = credit_limit

    def withdraw(self, amount):
        self._validate_amount(amount)
        if amount > self.balance + self.credit_limit:
            raise ValueError("Credit limit exceeded")
        self.balance -= amount

    def __str__(self):
        return (
            f"Кредитный счёт владельца {self.owner}: "
            f"баланс = {self._balance}, лимит = {self.credit_limit}, "
            f"доступно = {self._balance + self.credit_limit}"
        )
