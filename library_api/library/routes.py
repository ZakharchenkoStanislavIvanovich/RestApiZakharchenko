import json
from flask import Blueprint, Response, request
from library.schemas import BookSchema

books_bp = Blueprint("books", __name__)
book_schema = BookSchema()
books_schema = BookSchema(many=True)

BOOKS_FILE = "books.json"

def load_books():
    try:
        with open(BOOKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_books(books):
    with open(BOOKS_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=4, ensure_ascii=False)

books = load_books()

@books_bp.route("/", methods=["GET"])
def get_books():
    return Response(json.dumps(books, ensure_ascii=False, indent=4), content_type="application/json; charset=utf-8")

@books_bp.route("/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((b for b in books if b["book_id"] == book_id), None)
    if book:
        return Response(json.dumps(book, ensure_ascii=False, indent=4), content_type="application/json; charset=utf-8")
    return Response(json.dumps({"error": "Книга не знайдена"}, ensure_ascii=False), content_type="application/json; charset=utf-8"), 404

@books_bp.route("/", methods=["POST"])
def add_book():
    try:
        new_book = book_schema.load(request.json)
        books.append(new_book)
        save_books(books)
        return Response(json.dumps(new_book, ensure_ascii=False, indent=4), content_type="application/json; charset=utf-8"), 201
    except Exception as e:
        return Response(json.dumps({"error": str(e)}, ensure_ascii=False), content_type="application/json; charset=utf-8"), 400

@books_bp.route("/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    global books
    books = [b for b in books if b["book_id"] != book_id]
    save_books(books)
    return Response(json.dumps({"message": "Книга видалена"}, ensure_ascii=False), content_type="application/json; charset=utf-8"), 200
