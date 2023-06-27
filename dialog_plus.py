from pathlib import Path

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton

from atual_path import local_path

path = Path(local_path())


class DialogPlus:

    def __init__(self):
        super().__init__()

        self.dialog_plus = QDialog()
        self.dialog_plus.setWindowTitle('Novo Feed Rss')
        # ico = str(Path(base_path, 'rss.png'))
        self.dialog_plus.setWindowIcon(QIcon(f'{path}/icons/rss.png'))
        self.dialog_plus.setFixedSize(QSize(440, 120))
        self.link_nome = ''
        self.link_url = ''

        d_lay = QVBoxLayout(self.dialog_plus)
        d_lay.setAlignment(Qt.AlignCenter)

        layH_2 = QHBoxLayout()
        lbl_nome = QLabel('Nome: ')
        lbl_nome.setFont(QFont('Arial', 12, 700))
        layH_2.addWidget(lbl_nome)

        self.edt_nome = QLineEdit()
        self.edt_nome.setFont(QFont('Arial', 10, 400))
        self.edt_nome.setMaximumWidth(340)
        # self.edt_nome.setStyleSheet(style_qline_edit())
        layH_2.addWidget(self.edt_nome)

        layH_3 = QHBoxLayout()
        lbl_url = QLabel('URL: ')
        lbl_url.setFont(QFont('Arial', 12, 700))
        layH_3.addWidget(lbl_url)

        self.edt_url = QLineEdit()
        self.edt_url.setFont(QFont('Arial', 10, 400))
        self.edt_url.setMaximumWidth(340)
        # self.edt_url.setStyleSheet(style_qline_edit())
        layH_3.addWidget(self.edt_url)

        layH_4 = QHBoxLayout()
        btn_cancelar = QPushButton('Cancelar')
        btn_cancelar.setFixedSize(QSize(100, 30))
        btn_cancelar.setStyleSheet('background: #fde;')
        btn_cancelar.clicked.connect(self.close)
        layH_4.addWidget(btn_cancelar)

        btn_inserir = QPushButton('Adicionar')
        btn_inserir.setFixedSize(QSize(100, 30))
        btn_inserir.clicked.connect(self.about_close)
        layH_4.addWidget(btn_inserir)

        d_lay.addLayout(layH_2)
        d_lay.addLayout(layH_3)
        d_lay.addLayout(layH_4)

        self.dialog_plus.exec()

    def close(self):
        self.link_nome = ''
        self.link_url = ''
        self.dialog_plus.close()

    def about_close(self):
        self.link_nome = self.edt_nome.text().upper()
        self.link_url = self.edt_url.text()
        self.dialog_plus.close()
