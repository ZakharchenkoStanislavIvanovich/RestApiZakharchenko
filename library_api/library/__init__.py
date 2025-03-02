from flask import Flask
from library.routes import books_bp

def create_app():
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False
    app.register_blueprint(books_bp, url_prefix="/books")
    return app
