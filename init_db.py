import sqlite3

connection = sqlite3.connect('database.db')


# with open('schema.sql') as f:
#     connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO pegawai (nama, nip, kp_terakhir, kp_berikut) VALUES (?, ?, ?, ?)",
            ('John Doe', '198302012013061010', '2017-06-21','2021-06-21')
            )

cur.execute("INSERT INTO pegawai (nama, nip, kp_terakhir, kp_berikut) VALUES (?, ?, ?, ?)",
            ('Jane Doe', '198401012012022040', '2016-02-12','2020-02-12')
            )

cur.execute("INSERT INTO admin (username, password) VALUES (?, ?)",
('admin', 'admin')
)

connection.commit()
connection.close()