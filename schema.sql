CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT,
    phone TEXT,
    email TEXT UNIQUE NOT NULL,
    password TEXT,
    active INTEGER DEFAULT 1,
    date_created TEXT,
    hire_date TEXT,
    user_type INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS Competencies (
    competency_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    date_created TEXT
);

CREATE TABLE IF NOT EXISTS Assessments (
    assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    competency_id INTEGER,
    name TEXT NOT NULL,
    date_created TEXT,
    FOREIGN KEY (competency_id)
        REFERENCES Competencies (competency_id)
);

CREATE TABLE IF NOT EXISTS Assessment_Results (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    assessment_id INTEGER,
    score INTEGER,
    date_taken DATE,
    manager_id INTEGER,
    FOREIGN KEY (user_id)
        REFERENCES Users (user_id)
    FOREIGN KEY (assessment_id)
        REFERENCES Assessments (assessment_id)
    FOREIGN KEY (manager_id)
        REFERENCES Users (user_id)
);
