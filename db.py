import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, g
import os

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

# Lade und führe eine SQL-Datei aus
def execute_sql_file(filename):
    try:
        db_con = get_db_con()
        # Die SQL-Datei aus dem 'sql' Ordner lesen
        with open(os.path.join(current_app.root_path, 'sql', filename), 'r') as f:
            sql = f.read()
            db_con.executescript(sql)
        db_con.commit()
    except sqlite3.DatabaseError as e:
        # Fehlerbehandlung bei der Ausführung von SQL-Dateien
        print(f"Fehler beim Ausführen der SQL-Datei {filename}: {e}")

# Initialisiert die Datenbank und erstellt die Tabellen
def init_db():
    execute_sql_file('create_tables.sql')  # Erstellt die Tabellen, falls sie nicht existieren

# Löscht alle Tabellen (für Neustart)
def drop_tables():
    execute_sql_file('drop_tables.sql')  # Löscht alle Tabellen

# Beispiel-Daten einfügen (für alle Benutzer)
def insert_sample():
    try:
        db_con = get_db_con()
        # Überprüfen, ob bereits Benutzer existieren
        if db_con.execute('SELECT COUNT(*) FROM users').fetchone()[0] > 0:
            print("Benutzer existieren bereits, überspringe Insert-Beispiel-Daten.")
            return
        execute_sql_file('insert_sample.sql')  # Beispiel-Daten einfügen
    except sqlite3.DatabaseError as e:
        # Fehlerbehandlung bei Einfügen von Beispieldaten
        print(f"Fehler beim Einfügen der Beispiel-Daten: {e}")

# Beispiel-Daten für einen spezifischen Benutzer einfügen
def insert_sample_for_user(user_id):
    try:
        db_con = get_db_con()
        # Überprüfen, ob der Benutzer bereits Karteikarten hat
        existing_flashcards = db_con.execute('''SELECT id FROM flashcards WHERE user_id = ?''', (user_id,)).fetchall()
        if existing_flashcards:
            return  # Wenn der Benutzer bereits Karteikarten hat, tue nichts

        # Beispiel-Karteikarten einfügen
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
    except sqlite3.DatabaseError as e:
        # Fehlerbehandlung beim Einfügen der Karteikarten
        print(f"Fehler beim Einfügen der Karteikarten: {e}")

# Erstelle eine neue Karteikarte für den Benutzer
def create_flashcard_for_user(user_id, subject, question, answer):
    try:
        db_con = get_db_con()
        # Karteikarte in die Datenbank einfügen
        db_con.execute(''' 
            INSERT INTO flashcards (user_id, subject, question, answer)
            VALUES (?, ?, ?, ?)
        ''', (user_id, subject, question, answer))

        db_con.commit()
    except sqlite3.DatabaseError as e:
        # Fehlerbehandlung beim Erstellen einer neuen Karteikarte
        print(f"Fehler beim Erstellen der Karteikarte: {e}")

# Überprüfen der Benutzeranmeldeinformationen
def check_user_credentials(username, password):
    try:
        db_con = get_db_con()
        user = db_con.execute('SELECT id, password FROM users WHERE username = ?', (username,)).fetchone()
        if user and check_password_hash(user['password'], password):
            return user['id']
        return None
    except sqlite3.DatabaseError as e:
        # Fehlerbehandlung bei der Benutzerüberprüfung
        print(f"Fehler bei der Überprüfung der Benutzeranmeldeinformationen: {e}")
        return None

# Abfragen der Karteikarten für den angegebenen Benutzer
def get_flashcards_for_user(user_id):
    try:
        db_con = get_db_con()

        # Ändere die SQL-Abfrage, um auch die ID der Karteikarten abzurufen
        flashcards = db_con.execute(''' 
            SELECT id, subject, question, answer FROM flashcards WHERE user_id = ? 
        ''', (user_id,)).fetchall()

        return flashcards
    except sqlite3.DatabaseError as e:
        # Fehlerbehandlung bei der Abfrage der Karteikarten
        print(f"Fehler beim Abrufen der Karteikarten: {e}")
        return []

# Lösche eine Karteikarte aus der Datenbank
def delete_flashcard(flashcard_id, user_id):
    try:
        db_con = get_db_con()
        # Überprüfe, ob der Benutzer der Besitzer der Karteikarte ist
        db_con.execute(''' 
            DELETE FROM flashcards WHERE id = ? AND user_id = ?
        ''', (flashcard_id, user_id))
        db_con.commit()
    except sqlite3.DatabaseError as e:
        print(f"Fehler beim Löschen der Karteikarte: {e}")

def get_user_data(user_id):
    try:
        db_con = get_db_con()
        # Nur den Benutzernamen abfragen
        user = db_con.execute('''SELECT id, username FROM users WHERE id = ?''', (user_id,)).fetchone()
        if user:
            return user
        return None
    except sqlite3.DatabaseError as e:
        print(f"Fehler beim Abrufen der Benutzerdaten: {e}")
        return None

# Überprüft, ob ein Benutzername bereits in der Datenbank existiert
def username_exists(username):
    try:
        db_con = get_db_con()
        # Überprüft, ob der Benutzername bereits existiert
        result = db_con.execute('''SELECT 1 FROM users WHERE username = ? LIMIT 1''', (username,)).fetchone()
        return result is not None
    except sqlite3.DatabaseError as e:
        print(f"Fehler bei der Überprüfung des Benutzernamens: {e}")
        return False

def register_user(username, password):
    try:
        db_con = get_db_con()

        # Überprüfen, ob der Benutzername bereits existiert
        if username_exists(username):
            raise ValueError("Der Benutzername existiert bereits.")

        # Passwort hashen und Benutzer hinzufügen
        hashed_password = generate_password_hash(password)
        db_con.execute('''
            INSERT INTO users (username, password) 
            VALUES (?, ?)
        ''', (username, hashed_password))
        db_con.commit()
        print(f"Benutzer {username} erfolgreich registriert.")
    except sqlite3.DatabaseError as e:
        print(f"Fehler bei der Registrierung des Benutzers: {e}")
    except ValueError as ve:
        print(f"Registrierungsfehler: {ve}")
