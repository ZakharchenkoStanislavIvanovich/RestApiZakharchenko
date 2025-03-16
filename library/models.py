import json

BOOKS_FILE = "books.json"

def load_books():
    try:
        with open(BOOKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

books = load_books()

def save_books():
    with open(BOOKS_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=4, ensure_ascii=False)

def generate_book_id():
      if not books:
        return 1
      return max(book["book_id"] for book in books) + 1

class Book:
    def __init__(self, title, author):
        self.book_id = generate_book_id()
        self.title = title
        self.author = author

    def to_dict(self):
      
        return {"book_id": self.book_id, "title": self.title, "author": self.author}
