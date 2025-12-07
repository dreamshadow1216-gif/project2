class Account:
    """Basic bank account."""

    def __init__(self, username: str, balance: float = 0.0) -> None:
        """Initialize account with username and optional balance."""
        self.username = username
        self.balance = balance

    def get_name(self) -> str:
        """Return the account username."""
        return self.username

    def get_balance(self) -> float:
        """Return the current account balance."""
        return self.balance

    def set_balance(self, balance: float) -> None:
        """Set the account balance."""
        self.balance = balance

    def deposit(self, amount: float) -> bool:
        """Deposit a positive amount into the account."""
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount: float) -> bool:
        """Withdraw a positive amount if balance exists."""
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            return True
        return False

    def __str__(self) -> str:
        """Return a string of the account."""
        return f"Account: {self.username}, Balance: ${self.balance:.2f}"


class SavingAccount(Account):
    """Savings account with same logic."""

    def __init__(self, username: str, balance: float = 0.0) -> None:
        """Initialize savings account with username and optional balance."""
        super().__init__(username, balance)

    def deposit(self, amount: float) -> bool:
        """Deposit a positive amount into the savings account."""
