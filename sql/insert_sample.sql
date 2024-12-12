-- Beispiel-Daten nur einfügen, wenn keine Benutzer existieren
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
