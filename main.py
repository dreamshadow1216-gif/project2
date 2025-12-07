import sys
from PyQt6.QtWidgets import QApplication
from gui import AccountGUI

def main() -> None:
    """Start the bank account GUI application."""
    app = QApplication(sys.argv)
    window = AccountGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
