from flask_restful import Resource
from flask import request
from app.models.models import Book
from app.extensions import db
from app.schemas.schemas import BookSchema, ValidationError
from flasgger import swag_from

book_schema = BookSchema()
books_schema = BookSchema(many=True)


class BookListResource(Resource):
    @swag_from({
        'tags': ['Books'],
        'parameters': [
            {
                'name': 'limit',
                'in': 'query',
                'type': 'integer',
                'required': False,
                'default': 5
            },
            {
                'name': 'cursor',
                'in': 'query',
                'type': 'integer',
                'required': False
            }
        ],
        'responses': {
            200: {
                'description': 'Список книг',
                'content': {
                    'application/json': {
                        'example': {
                            'books': [{'book_id': 1, 'title': 'Book title', 'author': 'Author'}],
                            'next_cursor': 2
                        }
                    }
                }
            }
        }
    })
    def get(self):
        try:
            limit = int(request.args.get("limit", 5))
            cursor = request.args.get("cursor")
        except ValueError:
            return {"error": "Invalid pagination parameters"}, 400

        if cursor:
            books_query = Book.query.filter(Book.book_id > cursor).limit(limit).all()
        else:
            books_query = Book.query.limit(limit).all()

        if books_query:
            next_cursor = books_query[-1].book_id
            return {
                "books": [book.to_dict() for book in books_query],
                "next_cursor": next_cursor
            }
        return {"books": []}

    @swag_from({
        'tags': ['Books'],
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'title': {'type': 'string'},
                        'author': {'type': 'string'}
                    },
                    'required': ['title', 'author']
                },
                'example': {
                    'title': '1984',
                    'author': 'George Orwell'
                }
            }
        ],
        'responses': {
            201: {
                'description': 'Книга створена',
                'examples': {
                    'application/json': {
                        'book_id': 1,
                        'title': '1984',
                        'author': 'George Orwell'
                    }
                }
            },
            400: {
                'description': 'Помилка валідації'
            }
        }
    })
    def post(self):
        try:
            data = book_schema.load(request.json)
            new_book = Book(**data)
            db.session.add(new_book)
            db.session.commit()
            return new_book.to_dict(), 201
        except ValidationError as err:
            return {'error': err.messages}, 400



class BookResource(Resource):
    @swag_from({
        'tags': ['Books'],
        'parameters': [
            {
                'name': 'book_id',
                'in': 'path',
                'type': 'integer',
                'required': True
            }
        ],
        'responses': {
            200: {
                'description': 'Книга знайдена',
                'content': {
                    'application/json': {
                        'example': {'book_id': 1, 'title': 'Book title', 'author': 'Author'}
                    }
                }
            },
            404: {
                'description': 'Книга не знайдена'
            }
        }
    })
    def get(self, book_id):
        book = Book.query.get(book_id)
        if book:
            return book.to_dict()
        return {'error': 'Книга не знайдена'}, 404

    @swag_from({
        'tags': ['Books'],
        'parameters': [
            {
                'name': 'book_id',
                'in': 'path',
                'type': 'integer',
                'required': True
            }
        ],
        'responses': {
            204: {
                'description': 'Книга видалена (без вмісту)'
            },
            404: {
                'description': 'Книга не знайдена'
            }
        }
    })
    def delete(self, book_id):
        book = Book.query.get(book_id)
        if not book:
            return {'error': 'Книга не знайдена'}, 404
        db.session.delete(book)
        db.session.commit()
        return '', 204
