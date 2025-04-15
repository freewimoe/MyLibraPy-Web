import sqlite3

DB = "books.db"

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                genre TEXT,
                status TEXT
            )
        """)

def load_books():
    with sqlite3.connect(DB) as conn:
        cursor = conn.execute("SELECT title, author, genre, status FROM books")
        rows = cursor.fetchall()
        books = [
            {"title": row[0], "author": row[1], "genre": row[2], "status": row[3]}
            for row in rows
        ]
        return books

def add_book(title, author, genre, status):
    with sqlite3.connect(DB) as conn:
        conn.execute(
            "INSERT INTO books (title, author, genre, status) VALUES (?, ?, ?, ?)",
            (title.strip(), author.strip(), genre.strip(), status.strip())
        )

def search_books(keyword):
    keyword = f"%{keyword.lower()}%"
    with sqlite3.connect(DB) as conn:
        cursor = conn.execute("""
            SELECT title, author, genre, status FROM books
            WHERE LOWER(title) LIKE ?
               OR LOWER(author) LIKE ?
               OR LOWER(genre) LIKE ?
        """, (keyword, keyword, keyword))
        rows = cursor.fetchall()
        return [
            {"title": row[0], "author": row[1], "genre": row[2], "status": row[3]}
            for row in rows
        ]
