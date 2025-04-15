import os
import json
from collections import Counter
import csv

DATA_FILE = "books.json"

def load_books():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[Error] Failed to load data: {e}")
    return []

def save_books(books):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(books, f, indent=4)
        return True
    except Exception as e:
        print(f"[Error] Failed to save data: {e}")
        return False

def add_book(title, author, genre="", status=""):
    books = load_books()
    book = {
        "title": title.strip(),
        "author": author.strip(),
        "genre": genre.strip(),
        "status": status.strip().lower()
    }
    books.append(book)
    save_books(books)

def delete_book(index):
    books = load_books()
    try:
        removed = books.pop(index)
        save_books(books)
        return removed
    except IndexError:
        return None

def edit_book(index, new_data):
    books = load_books()
    try:
        book = books[index]
        book["title"] = new_data.get("title", book["title"])
        book["author"] = new_data.get("author", book["author"])
        book["genre"] = new_data.get("genre", book["genre"])
        book["status"] = new_data.get("status", book["status"])
        save_books(books)
        return book
    except IndexError:
        return None

def search_books(keyword):
    keyword = keyword.lower().strip()
    results = []
    for book in load_books():
        if (keyword in book.get("title", "").lower()
                or keyword in book.get("author", "").lower()
                or keyword in book.get("genre", "").lower()):
            results.append(book)
    return results

def export_books(filename="books_export.csv"):
    books = load_books()
    if not books:
        return False
    try:
        with open(filename, "w", newline='', encoding='utf-8') as csvfile:
            fieldnames = ["title", "author", "genre", "status"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for book in books:
                writer.writerow(book)
        return True
    except Exception as e:
        print(f"[Error] Failed to export books: {e}")
        return False

def get_statistics():
    books = load_books()
    total = len(books)
    genres = Counter(book["genre"].lower() for book in books if book.get("genre"))
    statuses = Counter(book["status"].lower() for book in books if book.get("status"))
    return {
        "total": total,
        "genres": dict(genres),
        "statuses": dict(statuses)
    }
    