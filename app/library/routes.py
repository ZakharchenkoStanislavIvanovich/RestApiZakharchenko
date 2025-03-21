
import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.library.schemas import BookSchema

books_router = APIRouter()
BOOKS_FILE = "books.json"

async def load_books():
    try:
        with open(BOOKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

async def save_books(books):
    with open(BOOKS_FILE, "w", encoding="utf-8") as f:
        json.dump([book.model_dump() for book in books], f, indent=4, ensure_ascii=False)

books = []

@books_router.on_event("startup")
async def startup_event():
    global books
    books_data = await load_books()
    books = [BookSchema(**book) for book in books_data]

@books_router.get("/", response_model=list[BookSchema])
async def get_books():
    return books

@books_router.get("/{book_id}", response_model=BookSchema)
async def get_book(book_id: int):
    book = next((b for b in books if b.book_id == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail="Книга не знайдена")
    return book

@books_router.post("/", response_model=BookSchema, status_code=201)
async def add_book(new_book: BookSchema):
    global books
    new_id = max((b.book_id for b in books), default=0) + 1
    book = BookSchema(book_id=new_id, title=new_book.title, author=new_book.author)
    books.append(book)
    await save_books(books)
    return book

@books_router.delete("/{book_id}")
async def delete_book(book_id: int):
    global books
    books = [b for b in books if b.book_id != book_id]
    await save_books(books)
    return {"message": "Книга видалена"}