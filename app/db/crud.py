from bson import ObjectId

from typing import Optional

from .schema import UserSchema
from .database import AsyncIOMotorClient

from config import DB_NAME


async def retrieve_from_collections(conn: AsyncIOMotorClient, collection: str) -> list[dict]:
    objects = []
    async for obj in conn[DB_NAME][collection].findall():
        objects.append(obj)
    return objects


async def retrieve_data(conn: AsyncIOMotorClient, id: str, collection: str) -> dict:
    obj = await conn[DB_NAME][collection].find_one({'_id': ObjectId(id)})
    return obj


async def get_user_by_email(conn: AsyncIOMotorClient, email: str) -> Optional[UserSchema]:
    obj = await conn[DB_NAME]['user'].find_one({'email': email})
    return UserSchema(**obj) if obj else None
