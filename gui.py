import csv
import os
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox,
    QStackedWidget, QInputDialog, QListWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from accounts import Account, SavingAccount

class AccountGUI(QWidget):
    """GUI for managing bank accounts with login, signup, deposit, and withdrawal."""

    def __init__(self) -> None:
        """Initialize the main GUI and screens."""
        super().__init__()
        self.setWindowTitle("Bank Account Manager")
        self.setFixedSize(300, 400)
        self.account = None
        self.filename = "accounts.csv"
        self.users_data = {}
        self.load_users_data()

        self.stack = QStackedWidget()
        self.login_screen = self.build_login_screen()
        self.account_summary_screen = self.build_account_summary_screen()
        self.signup_screen = self.build_signup_screen()

        self.stack.addWidget(self.login_screen)
        self.stack.addWidget(self.account_summary_screen)
        self.stack.addWidget(self.signup_screen)

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)

    def load_users_data(self) -> None:
        """Load users from CSV file into memory."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, mode="r", newline="") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row:
                            username, password, acc_type, balance = row
                            self.users_data[username] = {
                                "password": password,
                                "acc_type": acc_type,
                                "balance": float(balance)
                            }
            except Exception as e:
                self.show_error(f"Error loading users data: {e}")

    def build_login_screen(self) -> QWidget:
        """Create the login screen widget."""
        screen = QWidget()
        layout = QVBoxLayout()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_btn = QPushButton("Login")
        self.signup_btn = QPushButton("Sign Up")
        self.login_btn.clicked.connect(self.login)
        self.signup_btn.clicked.connect(self.go_to_signup)

        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.signup_btn)
        screen.setLayout(layout)
        return screen

    def build_signup_screen(self) -> QWidget:
        """Create the signup screen widget."""
        screen = QWidget()
        layout = QVBoxLayout()
        self.new_username_input = QLineEdit()
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_balance_input = QLineEdit()
        self.create_account_btn = QPushButton("Create Account")
        self.create_account_btn.clicked.connect(self.create_account)

        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.new_username_input)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.new_password_input)
        layout.addWidget(QLabel("Initial Balance:"))
        layout.addWidget(self.new_balance_input)
        layout.addWidget(self.create_account_btn)
        screen.setLayout(layout)
        return screen

    def build_account_summary_screen(self) -> QWidget:
        """Create the account summary screen widget."""
        screen = QWidget()
        layout = QVBoxLayout()
        self.balance_label = QLabel("Balance: $0.00")
        self.deposit_btn = QPushButton("Deposit")
        self.withdraw_btn = QPushButton("Withdraw")
        self.logout_btn = QPushButton("Logout")
        self.deposit_btn.clicked.connect(self.deposit)
        self.withdraw_btn.clicked.connect(self.withdraw)
        self.logout_btn.clicked.connect(self.logout)
        self.transaction_log = QListWidget()
        self.transaction_log.setFixedHeight(50)
        self.transaction_log.setFont(QFont("Arial", 8))

        layout.addWidget(self.balance_label)
        layout.addWidget(self.deposit_btn)
        layout.addWidget(self.withdraw_btn)
        layout.addWidget(self.logout_btn)
        layout.addWidget(QLabel("Transaction Log:"))
        layout.addWidget(self.transaction_log)
        screen.setLayout(layout)
        return screen

    def login(self) -> None:
        """Authenticate user and open account summary screen."""
        username = self.username_input.text()
        password = self.password_input.text()

        if username in self.users_data and self.users_data[username]["password"] == password:
            acc_type = self.users_data[username]["acc_type"]
            balance = self.users_data[username]["balance"]
            if acc_type == "Account":
                self.account = Account(username, balance)
            elif acc_type == "SavingAccount":
                self.account = SavingAccount(username, balance)
            self.balance_label.setText(f"Balance: ${self.account.get_balance():.2f}")
            self.stack.setCurrentWidget(self.account_summary_screen)
        else:
            self.show_error("Invalid username or password.")

    def go_to_signup(self) -> None:
        """Switch to the signup screen."""
        self.stack.setCurrentWidget(self.signup_screen)

    def create_account(self) -> None:
        """Create a new account from signup inputs."""
        username = self.new_username_input.text()
        password = self.new_password_input.text()
        try:
            balance = float(self.new_balance_input.text())
        except ValueError:
            self.show_error("Initial balance must be a number or 0.")
            return

        if not username or not password:
            self.show_error("Username and password cannot be empty.")
            return

        if username in self.users_data:
            self.show_error("Username already exists. Please choose another.")
            return

        self.users_data[username] = {"password": password, "acc_type": "Account", "balance": balance}
        self.save_users_data()
        self.show_message("Account created successfully! Please log in.")
        self.stack.setCurrentWidget(self.login_screen)

    def save_users_data(self) -> None:
        """Save all user data to CSV file."""
        try:
            with open(self.filename, mode="w", newline="") as file:
                writer = csv.writer(file)
                for username, data in self.users_data.items():
                    writer.writerow([username, data["password"], data["acc_type"], data["balance"]])
        except Exception as e:
            self.show_error(f"Error saving user data: {e}")

    def deposit(self) -> None:
        """Prompt for deposit amount and update account balance."""
        amount = self.prompt_for_amount("Deposit Amount")
        if amount is None:
            return
        if self.account.deposit(amount):
            self.balance_label.setText(f"Balance: ${self.account.get_balance():.2f}")
            self.transaction_log.addItem(f"Deposited: ${amount:.2f}")
            self.users_data[self.account.get_name()]["balance"] = self.account.get_balance()
            self.save_users_data()
        else:
            self.show_error("Invalid deposit amount.")

    def withdraw(self) -> None:
        """Prompt for withdrawal amount and update account balance."""
        amount = self.prompt_for_amount("Withdrawal Amount")
        if amount is None:
            return
        if self.account.withdraw(amount):
            self.balance_label.setText(f"Balance: ${self.account.get_balance():.2f}")
            self.transaction_log.addItem(f"Withdrew: ${amount:.2f}")
            self.users_data[self.account.get_name()]["balance"] = self.account.get_balance()
            self.save_users_data()
        else:
            self.show_error("Exceeds Balance.")

    def prompt_for_amount(self, action: str) -> float:
        """Prompt the user for amount and return it."""
        text, ok = QInputDialog.getText(self, action, f"Enter {action.lower()}:")
        if ok:
            try:
                amount = float(text)
                return amount
            except ValueError:
                self.show_error(f"{action} must be a valid number.")
        return None

    def logout(self) -> None:
        """Log out current user and return to login screen."""
        self.account = None
        self.transaction_log.clear()
        self.stack.setCurrentWidget(self.login_screen)

    def show_error(self, message: str) -> None:
        """Display an error message box."""
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.exec()

    def show_message(self, message: str) -> None:
        """Display an informational message box."""
        msg = QMessageBox()
        msg.setWindowTitle("Message")
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()
