import json
from flask import Blueprint, Response, request
from .models import Book, books, save_books
from .schemas import BookSchema, ValidationError

books_bp = Blueprint("books", __name__)
book_schema = BookSchema()
books_schema = BookSchema(many=True)

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
        book_data = book_schema.load(request.json)
        new_book = Book(**book_data)
        book_dict = new_book.to_dict()
        books.append(book_dict)
        save_books()
        return Response(json.dumps(book_dict, ensure_ascii=False, indent=4), content_type="application/json; charset=utf-8"), 201
    except ValidationError as e:
        return Response(json.dumps({"error": e.messages}, ensure_ascii=False), content_type="application/json; charset=utf-8"), 400

@books_bp.route("/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    global books
    book_exists = any(b["book_id"] == book_id for b in books)
    
    if not book_exists:
        return Response(json.dumps({"error": "Книга не знайдена"}, ensure_ascii=False), content_type="application/json; charset=utf-8"), 404

    books = [b for b in books if b["book_id"] != book_id]
    save_books()
    return Response(json.dumps({"message": "Книга видалена"}, ensure_ascii=False), content_type="application/json; charset=utf-8"), 200
