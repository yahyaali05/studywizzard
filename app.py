import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
import db

# Flask-Anwendung initialisieren
app = Flask(__name__)

# Konfiguration für die Flask-App, insbesondere für den Pfad zur SQLite-Datenbank
app.config.from_mapping(
    SECRET_KEY='geheimschluessel',  # Geheimschlüssel für die Session (nur für Entwicklungsumgebung)
    DATABASE=os.path.join(app.instance_path, 'studywizards.db')  # SQLite-Datenbankpfad
)

# Stellt sicher, dass die DB-Verbindung am Ende der Anfrage geschlossen wird
app.teardown_appcontext(db.close_db_con)

@app.route('/profile')
def profile():
    if 'username' in session:
        return f'Willkommen, {session["username"]}!'
    return redirect(url_for('login'))  # Umleiten zur Login-Seite, wenn nicht eingeloggt

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_id = db.check_user_credentials(username, password)
        if user_id:
            session['username'] = username
            session['user_id'] = user_id
            flash('Erfolgreich eingeloggt!', 'success')
            return redirect(url_for('index'))
        flash('Benutzername oder Passwort sind falsch!', 'error')
    return render_template('login.html')

@app.route('/insert/sample')
def run_insert_sample():
    if 'user_id' in session:  # Stelle sicher, dass der Benutzer eingeloggt ist
        user_id = session['user_id']
        db.insert_sample(user_id)  # Beispiel-Karteikarten in die Datenbank einfügen
        flash('Beispiel-Karteikarten wurden erfolgreich hinzugefügt!', 'success')
    return redirect(url_for('view_flashcards'))  # Nach dem Einfügen weiter zu den Karteikarten

@app.route('/view_flashcards')
def view_flashcards():
    if 'user_id' in session:
        user_id = session['user_id']
        flashcards = get_flashcards_for_user(user_id)  # Karteikarten aus der DB holen
        return render_template('view_flashcards.html', flashcards=flashcards)
    return redirect(url_for('login'))  # Wenn der Benutzer nicht eingeloggt ist, zurück zur Login-Seite

    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    flashcards = db.get_flashcards_for_user(user_id)
    return render_template('view_flashcards.html', flashcards=flashcards)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if db.username_exists(username):
            flash('Benutzername ist bereits vergeben!', 'error')
            return redirect(url_for('register'))
        db.register_user(username, password)
        flash('Erfolgreich registriert!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

def init_db_command():
  #  """Initialisiert die Datenbank und erstellt die Tabellen."""
    db.init_db()
    print("Datenbank erfolgreich initialisiert!")

if __name__ == '__main__':
    app.run(debug=True)
