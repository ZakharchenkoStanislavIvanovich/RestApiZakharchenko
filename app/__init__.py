from flask import Flask
from app.extensions import db
from flask_restful import Api
from flasgger import Swagger

from app.routes.routes import BookListResource, BookResource

def create_app():
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:12345z@db:5432/library"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config['SWAGGER'] = {
        'title': 'Library API',
        'uiversion': 3
    }

    db.init_app(app)
    Swagger(app)
    api = Api(app)

    api.add_resource(BookListResource, "/books")
    api.add_resource(BookResource, "/books/<int:book_id>")

    with app.app_context():
        from app.models.models import Book
        db.create_all()

    return app
