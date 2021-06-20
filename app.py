import sqlite3
from flask import Flask, render_template
from datetime import datetime
import requests


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    print(d2)
    return abs((d2 - d1).days)

def telegram_bot_sendtext(bot_message):
   bot_token = '1851192408:AAGnbb4I2G8Z5T45-NvfdqtxaiVi-MFcaUE'
   bot_chatID = '956006928'
   send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

   response = requests.get(send_text)

   return response.json()

app = Flask(__name__)


@app.route('/')
def index():
    conn = get_db_connection()
    pegawais = conn.execute('SELECT * FROM pegawai').fetchall()
    list_peg = [list(i) for i in pegawais]
    today = datetime.today().strftime('%Y-%m-%d')
    counter=[]
    bell_notif=0
    x=0
    for i in pegawais:
        counter.append(days_between(today,i['kp_berikut']))
        if counter[x] <= 7 :
            bell_notif+=1
        if counter[x] <= 1 and counter[x] > -1 :
            message='Kenaikan Pangkat a.n '+ i['nama'] +' NIP : '+ i['nip']
            telegram_bot_sendtext(message)
        x+=1

    conn.close()
    return render_template('index.html',bell=bell_notif,counter=counter,pegawais=pegawais)