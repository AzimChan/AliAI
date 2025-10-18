import sqlite3

conn = sqlite3.connect("bank_chatbot.db")
cursor = conn.cursor()

# Create main profile table
cursor.execute("""
CREATE TABLE IF NOT EXISTS financial_profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL,
    credit_balance REAL NOT NULL
);
""")

# Create related tables (nested concept)
cursor.executescript("""
CREATE TABLE IF NOT EXISTS secured_loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    loan_name TEXT,
    amount REAL,
    interest_rate REAL,
    FOREIGN KEY (profile_id) REFERENCES financial_profile(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS unsecured_loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    loan_name TEXT,
    amount REAL,
    interest_rate REAL,
    FOREIGN KEY (profile_id) REFERENCES financial_profile(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS deposits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    deposit_type TEXT,
    amount REAL,
    maturity_date TEXT,
    FOREIGN KEY (profile_id) REFERENCES financial_profile(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS income_expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    category TEXT,
    description TEXT,
    amount REAL,
    date TEXT,
    FOREIGN KEY (profile_id) REFERENCES financial_profile(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    goal_name TEXT,
    target_amount REAL,
    current_amount REAL,
    FOREIGN KEY (profile_id) REFERENCES financial_profile(id) ON DELETE CASCADE
);
""")

conn.commit()
print("✅ Database with nested (related) structure created!")
conn.close()

