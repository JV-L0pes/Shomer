import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/shomerdb")
client = AsyncIOMotorClient(MONGODB_URI)
db = client.get_default_database()

users_collection = db["users"]
logs_collection = db["logs"] 