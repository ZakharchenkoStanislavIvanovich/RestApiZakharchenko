from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.collection import Collection

client = AsyncIOMotorClient("mongodb://mongo_admin:password@localhost:27017")
db = client.books
books_collection: Collection = db.books
