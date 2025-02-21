# db.py
import sqlite3
from flask import g

DATABASE = "finance.db"

def get_db():
    """Establish and return a database connection.

    Connects to the SQLite database specified in DATABASE, storing the connection in Flask’s
    g object to reuse it throughout the request. The row_factory is set to enable dictionary-like
    access to rows.
    """
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return g.db

def close_db(exception=None):
    """Close the database connection at the end of the request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()

def create_tables():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            hash TEXT NOT NULL,
            cash NUMERIC NOT NULL DEFAULT 10000.00 CHECK (cash >= 0)
        );

        CREATE TABLE IF NOT EXISTS sqlite_sequence(name,seq);

        CREATE TABLE IF NOT EXISTS history_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL CHECK (type IN ('buy', 'sell')),
            stock_symbol TEXT NOT NULL,
            stock_price NUMERIC NOT NULL,
            shares_amount INTEGER NOT NULL CHECK (shares_amount > 0),
            time DATETIME NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
        );

        CREATE TABLE IF NOT EXISTS user_stocks (
            user_id INTEGER NOT NULL,
            stock_symbol TEXT NOT NULL,
            shares_amount INTEGER NOT NULL CHECK (shares_amount > 0),
            PRIMARY KEY (user_id, stock_symbol),
            FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
        );""")
    
    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_tables()
    print("Database initialize successfully")