import sys
import ctypes
from PyQt6.QtWidgets import QApplication
from controller import TaskController

if sys.platform.startswith("win"):
    ctypes.windll.user32.ShowWindow(
        ctypes.windll.kernel32.GetConsoleWindow(), 0
    )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = TaskController()
    controller.view.show()
    sys.exit(app.exec())