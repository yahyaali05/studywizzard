import os
import sqlite3
import db
from db import (
    get_db_con, 
    get_flashcards_for_user, 
    username_exists, 
    register_user
)
from flask import Flask, render_template, request, redirect, url_for, session, flash


app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY='geheimschluessel',  
    DATABASE=os.path.join(app.instance_path, 'studywizards.db')  
)

app.teardown_appcontext(db.close_db_con)

@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    if user_id is None:
        flash('Du musst eingeloggt sein, um dein Profil zu sehen.', 'danger')
        return redirect(url_for('login'))


    user_data = db.get_user_data(user_id)
    if user_data is None:
        flash('Benutzerdaten konnten nicht geladen werden.', 'danger')
        return redirect(url_for('index'))
    
    return render_template('profile.html', user=user_data)

@app.route('/logout')
def logout():
    session.clear()  
    flash('Du hast dich erfolgreich ausgeloggt!', 'success')
    return redirect(url_for('login'))

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
            flash('Erfolgreich eingeloggt!', 'success')
            session['user_id'] = user_id
            return redirect(url_for('index'))
        else:
            flash('Ungültige Anmeldedaten. Versuche es erneut.', 'danger')
    
    return render_template('login.html')

@app.route('/insert/sample')
def run_insert_sample():
    if 'user_id' in session:
        user_id = session['user_id']
        db.insert_sample_for_user(user_id)
        flash('Beispiel-Karteikarten wurden erfolgreich hinzugefügt!', 'success')
        return render_template('insert_sample.html')
    flash('Du musst eingeloggt sein, um diese Aktion auszuführen.', 'danger')
    return redirect(url_for('login'))

@app.route('/view_flashcards')
def view_flashcards():
    user_id = session.get('user_id')
    if user_id is None:
        flash('Du musst eingeloggt sein, um deine Karteikarten zu sehen.', 'danger')
        return redirect(url_for('login'))
    
    flashcards = db.get_flashcards_for_user(user_id)
    return render_template('view_flashcards.html', flashcards=flashcards)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            register_user(username, password)
            flash('Registrierung erfolgreich! Bitte logge dich ein.', 'success')
            return redirect(url_for('login'))
        except ValueError as e:
            flash(str(e), 'danger')
    return render_template('register.html')

# Route für das Erstellen einer neuen Karteikarte
@app.route('/create_flashcard', methods=['GET', 'POST'])
def create_flashcard():
    if 'user_id' not in session:
        flash('Du musst eingeloggt sein, um eine Karteikarte zu erstellen.', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        subject = request.form['subject']
        question = request.form['question']
        answer = request.form['answer']
        
        # Karteikarte in die Datenbank einfügen
        user_id = session['user_id']
        db.create_flashcard_for_user(user_id, subject, question, answer)
        flash('Karteikarte erfolgreich erstellt!', 'success')
        return redirect(url_for('view_flashcards'))
    
    return render_template('create_flashcard.html')

# Route für das Löschen einer Karteikarte
@app.route('/delete_flashcard/<int:flashcard_id>', methods=['POST'])
def delete_flashcard(flashcard_id):
    user_id = session.get('user_id')
    if user_id is None:
        flash('Du musst eingeloggt sein, um eine Karteikarte zu löschen.', 'danger')
        return redirect(url_for('login'))
    
    db.delete_flashcard(flashcard_id, user_id)
    flash('Karteikarte erfolgreich gelöscht!', 'success')
    return redirect(url_for('view_flashcards'))

# Funktion, um die Datenbank zu initialisieren
def init_db_command():
    db.init_db()
    print("Datenbank erfolgreich initialisiert!")
<<<<<<< HEAD
    
# Starte die Flask-App
if __name__ == '__main__':
=======

if __name__ == '__main__': 
>>>>>>> d1cce778b1645af1a0c09a1c3a2208f599383dac
    app.run(debug=True)
