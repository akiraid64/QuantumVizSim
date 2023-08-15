# main.py
import sys
from PyQt5.QtWidgets import QApplication
from gui import QuantumApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuantumApp()
    sys.exit(app.exec_())
