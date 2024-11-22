--Wenn die Tabellen nicht existieren, werden sie erstellt
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS flashcards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    subject TEXT NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    flashcard_id INTEGER,
    status TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (flashcard_id) REFERENCES flashcards(id) ON DELETE CASCADE
);

-- Falls vorhanden, werden die alten Tabellen gelöscht (für Neustart)
BEGIN TRANSACTION;
DROP TABLE IF EXISTS progress;
DROP TABLE IF EXISTS flashcards;
DROP TABLE IF EXISTS users;
COMMIT;

-- Beispiel-Daten einfügen
BEGIN TRANSACTION;
INSERT INTO users (username, password) VALUES ('user1', 'password123');
INSERT INTO users (username, password) VALUES ('user2', 'password456');

INSERT INTO flashcards (user_id, subject, question, answer) 
VALUES (1, 'Math', 'Was ist 2 + 2?', '4');
INSERT INTO flashcards (user_id, subject, question, answer) 
VALUES (1, 'History', 'Wer war Napoleon?', 'Ein französischer Kaiser');

INSERT INTO progress (user_id, flashcard_id, status) 
VALUES (1, 1, 'not started');
INSERT INTO progress (user_id, flashcard_id, status) 
VALUES (1, 2, 'in progress');

COMMIT;
