import os
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DB = "books.db"

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS books (title TEXT, author TEXT)")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        with sqlite3.connect(DB) as conn:
            conn.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
        return redirect("/")
    
    with sqlite3.connect(DB) as conn:
        books = conn.execute("SELECT title, author FROM books").fetchall()
    return render_template("index.html", books=books)

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
