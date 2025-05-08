from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.library.models import BookSchema
from app.library.database import books_collection
from pydantic_mongo import ObjectIdField
from fastapi import status
from fastapi.responses import Response

books_router = APIRouter()

@books_router.get("/", response_model=list[BookSchema])
async def get_books():
    books_cursor = books_collection.find({})
    books = [BookSchema(**book) async for book in books_cursor]
    return books

@books_router.get("/{book_id}", response_model=BookSchema)
async def get_book(book_id: str):
    book = await books_collection.find_one({"_id": ObjectId(book_id)})
    if not book:
        raise HTTPException(status_code=404, detail="Книга не знайдена")
    return BookSchema(**book)

@books_router.post("/", response_model=BookSchema, status_code=201)
async def add_book(new_book: BookSchema):
    new_book_dict = new_book.model_dump(by_alias=True, exclude={"id"})
    result = await books_collection.insert_one(new_book_dict)
    created_book = await books_collection.find_one({"_id": result.inserted_id})
    return BookSchema(**created_book)

@books_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: str):
    result = await books_collection.delete_one({"_id": ObjectId(book_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Книга не знайдена")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
