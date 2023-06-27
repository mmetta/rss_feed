import ast
import json
import os
import sqlite3

appData = os.getenv('APPDATA') + '\\LeitorRSS'
database = os.path.join(appData, 'config.db')


def create_db():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    # ## CREATE ## #
    cursor.execute("""
            CREATE TABLE configs (
                quant INTEGER NOT NULL,
                items TEXT NOT NULL,
                feeds TEXT NOT NULL
            );
            """)
    print('Tabela criada com sucesso.')

    items = ['G1 SP', 'ECONOMIA', 'POLITICA', 'REVISTA VEJA', 'INFO MONEY', 'CANALTECH', 'UOL TECNOLOGIA']
    feeds = [
        'https://g1.globo.com/rss/g1/sao-paulo/',
        'https://g1.globo.com/rss/g1/economia/',
        'https://g1.globo.com/rss/g1/politica/',
        'https://veja.abril.com.br/rss/',
        'https://www.infomoney.com.br/feed/',
        'https://canaltech.com.br/rss/',
        'http://rss.uol.com.br/feed/tecnologia.xml'
    ]
    quant = 5
    conn.execute("INSERT INTO configs (quant, items, feeds) VALUES (?, ?, ?)",
                 (quant, str(items), str(feeds)))
    conn.commit()
    conn.close()


def converter(campo):
    return ast.literal_eval(campo)


def select_all():
    # def project_settings():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM configs;
    """)
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    data = []
    for row in rows:
        data.append(dict(zip(columns, row)))
    json_data = json.dumps(data)
    obj = json.loads(json_data)
    obj[0]['items'] = eval(obj[0]['items'])
    obj[0]['feeds'] = eval(obj[0]['feeds'])
    return obj[0]


def update_data(data):
    # ## UPDATE ## #
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE configs SET quant = ?, items = ?, feeds = ?
    """, (data['quant'], str(data['items']), str(data['feeds'])))
    conn.commit()
    conn.close()
