-- Users Table (unchanged)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS flashcards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    subject TEXT ,
    question TEXT NOT NULL, -- The word
    answer TEXT NOT NULL, -- The translation
    category TEXT, -- Category (e.g., Household, Work, Nature)
    grade_level TEXT, -- Optional: Grade level (7–10)
    is_learned BOOLEAN DEFAULT 0, -- Track if the card is learned
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);


-- Progress Table (updated with UNIQUE constraint)
CREATE TABLE IF NOT EXISTS progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    flashcard_id INTEGER,
    review_count INTEGER DEFAULT 0, -- Track the number of reviews
    last_reviewed DATETIME DEFAULT NULL, -- Last review timestamp
    status TEXT NOT NULL, -- Active or Learned
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (flashcard_id) REFERENCES flashcards(id) ON DELETE CASCADE,
    UNIQUE (user_id, flashcard_id) -- Composite UNIQUE constraint
);

-- Test Results Table (unchanged)
CREATE TABLE IF NOT EXISTS test_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    correct_answers INTEGER,
    incorrect_answers INTEGER,
    total_questions INTEGER,
    test_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    UNIQUE(name, user_id),
    FOREIGN KEY(user_id) REFERENCES users(id)
);

