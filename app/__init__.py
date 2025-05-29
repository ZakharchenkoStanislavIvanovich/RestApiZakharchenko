from fastapi import FastAPI
from app.library.routes import books_router
from app.auth.routes import auth_router

def create_app():
    app = FastAPI(title="Library API")
    app.include_router(auth_router, prefix="/auth")
    app.include_router(books_router, prefix="/books")
    return app