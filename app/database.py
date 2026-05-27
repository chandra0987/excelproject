from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config import settings

client: AsyncIOMotorClient | None = None
db: AsyncIOMotorDatabase | None = None


async def init_db():
    """Initialize MongoDB connection."""
    global client, db
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]

    # Ensure indexes for the users collection
    await db.users.create_index("username", unique=True)
    await db.users.create_index("email", unique=True)


async def close_db():
    """Close MongoDB connection."""
    global client
    if client:
        client.close()
        client = None


def get_database() -> AsyncIOMotorDatabase:
    """Return the database instance (must be called after init_db)."""
    if db is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return db


def get_users_collection():
    """Return the users collection."""
    return get_database().users
