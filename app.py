import os
from flask import Flask, render_template, request, redirect
from mylibrapy.logic import (
    load_books, add_book, search_books, init_db
)

app = Flask(__name__)
init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        genre = request.form.get("genre", "")
        status = request.form.get("status", "")
        add_book(title, author, genre, status)
        return redirect("/")

    books = load_books()
    return render_template("index.html", books=books)

@app.route("/search")
def search():
    keyword = request.args.get("q", "")
    results = search_books(keyword) if keyword else []
    return render_template("search.html", books=results, query=keyword)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)  # debug=True für Auto-Reload
