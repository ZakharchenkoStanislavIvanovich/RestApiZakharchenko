from fastapi import FastAPI
from library.routes import books_router

app = FastAPI(title="Library API")

app.include_router(books_router, prefix="/books")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
