from PySide6.QtWidgets import QMainWindow, QApplication
import sys
import GUI

STYLE_SHEET = ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE_SHEET)
    window = GUI.MainWindow()
    window.show()
    sys.exit(app.exec())