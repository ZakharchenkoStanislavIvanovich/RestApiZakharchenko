from marshmallow import Schema, fields, validates, ValidationError

class BookSchema(Schema):
    book_id = fields.Int(required=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)

    @validates("title")
    def validate_title(self, value):
        if len(value) < 2:
            raise ValidationError("Title must be at least 2 characters long.")

    @validates("author")
    def validate_author(self, value):
        if len(value) < 2:
            raise ValidationError("Author must be at least 2 characters long.")
