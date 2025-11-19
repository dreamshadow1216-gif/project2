class Account:

    def __init__(self, username: str, balance: float = 0.0) -> None:
        self.username = username
        self.balance = balance

    def get_name(self) -> str:
        return self.username

    def get_balance(self) -> float:
        return self.balance

    def set_balance(self, balance: float) -> None:
        self.balance = balance

    def deposit(self, amount: float) -> bool:
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount: float) -> bool:
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            return True
        return False

    def __str__(self) -> str:
        return f"Account: {self.username}, Balance: ${self.balance:.2f}"


class SavingAccount(Account):

    def __init__(self, username: str, balance: float = 0.0) -> None:
        super().__init__(username, balance)

    def deposit(self, amount: float) -> bool:
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount: float) -> bool:
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            return True
        return False

    def __str__(self) -> str:
        return f"Savings Account: {self.username}, Balance: ${self.balance:.2f}"