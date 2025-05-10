import sys
from PyQt5.QtWidgets import QApplication
from interface import LockedInUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LockedInUI()
    window.show()
    sys.exit(app.exec_())
