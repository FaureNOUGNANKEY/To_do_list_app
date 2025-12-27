from flask import Flask ,render_template , abort ,request ,flash ,redirect ,url_for
import sqlite3
from dotenv import load_dotenv
import os


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn 

def get_tache(id_tache):
    conn = get_db_connection()
    tache = conn.execute("SELECT * FROM TACHES WHERE id= ?",(id_tache,)).fetchone()
    conn.close()
    if tache is None:
        abort(404)
    return tache

load_dotenv()

app = Flask (__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY") # os.environ['SECRET_KEY]


@app.route('/')
def index():
    conn = get_db_connection()
    taches = conn.execute("SELECT * FROM TACHES").fetchall()
    conn.close
    return render_template('index.html' ,taches=taches)

@app.route('/<int:id_tache>')
def tache(id_tache):
    tache = get_tache(id_tache)
    return render_template('tache.html', tache=tache)

@app.route('/add',methods=('GET','POST'))
def add():
    if request.method == 'POST':
        titre = request.form['titre']
        description = request.form['description']
        statut = 'En cours'
        if not titre :
            flash('le titre est obligatoire !')
        else :
            conn = get_db_connection()
            conn.execute("INSERT INTO TACHES (titre,description,statut) values (?,?,?)",(titre,description,statut))
            conn.commit()
            conn.close()
            flash ("La tache a été ajouté avec succes")
            return redirect(url_for("index"))
    return render_template("add.html")

@app.route("/<int:id_tache>/update",methods=('POST','GET'))
def update(id_tache):
    tache = get_tache(id_tache)
    if request.method == "POST" :
        titre = request.form['titre']
        description = request.form['description']
        statut = request.form['statut'] 
        if not titre :
            flash ("Le titre est obligatoire ")
        else:
            with get_db_connection() as conn :
                conn.execute("UPDATE TACHES SET description=? ,statut=? WHERE id=?", (description,statut,id_tache))
                conn.execute ("UPDATE TACHES SET titre=? WHERE id=?",(titre,id_tache))
                conn.commit()
            conn.close()
            flash ('"{}" a été modifier avec succes'.format(tache['titre']))
            return redirect(url_for("index"))
    return render_template('update.html',tache=tache)

@app.route('/<int:id_tache>/delete',methods=("POST",))
def delete(id_tache):
    tache = get_tache(id_tache)
    conn = get_db_connection()
    conn.execute("DELETE FROM TACHES WHERE id=?",(id_tache,))
    conn.commit()
    conn.close()
    flash ('"{}" a été supprimer avec succes'.format(tache['titre']))
    return redirect(url_for('index'))

if __name__ == "__main__" :
    app.run(debug=True)