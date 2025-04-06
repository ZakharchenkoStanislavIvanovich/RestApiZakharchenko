from flask import Flask
from app.extensions import db
from app.routes.routes import books_bp

def create_app():
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:12345z@db:5432/library"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    app.register_blueprint(books_bp, url_prefix="/books")

    with app.app_context():
        from app.models.models import Book
        db.create_all()

    return app
