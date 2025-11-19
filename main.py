import sys
from PyQt6.QtWidgets import QApplication
from gui import AccountGUI

def main() -> None:
    app = QApplication(sys.argv)
    window = AccountGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()