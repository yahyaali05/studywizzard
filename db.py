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


def insert_sample_for_user(user_id):
    try:
        db_con = get_db_con()
        existing_flashcards = db_con.execute('''SELECT id FROM flashcards WHERE user_id = ?''', (user_id,)).fetchall()
        if existing_flashcards:
            return  # Skip if user already has flashcards

        flashcards_data = [
    # Household (English grammar focus)
    ('Household', 'Wie sagt man "Teller" auf Englisch?', 'Plate', '7'),
    ('Household', 'Wie bildet man den Plural von "knife" auf Englisch?', 'Knives', '7'),
    ('Household', 'Was bedeutet "to clean" auf Deutsch?', 'Putzen', '7'),
    ('Household', 'Was ist das englische Wort für "Kühlschrank"?', 'Fridge', '7'),
    ('Household', 'Was ist das Gegenteil von "dirty"?', 'Clean', '7'),
    ('Household', 'Wie sagt man "Staubsauger" auf Englisch?', 'Vacuum cleaner', '8'),
    ('Household', 'Was bedeutet "to dust" auf Deutsch?', 'Abstauben', '8'),
    ('Household', 'Wie bildet man die Vergangenheit von "buy"?', 'Bought', '8'),
    ('Household', 'Was ist der Unterschied zwischen "much" und "many"?', 'Much für unzählbare, many für zählbare Nomen.', '8'),
    ('Household', 'Bilde einen Satz mit "there is" oder "there are".', 'There is a table in the kitchen.', '8'),
    ('Household', 'Wann benutzt man "some" und "any" in Fragen?', 'Any in den meisten Fragen, some wenn eine positive Antwort erwartet wird.', '9'),
    ('Household', 'Bilde einen Satz mit "have to".', 'I have to clean my room every Saturday.', '9'),
    ('Household', 'Was ist die Steigerung von "little"?', 'Less, least.', '9'),
    ('Household', 'Was ist die richtige Form: "much money" oder "many money"?', 'Much money (da unzählbar).', '9'),
    ('Household', 'Setze "yet" oder "still" in einen korrekten Satz.', 'She hasn’t finished her homework yet.', '9'),
    ('Household', 'Was ist der Unterschied zwischen "some" und "any"?', 'Some für positive Sätze, any für negative und Fragen.', '10'),
    ('Household', 'Bilde einen korrekten Satz mit "used to".', 'I used to live in Berlin.', '10'),
    ('Household', 'Wann benutzt man das Present Perfect im Englischen?', 'Bei Handlungen, die in der Vergangenheit begannen und noch andauern.', '10'),
    ('Household', 'Was ist die richtige Form: "less" oder "fewer"?', 'Fewer für zählbare, less für unzählbare Nomen.', '10'),
    ('Household', 'Setze "already" oder "yet" in einen korrekten Satz.', 'Have you finished your homework yet?', '10'),

    # Work
    ('Work', 'Wie sagt man "Chef" auf Englisch?', 'Boss', '7'),
    ('Work', 'Was bedeutet "to apply for a job" auf Deutsch?', 'Sich für eine Stelle bewerben', '7'),
    ('Work', 'Wie heißt "Lebenslauf" auf Englisch?', 'Resume', '7'),
    ('Work', 'Wie sagt man "Büro" auf Englisch?', 'Office', '7'),
    ('Work', 'Was bedeutet "to work from home"?', 'Von zu Hause aus arbeiten', '7'),
    ('Work', 'Wie sagt man "Mitarbeiter" auf Englisch?', 'Employee', '8'),
    ('Work', 'Was bedeutet "to be promoted" auf Deutsch?', 'Befördert werden', '8'),
    ('Work', 'Wie bildet man das Simple Past von "go"?', 'Went', '8'),
    ('Work', 'Was bedeutet "to sign a contract" auf Deutsch?', 'Einen Vertrag unterschreiben', '8'),
    ('Work', 'Bilde einen Satz mit "can" oder "must".', 'You must finish your work on time.', '8'),
    ('Work', 'Wann benutzt man "whom" statt "who"?', 'Wenn es das Objekt im Satz ist.', '9'),
    ('Work', 'Was ist ein Gerundium im Englischen?', 'Eine Verbform mit -ing, die als Nomen benutzt wird.', '9'),
    ('Work', 'Bilde einen Satz mit "despite".', 'Despite the rain, we went outside.', '9'),
    ('Work', 'Wann benutzt man das Passiv im Englischen?', 'Wenn die Handlung wichtiger als das Subjekt ist.', '9'),
    ('Work', 'Setze "neither" oder "either" in einen Satz.', 'Neither of them was ready.', '9'),
    ('Work', 'Bilde einen Satz mit "even though".', 'Even though it was late, he continued working.', '10'),
    ('Work', 'Wann benutzt man das Subjunctive im Englischen?', 'In hypothetischen oder Wunsch-Sätzen.', '10'),
    ('Work', 'Setze "must" oder "have to" in einen Satz.', 'I must study for the exam.', '10'),
    ('Work', 'Was ist ein Phrasal Verb? Gib ein Beispiel.', 'Ein Verb mit Präposition/Adverb, z. B. "give up".', '10'),
    ('Work', 'Was ist der Unterschied zwischen "make" und "do"?', 'Make für kreative Dinge, do für Tätigkeiten.', '10'),

    # Nature
    ('Nature', 'Wie sagt man "Baum" auf Englisch?', 'Tree', '7'),
    ('Nature', 'Was ist das englische Wort für "Blume"?', 'Flower', '7'),
    ('Nature', 'Was bedeutet "to grow" auf Deutsch?', 'Wachsen', '7'),
    ('Nature', 'Wie sagt man "Wolke" auf Englisch?', 'Cloud', '7'),
    ('Nature', 'Was bedeutet "to plant" auf Deutsch?', 'Pflanzen', '7'),
    ('Nature', 'Wie sagt man "Berg" auf Englisch?', 'Mountain', '8'),
    ('Nature', 'Was bedeutet "to rain" auf Deutsch?', 'Regnen', '8'),
    ('Nature', 'Was ist die Vergangenheit von "see"?', 'Saw', '8'),
    ('Nature', 'Wie sagt man "Fluss" auf Englisch?', 'River', '8'),
    ('Nature', 'Bilde einen Satz mit "because".', 'I stayed inside because it was raining.', '8'),
    ('Nature', 'Was ist die passive Form von "The wind blows the leaves"?', 'The leaves are blown by the wind.', '9'),
    ('Nature', 'Bilde einen Satz mit einem Partizipialsatz.', 'Walking through the forest, I saw a deer.', '9'),
    ('Nature', 'Wann benutzt man "so" und wann "such"?', 'So + Adjektiv, such + Adjektiv + Nomen.', '9'),
    ('Nature', 'Setze "either" oder "neither" in einen Satz.', 'I don’t like either of these options.', '9'),
    ('Nature', 'Was ist der Unterschied zwischen "will" und "going to" in Zukunftssätzen?', 'Will für spontane Entscheidungen, going to für geplante Aktionen.', '9'),
    ('Nature', 'Bilde einen Satz mit "although".', 'Although it was raining, we went outside.', '10'),
    ('Nature', 'Wann benutzt man "which" statt "that"?', 'Which für zusätzliche Informationen, that für notwendige.', '10'),
    ('Nature', 'Setze "already" oder "yet" in einen Satz.', 'I haven’t finished my essay yet.', '10'),
    ('Nature', 'Was ist der Unterschied zwischen "say" und "tell"?', 'Say wird allgemein benutzt, tell benötigt oft ein Objekt.', '10'),
    ('Nature', 'Wann benutzt man das Past Perfect im Englischen?', 'Bei einer Handlung, die vor einer anderen in der Vergangenheit passiert ist.', '10'),

        ('School', 'Wie sagt man "Lehrer" auf Englisch?', 'Teacher', '7'),
    ('School', 'Was bedeutet "to write" auf Deutsch?', 'Schreiben', '7'),
    ('School', 'Wie heißt das englische Wort für "Schule"?', 'School', '7'),
    ('School', 'Wie sagt man "Heft" auf Englisch?', 'Notebook', '7'),
    ('School', 'Wie heißt "Tafel" auf Englisch?', 'Board', '7'),
    ('School', 'Wie sagt man "Schüler" auf Englisch?', 'Student', '8'),
    ('School', 'Was bedeutet "to study" auf Deutsch?', 'Lernen / Studieren', '8'),
    ('School', 'Wie bildet man die Vergangenheit von "read"?', 'Read (Aussprache: red)', '8'),
    ('School', 'Was ist das englische Wort für "Klassenzimmer"?', 'Classroom', '8'),
    ('School', 'Bilde einen Satz mit "can" oder "should".', 'You should do your homework.', '8'),
    ('School', 'Wann benutzt man das Past Perfect im Englischen?', 'Bei einer Handlung, die vor einer anderen in der Vergangenheit passiert ist.', '9'),
    ('School', 'Was ist der Unterschied zwischen "say" und "tell"?', 'Say wird allgemein benutzt, tell benötigt oft ein Objekt.', '9'),
    ('School', 'Bilde einen Satz mit "although".', 'Although it was raining, we went outside.', '9'),
    ('School', 'Wann benutzt man "which" statt "that"?', 'Which für zusätzliche Informationen, that für notwendige.', '9'),
    ('School', 'Setze "already" oder "yet" in einen Satz.', 'I haven’t finished my essay yet.', '9'),
    ('School', 'Bilde einen Satz mit einem Relativsatz.', 'The book that I borrowed is very interesting.', '10'),
    ('School', 'Wann benutzt man das Future Perfect?', 'Für eine Handlung, die zu einem bestimmten Zeitpunkt in der Zukunft abgeschlossen sein wird.', '10'),
    ('School', 'Was ist der Unterschied zwischen "either" und "neither"?', 'Either für eine Auswahl, neither für keine der Optionen.', '10'),
    ('School', 'Bilde einen Satz mit "unless".', 'I won’t go outside unless it stops raining.', '10'),
    ('School', 'Setze "yet" oder "still" in einen Satz.', 'She still hasn’t arrived.', '10'),

    # Other
    ('Other', 'Wie sagt man "Auto" auf Englisch?', 'Car', '7'),
    ('Other', 'Was bedeutet "to run" auf Deutsch?', 'Rennen', '7'),
    ('Other', 'Wie heißt "Haus" auf Englisch?', 'House', '7'),
    ('Other', 'Was ist das englische Wort für "Straße"?', 'Street', '7'),
    ('Other', 'Was bedeutet "to jump" auf Deutsch?', 'Springen', '7'),
    ('Other', 'Wie sagt man "Fenster" auf Englisch?', 'Window', '8'),
    ('Other', 'Was bedeutet "to open" auf Deutsch?', 'Öffnen', '8'),
    ('Other', 'Was ist die Vergangenheit von "take"?', 'Took', '8'),
    ('Other', 'Wie sagt man "Tür" auf Englisch?', 'Door', '8'),
    ('Other', 'Bilde einen Satz mit "like".', 'I like playing football.', '8'),
    ('Other', 'Was ist der Unterschied zwischen "make" und "do"?', 'Make für kreative Dinge, do für Tätigkeiten.', '9'),
    ('Other', 'Was ist ein Phrasal Verb? Gib ein Beispiel.', 'Ein Verb mit Präposition/Adverb, z. B. "give up".', '9'),
    ('Other', 'Wann benutzt man das Subjunctive im Englischen?', 'In hypothetischen oder Wunsch-Sätzen.', '9'),
    ('Other', 'Bilde einen Satz mit "even though".', 'Even though it was late, he continued working.', '9'),
    ('Other', 'Setze "must" oder "have to" in einen Satz.', 'I must study for the exam.', '9'),
    ('Other', 'Wann benutzt man "used to" im Englischen?', 'Für vergangene Gewohnheiten oder Zustände.', '10'),
    ('Other', 'Was ist der Unterschied zwischen "so" und "such"?', 'So + Adjektiv, such + Adjektiv + Nomen.', '10'),
    ('Other', 'Bilde einen Satz mit einem Bedingungssatz (If-Satz).', 'If it rains, we will stay inside.', '10'),
    ('Other', 'Wann benutzt man das Gerundium im Englischen?', 'Nach bestimmten Verben und Präpositionen, z. B. "enjoy doing".', '10'),
    ('Other', 'Setze "neither" oder "either" in einen Satz.', 'Neither of them was ready.', '10'),
]


        for category, question, answer, grade_level in flashcards_data:
            db_con.execute(''' 
                INSERT INTO flashcards (user_id, category, question, answer, grade_level, is_learned) 
                VALUES (?, ?, ?, ?, ?, 0)
            ''', (user_id, category, question, answer, grade_level))

        db_con.commit()
    except sqlite3.DatabaseError as e:
        print(f"Error inserting flashcards: {e}")

def initialize_categories(db_con, user_id): 
    categories = ['Household', 'Work', 'Nature', 'School', 'Other']
    for category in categories:
        db_con.execute('''
            INSERT OR IGNORE INTO categories (name, user_id) VALUES (?, ?)
        ''', (category, user_id))
    db_con.commit()



def create_flashcard_for_user(user_id, category, question, answer, grade_level):
    try:
        db_con = get_db_con()
        # Insert flashcard into the database
        db_con.execute(''' 
            INSERT INTO flashcards (user_id, category, question, answer, grade_level, is_learned)
            VALUES (?, ?, ?, ?, ?, 0)
        ''', (user_id, category, question, answer, grade_level))

        db_con.commit()
    except sqlite3.DatabaseError as e:
        print(f"Error creating flashcard: {e}")


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

def get_flashcards_for_user(user_id):
    db_con = get_db_con()
    return db_con.execute('''
        SELECT id, category, question, answer
        FROM flashcards
        WHERE user_id = ? AND is_learned = 0
        ORDER BY id ASC
    ''', (user_id,)).fetchall()


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

