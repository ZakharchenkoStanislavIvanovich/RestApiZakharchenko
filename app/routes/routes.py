from flask import Blueprint, request, jsonify
from app.models.models import Book
from app.extensions import db
from app.schemas.schemas import BookSchema, ValidationError

books_bp = Blueprint("books", __name__)
book_schema = BookSchema()
books_schema = BookSchema(many=True)

@books_bp.route("/", methods=["GET"])
def get_books():
    try:
        limit = int(request.args.get("limit", 5))
        offset = int(request.args.get("offset", 0))
    except ValueError:
        return jsonify({"error": "Invalid pagination parameters"}), 400

    books_query = Book.query.offset(offset).limit(limit).all()
    return jsonify([book.to_dict() for book in books_query])

@books_bp.route("/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book:
        return jsonify(book.to_dict())
    return jsonify({"error": "Книга не знайдена"}), 404

@books_bp.route("/", methods=["POST"])
def add_book():
    try:
        data = book_schema.load(request.json)
        new_book = Book(**data)
        db.session.add(new_book)
        db.session.commit()
        return jsonify(new_book.to_dict()), 201
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400

@books_bp.route("/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Книга не знайдена"}), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Книга видалена"})
