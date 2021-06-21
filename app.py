import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, session
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import requests


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    print(d2)
    return (d2 - d1).days

def telegram_bot_sendtext(bot_message):
   bot_token = '1851192408:AAGnbb4I2G8Z5T45-NvfdqtxaiVi-MFcaUE'
   bot_chatID = '956006928'
   send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

   response = requests.get(send_text)

   return response.json()

app = Flask(__name__)
app.secret_key = "jjaasasa"


@app.route('/')
def index():
    if session['loggedin'] == True:
        conn = get_db_connection()
        pegawais = conn.execute('SELECT * FROM pegawai').fetchall()
        today = datetime.today().strftime('%Y-%m-%d')
        counter=[]
        notif=1
        bell_notif=0
        x=0
        for i in pegawais:
            counter.append(days_between(today,i['kp_berikut']))
            if counter[x] <= 7 :
                bell_notif+=1
            if counter[x] <= 1 and counter[x] > -1 and notif == 1:
                message='Kenaikan Pangkat a.n '+ i['nama'] +' NIP : '+ i['nip'] +' tanggal '+ i['kp_berikut']
                telegram_bot_sendtext(message)
            if counter[x] <= -1:
                next_kp = datetime.strptime(i['kp_berikut'],'%Y-%m-%d').date() + relativedelta(years=4)
                conn = get_db_connection()
                conn.execute('UPDATE pegawai SET kp_terakhir = ?, kp_berikut = ?'
                            ' WHERE id = ?',
                            (i['kp_berikut'], next_kp, i['id']))
                conn.commit()
                conn.close()
            x+=1
        conn.close()
        return render_template('index.html',bell_notif=bell_notif,counter=counter,pegawais=pegawais)
    else:
        return redirect(url_for('login'))
   
@app.route('/create', methods=('GET', 'POST'))
def create():
    nama = request.form['nama']
    nip = request.form['nip']
    kp_terakhir = request.form['kp_terakhir']
    kp_berikut = request.form['kp_berikut']

    conn = get_db_connection()
    conn.execute('INSERT INTO pegawai (nama, nip, kp_terakhir, kp_berikut) VALUES (?, ?, ?, ?)',
                    (nama, nip, kp_terakhir, kp_berikut))
    conn.commit()
    conn.close()        
    return redirect(url_for('index'))

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    
    nama = request.form['edit_nama']
    nip = request.form['edit_nip']
    kp_terakhir = request.form['edit_kp_terakhir']
    kp_berikut = request.form['edit_kp_berikut']

    conn = get_db_connection()
    conn.execute('UPDATE pegawai SET nama = ?, nip = ?,kp_terakhir = ?, kp_berikut = ?'
                    ' WHERE id = ?',
                    (nama, nip, kp_terakhir, kp_berikut, id))
    conn.commit()
    conn.close()        
    return redirect(url_for('index'))

@app.route('/<int:id>/delete', methods=('GET', 'POST'))
def delete(id):
    
    conn = get_db_connection()
    conn.execute('DELETE from pegawai WHERE id = ?',(id,))
    conn.commit()
    conn.close()        
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    conn = get_db_connection()
    admins = conn.execute('SELECT * FROM admin').fetchall()
    conn.commit()
    conn.close()
    return render_template('admin.html',admins=admins)

@app.route('/create_admin', methods=('GET', 'POST'))
def create_admin():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    conn.execute('INSERT INTO admin (username, password) VALUES (?, ?)',
                    (username, password))
    conn.commit()
    conn.close()        
    return redirect(url_for('admin'))

@app.route('/<int:id>/edit_admin', methods=('GET', 'POST'))
def edit_admin(id):
    
    username = request.form['edit_username']
    password = request.form['edit_password']

    conn = get_db_connection()
    conn.execute('UPDATE admin SET username = ?, password = ?'
                    ' WHERE id = ?',
                    (username, password, id))
    conn.commit()
    conn.close()        
    return redirect(url_for('admin'))

@app.route('/<int:id>/delete_admin', methods=('GET', 'POST'))
def delete_admin(id):
    
    conn = get_db_connection()
    conn.execute('DELETE from admin WHERE id = ?',(id,))
    conn.commit()
    conn.close()        
    return redirect(url_for('admin'))

@app.route('/login_post', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    admins = conn.execute('SELECT * FROM admin WHERE username= ? AND password= ?',
    (username, password))

    # return admins

    if admins.fetchone():
        session['loggedin'] = True
        session['username'] = username
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        conn.commit()
        conn.close()
        login_ = "Gagal"
        return render_template('login.html',login_=login_)
    
    # return render_template('index.html',admins=admins)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session['loggedin'] = False
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)