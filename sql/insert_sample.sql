#Beispiel-Daten nur einfügen, wenn keine Benutzer existieren
def insert_sample():
    db_con = get_db_con()
    
#Überprüfen, ob bereits Benutzer existieren
    if db_con.execute('SELECT COUNT(*) FROM users').fetchone()[0] > 0:
        print("Benutzer existieren bereits, überspringe Insert-Beispiel-Daten.")
        return

#Beispiel-Daten einfügen
    db_con.execute('''INSERT INTO users (username, password) VALUES ('user1', 'password123')''')
    db_con.execute('''INSERT INTO users (username, password) VALUES ('user2', 'password456')''')
    db_con.commit()
    
    # Flashcards für Benutzer 1 einfügen
    db_con.execute('''INSERT INTO flashcards (user_id, subject, question, answer) 
                       VALUES (1, 'Math', 'Was ist 2 + 2?', '4')''')
    db_con.execute('''INSERT INTO flashcards (user_id, subject, question, answer) 
                       VALUES (1, 'History', 'Wer war Napoleon?', 'Ein französischer Kaiser')''')
    db_con.commit()
