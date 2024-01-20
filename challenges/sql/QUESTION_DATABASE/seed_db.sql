-- This script created and put the data in the database you're querying.

-- authors:
-- +----------+---------+
-- | authorId | name    |
-- +----------+---------+
-- | 1        | Alice   |
-- +----------+---------+
-- | 2        | Bob     |
-- +----------+---------+
-- | 3        | Charlie |
-- +----------+---------+

-- flashcards:
-- +---------------------------------+------------------+----------+
-- | question                        | answer           | authorId |
-- +---------------------------------+------------------+----------+
-- | What is powerhouse of the cell? | The Mitochondria | 1        |
-- +---------------------------------+------------------+----------+
-- | What is the capital of France?  | Paris            | 1        |
-- +---------------------------------+------------------+----------+
-- |               ...               |        ...       |    ...   |
-- +---------------------------------+------------------+----------+

BEGIN TRANSACTION;

    -- This database represents a basic example of a flashcard application.

    -- Create a table of authors, which have an id and name.
    CREATE TABLE authors (
        authorId INTEGER PRIMARY KEY,
        name     TEXT
    );

    -- Create a table of flashcards, which have questions, answers, and authors.
    -- Flashcards are uniquely identified by the combination of their question, answer, and author.
    CREATE TABLE flashcards (
        question    TEXT, 
        answer      TEXT,
        authorId    INTEGER,
        PRIMARY KEY (question, answer, authorId),
        FOREIGN KEY (authorId) REFERENCES authors(authorId)
    );


    INSERT INTO authors (authorId, name)
           VALUES (1, "Alice"),
                  (2, "Bob"),
                  (3, "Charlie");

    INSERT INTO flashcards (question, answer, authorId)
           VALUES ("What is powerhouse of the cell?", "The Mitochondria", 1),
                  ("What is the capital of France?", "Paris", 1),
                  ("What is the largest planet in our solar system?", "Jupiter", 1),
                  ("What is the smallest country in the world?", "Vatican City", 1),
                  ("What is the chemical symbol for gold?", "Au", 1),
                  ("What is the largest organ in the human body?", "Skin", 1),
                  ("What is the most abundant gas in the Earth's atmosphere?", "Nitrogen", 2),
                  ("What is the process by which plants make their own food?", "Photosynthesis", 2),
                  ("What is the name of the force that opposes motion?", "Friction", 2),
                  ("What is the name of the process by which a gas turns into a liquid?", "Condensation", 2);

COMMIT;

-- Wondering about BEGIN TRANSACTION / COMMIT?
-- https://en.wikipedia.org/wiki/Database_transaction
-- https://en.wikipedia.org/wiki/Commit_(data_management)
