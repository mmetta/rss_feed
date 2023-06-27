from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow

from atual_path import local_path
from feeds import Feeds

path = Path(local_path())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Leitor de Feeds RSS')
        self.setWindowIcon(QIcon(f'{path}/icons/rss.png'))
        self.setMinimumSize(1000, 600)

        self.myFeeds = Feeds()
        self.setCentralWidget(self.myFeeds)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
