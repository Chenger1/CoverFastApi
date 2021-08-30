from bson import ObjectId

from typing import Optional

from .schema import UserSchema
from .database import AsyncIOMotorClient

from config import DB_NAME


async def create_new_item(conn: AsyncIOMotorClient, collection: str, data: dict) -> dict:
    item = await conn[DB_NAME][collection].insert_one(data)
    return await conn[DB_NAME][collection].find_one({'_id': item.inserted_id})


async def retrieve_from_collections(conn: AsyncIOMotorClient, collection: str) -> list[dict]:
    objects = []
    async for obj in conn[DB_NAME][collection].find():
        objects.append(obj)
    return objects


async def retrieve_data(conn: AsyncIOMotorClient, id: str, collection: str) -> dict:
    obj = await conn[DB_NAME][collection].find_one({'_id': ObjectId(id)})
    return obj


async def get_user_by_email(conn: AsyncIOMotorClient, email: str) -> Optional[UserSchema]:
    obj = await conn[DB_NAME]['user'].find_one({'email': email})
    return UserSchema(**obj) if obj else None


async def update_main_page(conn: AsyncIOMotorClient, data: dict) -> bool:
    item = await conn[DB_NAME]['main_page'].find_one()
    if item:
        updated_item = await conn[DB_NAME]['main_page'].update_one({'_id': item.get('_id')},
                                                                   {'$set': data})
    else:
        updated_item = await create_new_item(conn, 'main_page', data)
    if updated_item:
        return True
    return False


async def get_main_page(conn: AsyncIOMotorClient) -> dict:
    item = await conn[DB_NAME]['main_page'].find_one()
    return item
