from app.extensions import db

class Book(db.Model):
    __tablename__ = "books"
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    author = db.Column(db.String(128), nullable=False)

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author
        }
