"""

    Imitation of a rast server to get the current exchange rate.

"""

import uvicorn
import json
import sqlite3 as sql
import time
from fastapi import FastAPI


DATA_BASE=r'database\valuta.db'
PORT=9090
URL='http://127.0.0.1:9090'


#  Сonnecting to the database and starting the server.
app=FastAPI()
if __name__=='__main__':
    uvicorn.run('server:app', port=PORT)

@app.get("/help")
def help():
        return json.dumps({'help' : '''This is a web service of exchange rates. Supported commands:
                    /fresh_currency    Last information about currency
                    /fresh_currency_valuta    where valuta=usd or eur or rub Last information about valuta   
                '''})


@app.get("/fresh_currency")
def fresh_currency():
    try:
        con = sql.connect(DATA_BASE)
        cur = con.cursor()
        with con:
            cur.execute('''SELECT MAX("id"),"date", "usd_buy", "usd_sell", "eur_buy", "eur_sell","rub_buy", "rub_sell"
                           FROM "valuta"
                            ''')
            data = cur.fetchone()
        return json.dumps({'date':data[1], 'usd_buy':data[2], 'usd_sell':data[3], 'eur_buy,':data[4],
                            'eur_sell':data[5], 'rub_buy':data[6], 'rub_sell':data[7]})
    except Exception as e:
        with open(r'logs\log_server.txt', 'a') as w:
            w.write(f'{time.strftime("%H:%M: %d %m %Y", time.gmtime(time.time()))} Error {e}\n')
        return json.dumps({'error': 'code 500'})
@app.get("/fresh_currency_rub")
def fresh_currency_rub():
    try:
        con = sql.connect(DATA_BASE)
        cur=con.cursor()
        with con:
            cur.execute('''SELECT MAX("id"),"date", "rub_buy", "rub_sell"
                           FROM "valuta"
                            ''')
            data=cur.fetchone()
        return json.dumps({'date':data[1], 'rub_buy':data[2], 'rub_sell':data[3]})
    except Exception as e:
        with open(r'logs\log_server.txt', 'a') as w:
            w.write(f'{time.strftime("%H:%M: %d %m %Y", time.gmtime(time.time()))} Error {e}\n')
        return json.dumps({'error': 'code 500'})
@app.get("/fresh_currency_eur")
def fresh_currency_eur():
    try:
        con = sql.connect(DATA_BASE)
        cur = con.cursor()
        with con:
            cur.execute('''SELECT MAX("id"),"date", "eur_buy", "eur_sell"
                           FROM "valuta"
                            ''')
            data = cur.fetchone()
        return json.dumps({'date':data[1], 'eur_buy,':data[2], 'eur_sell':data[3]})
    except Exception as e:
        with open(r'logs\log_server.txt', 'a') as w:
            w.write(f'{time.strftime("%H:%M: %d %m %Y", time.gmtime(time.time()))} Error {e}\n')
        return json.dumps({'error': 'code 500'})
@app.get("/fresh_currency_usd")
def fresh_currency_usd():
    try:
        con = sql.connect(DATA_BASE)
        cur = con.cursor()
        with con:
            cur.execute('''SELECT MAX("id"),"date", "usd_buy", "usd_sell"
                           FROM "valuta"
                            ''')
            data = cur.fetchone()
        return json.dumps({'date':data[1], 'usd_buy':data[2], 'usd_sell':data[3]})
    except Exception as e:
        with open(r'logs\log_server.txt', 'a') as w:
            w.write(f'{time.strftime("%H:%M: %d %m %Y", time.gmtime(time.time()))} Error {e}\n')
        return json.dumps({'error': 'code 500'})

