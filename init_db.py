import sqlite3

connection = sqlite3.connect('database.db')

with open ('schema.sql') as f :
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute(" INSERT INTO TACHES (titre,description,statut) VALUES(?,?,?)",('ranger chambre','ranger ma chambre','Terminee'))

connection.commit()
connection.close
