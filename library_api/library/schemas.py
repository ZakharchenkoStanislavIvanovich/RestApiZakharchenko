from pydantic import BaseModel, Field

class BookSchema(BaseModel):
    book_id: int
    title: str = Field(..., min_length=2, description="Назва має бути не менше 2 символів")
    author: str = Field(..., min_length=2, description="Автор має бути не менше 2 символів")
