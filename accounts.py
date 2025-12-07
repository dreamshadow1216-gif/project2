class Account:
    """Basic bank account."""

    def __init__(self, username: str, balance: float = 0.0) -> None:
        """Set username and starting balance."""
        self.username = username
        self.balance = balance

    def get_name(self) -> str:
        """Return the username."""
        return self.username

    def get_balance(self) -> float:
        """Return the current balance."""
        return self.balance

    def set_balance(self, balance: float) -> None:
        """Set a new balance."""
        self.balance = balance

    def deposit(self, amount: float) -> bool:
        """Add money to the account if amount is positive."""
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount: float) -> bool:
        """Take money from the account if enough balance."""
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            return True
        return False

    def __str__(self) -> str:
        """Return account info as a string."""
        return f"Account: {self.username}, Balance: ${self.balance:.2f}"


class SavingAccount(Account):
    """Savings account (like Account)."""

    def __init__(self, username: str, balance: float = 0.0) -> None:
        """Set username and starting balance."""
        super().__init__(username, balance)

    def deposit(self, amount: float) -> bool:
        """Add money to savings account."""
        return super().deposit(amount)
