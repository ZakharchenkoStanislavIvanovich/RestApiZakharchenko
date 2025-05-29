import os
from motor.motor_asyncio import AsyncIOMotorClient

mongo_uri = os.getenv("MONGO_URI", "mongodb://mongo_admin:password@mongo_db:27017")
client = AsyncIOMotorClient(mongo_uri)
db = client.books
books_collection = db.books
