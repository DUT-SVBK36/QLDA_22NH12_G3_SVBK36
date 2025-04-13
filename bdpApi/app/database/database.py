from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database
from pymongo.collection import Collection
from contextlib import asynccontextmanager

# MongoDB connection
MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "detection_system"

# Create MongoDB client
client = AsyncIOMotorClient(MONGODB_URL)
db = client[DATABASE_NAME]

# Collections
users_collection = db.users
sessions_collection = db.sessions
session_items_collection = db.session_items
labels_collection = db.labels

# Dependency to get DB
async def get_db():
    """Return database client"""
    return db

# Dependency to get specific collections
async def get_users_collection():
    """Return users collection"""
    return users_collection

async def get_sessions_collection():
    """Return sessions collection"""
    return sessions_collection

async def get_session_items_collection():
    """Return session items collection"""
    return session_items_collection

async def get_labels_collection():
    """Return labels collection"""
    return labels_collection 