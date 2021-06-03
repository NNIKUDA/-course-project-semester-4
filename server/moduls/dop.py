"""

This program looks for information every day at 6 o'clock and adds it to the database/

"""

import sqlite3 as sql
import time
import requests
from bs4 import BeautifulSoup


URL='https://www.bps-sberbank.by'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
DATA_BASE=r'..\database\valuta.db'

if __name__=='__main__':
    try:
        con = sql.connect(DATA_BASE)
    except Exception as e:
        with open(r'..\logs\log_dop.txt', 'a') as w:
            w.write(f'''{time.strftime("%H:%M: %d %m %Y", time.gmtime(time.time()))} 
                    Fatal Error  database connection {e}\n''')
        exit(1)
    with con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS "valuta"(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                date VARCHAR NOT NULL,
                usd_buy VARCHAR NOT NULL,
                usd_sell VARCHAR NOT NULL,
                eur_buy VARCHAR NOT NULL,
                eur_sell VARCHAR NOT NULL,
                rub_buy VARCHAR NOT NULL,
                rub_sell VARCHAR NOT NULL
            );  
        """)

    while True:
        t = time.localtime(time.time())
        if t.tm_min==0 or t.tm_min==1:
            try:
                answer=requests.get(URL, headers=HEADERS)
                if answer.status_code==200:
                    html_doc=answer.text
                    parser=BeautifulSoup(html_doc, 'html.parser')
                    valuts = []
                    v=parser.findAll('div', class_='BlockCurrencyExchangeRates__rate-item_buy-rate')
                    for i in v:
                        valuts.append(i.contents.pop())
                    v = parser.findAll('div', class_='BlockCurrencyExchangeRates__rate-item_sell-rate')
                    for i in v:
                        valuts.append(i.contents.pop())
                    with con:
                        date=time.strftime('%H:%M %d %m %Y', time.gmtime(time.time()))
                        con.execute(f"""
                        INSERT INTO "valuta"
                        ("id", "date", "usd_buy", "usd_sell", "eur_buy",
                                       "eur_sell", "rub_buy","rub_sell") VALUES
                        ( NULL ,'{date}','{valuts[0]}','{valuts[3]}','{valuts[1]}',
                                         '{valuts[4]}','{valuts[2]}','{valuts[5]}');
                        """)

                    time.sleep(3590)
                else:
                    with open(r'..\logs\log_dop.txt', 'a') as w:
                        w.write(f'''{time.strftime("%H:%M: %d %m %Y",time.gmtime(time.time()))}
                                    Error get code {answer.status_code}\n
                            ''')
                    time.sleep(10)
            except Exception as e:
                with open(r'..\logs\log_dop.txt', 'a') as w:
                    w.write(f'{time.strftime("%H:%M: %d %m %Y",time.gmtime(time.time()))} Error connection {e}\n')
                time.sleep(10)

        else:
            time.sleep(3590)
