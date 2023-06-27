import os
from pathlib import Path

from PySide6.QtCore import QStringListModel, Qt
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QWidget, QHBoxLayout, QListView, QLabel, QVBoxLayout, QSpinBox, QPushButton
from feedparser import parse

from atual_path import local_path
from dialog_plus import DialogPlus
from sqlite_data import select_all, create_db, update_data

appData = os.getenv('APPDATA') + '\\LeitorRSS'
db_dir = os.path.isdir(appData)
if not db_dir:
    os.makedirs(os.path.join(os.environ['APPDATA'], 'LeitorRSS'))
    create_db()

config = select_all()
path = Path(local_path())


class Feeds(QWidget):
    def __init__(self):
        super().__init__()

        self.items = config['items']
        self.feeds = config['feeds']
        self.quant = config['quant']

        h_main = QHBoxLayout()
        vl_lay = QVBoxLayout()

        lbl_config = QLabel('Configurações')
        lbl_config.setStyleSheet('padding: 10; color: #0076ad;')
        lbl_config.setFont(QFont('Arial', 12, 700))
        lbl_config.setAlignment(Qt.AlignCenter)

        hl_qtd = QHBoxLayout()
        lbl_qtd = QLabel('Feeds por página: ')
        self.spin_quant = QSpinBox()
        self.spin_quant.setAlignment(Qt.AlignCenter)
        self.spin_quant.setValue(self.quant)
        self.spin_quant.setMinimum(1)
        self.spin_quant.setMaximum(10)
        self.spin_quant.valueChanged.connect(self.changed_quant)
        iqt = QIcon(f'{path}/icons/save.png')
        self.btn_qtd = QPushButton()
        self.btn_qtd.setStyleSheet('background: transparent; border: 0; padding: 0;')
        self.btn_qtd.setFixedSize(30, 30)
        self.btn_qtd.setIcon(iqt)
        self.btn_qtd.setDisabled(True)
        self.btn_qtd.clicked.connect(self.save_feed)
        hl_qtd.addWidget(lbl_qtd)
        hl_qtd.addWidget(self.spin_quant)
        hl_qtd.addWidget(self.btn_qtd)

        btn_refresh = QPushButton('Refresh')
        btn_refresh.setStyleSheet('background: #0076ad; color: white; font-weight: bold; padding: 10px;')
        btn_refresh.clicked.connect(self.refresh)

        hl_plus = QHBoxLayout()
        lbl_canal = QLabel('Canais de Feed')
        lbl_canal.setStyleSheet('padding: 10; color: #0076ad;')
        lbl_canal.setFont(QFont('Arial', 12, 700))

        ico = QIcon(f'{path}/icons/plus.png')
        plus_action = QPushButton()
        plus_action.setIcon(ico)
        plus_action.setStyleSheet('border: 0; background: transparent;')
        plus_action.clicked.connect(self.show_dialog_plus)
        minus = QIcon(f'{path}/icons/minus.png')
        minus_action = QPushButton()
        minus_action.setIcon(minus)
        minus_action.setStyleSheet('border: 0; background: transparent;')
        minus_action.clicked.connect(self.delete_feed)
        hl_plus.addWidget(minus_action)
        hl_plus.addWidget(lbl_canal)
        hl_plus.addWidget(plus_action)

        self.feed_list = QListView()
        self.feed_list.setFixedWidth(200)
        self.feed_list.setFont(QFont('Arial', 10, 700))
        self.feed_list.setStyleSheet('''QListView::item {
            padding-top: 4px; padding-bottom: 4px; color: #0076ad;
        }''')
        self.pop_list()
        self.feed_list.clicked.connect(self.feed_select)

        self.feed_content = QWebEngineView()
        feed = parse(self.feeds[0])
        self.views(feed)

        vl_lay.addWidget(lbl_config)
        vl_lay.addLayout(hl_qtd)
        vl_lay.addWidget(btn_refresh)
        vl_lay.addLayout(hl_plus)
        vl_lay.addWidget(self.feed_list)
        h_main.addLayout(vl_lay)
        h_main.addWidget(self.feed_content)
        self.setLayout(h_main)

        # self.feed_content.loadFinished.connect(self._on_load_finished)

    def _on_load_finished(self):
        try:
            self.feed_content.page().runJavaScript('document.querySelector("div")', 0, print('página OK!!'))
            # self.feed_content.page().runJavaScript('console.log("Page loaded successfully")')
        except Exception as e:
            print(' *** Deu erro ***', e)

    def show_dialog_plus(self):
        dg = DialogPlus()
        if dg.link_url != '' and dg.link_nome != '':
            self.feeds.append(dg.link_url)
            self.items.append(dg.link_nome)
            self.pop_list()
            index = len(self.feeds) - 1
            item = self.feed_list.model().index(index, 0)
            self.feed_list.setCurrentIndex(item)
            feed = parse(self.feeds[index])
            self.views(feed)
            self.btn_qtd.setDisabled(False)

    def delete_feed(self):
        selected = self.feed_list.currentIndex()
        index = selected.row()
        self.items.pop(index)
        self.feeds.pop(index)
        self.pop_list()
        feed = parse(self.feeds[0])
        self.views(feed)
        self.btn_qtd.setDisabled(False)

    def save_feed(self):
        new_conf = {
            'quant': self.quant,
            'items': self.items,
            'feeds': self.feeds
        }
        update_data(new_conf)
        self.btn_qtd.setDisabled(True)

    def refresh(self):
        self.feed_select()

    def changed_quant(self):
        quant = self.spin_quant.value()
        self.quant = quant
        if quant != config['quant']:
            self.btn_qtd.setDisabled(False)
        else:
            self.btn_qtd.setDisabled(True)

    def views(self, feed):
        html = '''
                    <html>
                    <style>
                        img {
                          max-width: calc(100% - 16px);
                          margin: 0 20px 10px 10px;
                        }
                        div {
                          text-align: justify;
                          font-family: Arial;
                          font-size: 12pt;
                          margin-bottom: 10px;
                          margin-right: 10px;
                        }
                        h2 {
                          color: white;
                          background: #0076ad;
                          padding: 10 10;
                        }
                    </style>
                    <body>
                '''

        for entry in feed.entries[:self.quant]:
            html += '<h2>{}</h2>'.format(entry.title)
            try:
                rows = str(entry.summary).split('\n')
                style = ''
                if len(rows) < 3:
                    style = ' style="min-height: 200px;"'
                for row in rows:
                    try:
                        html += '<div{}>{}</div>'.format(style, row)
                        html += '</body></html>'
                    except Exception as e:
                        print(' **** NÃO FOI POSSÍVEL LER O CONTEÚDO ****')
                        print(e)
            except Exception as e:
                # entry.content[0].value
                print(' **** NÃO FOI POSSÍVEL LER O CONTEÚDO ****')
                print(e)

        self.feed_content.setHtml(html)
        self.feed_content.show()

    def pop_list(self):
        model = QStringListModel()
        model.setStringList(self.items)
        self.feed_list.setModel(model)
        self.feed_list.setCurrentIndex(model.index(0))

    def feed_select(self):
        selected = self.feed_list.currentIndex()
        index = selected.row()
        feed = parse(self.feeds[index])
        self.views(feed)
