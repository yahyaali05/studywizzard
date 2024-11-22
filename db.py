import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, g

# Holen der Datenbankverbindung
def get_db_con():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row  # Um auf Spalten mit Namen zuzugreifen
    return g.db

# Schließen der Verbindung nach der Anfrage
def close_db_con(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Registrierung eines neuen Benutzers
def register_user(username, password):
    db_con = get_db_con()
    
    if username_exists(username):  # Verhindert doppelte Benutzernamen
        return False

    hashed_password = generate_password_hash(password)  # Passwort hashen
    db_con.execute(''' 
        INSERT INTO users (username, password)
        VALUES (?, ?)
    ''', (username, hashed_password))
    db_con.commit()
    return True

# Überprüfen, ob der Benutzername existiert
def username_exists(username):
    db_con = get_db_con()
    result = db_con.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
    return result is not None

# Überprüfen der Benutzeranmeldeinformationen
def check_user_credentials(username, password):
    db_con = get_db_con()
    user = db_con.execute('SELECT id, password FROM users WHERE username = ?', (username,)).fetchone()
    if user and check_password_hash(user['password'], password):
        return user['id']
    return None

def get_flashcards_for_user(user_id):
    db_con = get_db_con()
    flashcards = db_con.execute('''
        SELECT subject, question, answer FROM flashcards WHERE user_id = ?
    ''', (user_id,)).fetchall()
    return flashcards
def insert_sample(user_id):
    db_con = get_db_con()
    
    # Überprüfen, ob der Benutzer bereits Karteikarten hat
    existing_flashcards = db_con.execute('''SELECT id FROM flashcards WHERE user_id = ?''', (user_id,)).fetchall()
    if existing_flashcards:
        return  # Wenn der Benutzer bereits Karteikarten hat, tue nichts

    # Karteikarten für Deutsch, Mathe und Englisch einfügen
    flashcards_data = [
        ('Deutsch', 'Was ist der Hauptstadt von Deutschland?', 'Berlin'),
        ('Deutsch', 'Was ist der Plural von "Kind"?', 'Kinder'),
        ('Deutsch', 'Wie viele Bundesländer hat Deutschland?', '16'),
        
        ('Mathe', 'Was ist 2 + 2?', '4'),
        ('Mathe', 'Was ist 5 * 6?', '30'),
        ('Mathe', 'Was ist der Wert von Pi?', '3.14159'),
        
        ('Englisch', 'Wie sagt man "Hallo" auf Englisch?', 'Hello'),
        ('Englisch', 'Was ist der englische Begriff für "Apfel"?', 'Apple'),
        ('Englisch', 'Was bedeutet "I am hungry"?', 'Ich habe Hunger')
    ]
    
    # Karteikarten in die Datenbank einfügen
    for subject, question, answer in flashcards_data:
        db_con.execute(''' 
            INSERT INTO flashcards (user_id, subject, question, answer) 
            VALUES (?, ?, ?, ?)
        ''', (user_id, subject, question, answer))
    
    db_con.commit()



    # Überprüfen, ob 'user1' bereits existiert
    if not username_exists('user1'):
        db_con.execute(''' 
            INSERT INTO users (username, password) VALUES ('user1', 'password123')
        ''')
    if not username_exists('user2'):
        db_con.execute(''' 
            INSERT INTO users (username, password) VALUES ('user2', 'password456')
        ''')

    db_con.commit()

    # Flashcards für Benutzer 1 einfügen (falls sie nicht existieren)
    db_con.execute(''' 
        INSERT INTO flashcards (user_id, subject, question, answer)
        VALUES (1, 'Math', 'Was ist 2 + 2?', '4')
    ''')
    db_con.execute(''' 
        INSERT INTO flashcards (user_id, subject, question, answer)
        VALUES (1, 'History', 'Wer war Napoleon?', 'Ein französischer Kaiser')
    ''')

    db_con.commit()

# Initialisiert die Datenbank und erstellt die Tabellen
def init_db():
    db_con = get_db_con()
    with current_app.open_resource('sql/create_tables.sql', mode='r') as f:
        db_con.executescript(f.read())  # Führt das SQL-Skript aus, um Tabellen zu erstellen
    db_con.commit()
