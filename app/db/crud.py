from bson import ObjectId

from typing import Optional

from .schema import LogInUser
from .database import AsyncIOMotorClient

from ..config import DB_NAME


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


async def delete_item(conn: AsyncIOMotorClient, id: str, collection: str) -> bool:
    result = await conn[DB_NAME][collection].delete_one({'_id': ObjectId(id)})
    return result


async def get_user_by_email(conn: AsyncIOMotorClient, email: str) -> Optional[LogInUser]:
    obj = await conn[DB_NAME]['user'].find_one({'email': email})
    schema = None
    if obj:
        schema = LogInUser(user_id=str(obj.get('_id')),
                           is_admin=obj.get('is_admin'),
                           password=obj.get('password'))
    return schema


async def get_features(conn: AsyncIOMotorClient, value: str) -> list[dict]:
    list_of_objects = []
    async for feature in conn[DB_NAME]['feature']\
            .find({'$or': [{'title': {'$regex': f'.*{value}.*', '$options': 'i'}},
                           {'text': {'$regex': f'.*{value}.*', '$options': 'i'}}]}):
        #  Search by title OR text
        list_of_objects.append(feature)

    return list_of_objects


async def update_item(conn: AsyncIOMotorClient, obj_id: str, collection: str,
                      data: dict) -> bool:
    updated_item = await conn[DB_NAME][collection].update_one({'_id': ObjectId(obj_id)},
                                                              {'$set': data})
    if updated_item:
        return True
    return False


async def update_singleton(conn: AsyncIOMotorClient, data: dict, collection: str) -> bool:
    item = await conn[DB_NAME][collection].find_one()
    if item:
        updated_item = await conn[DB_NAME][collection].update_one({'_id': item.get('_id')},
                                                                   {'$set': data})
    else:
        updated_item = await create_new_item(conn, collection, data)
    if updated_item:
        return True
    return False


async def get_singleton(conn: AsyncIOMotorClient, collection: str) -> dict:
    item = await conn[DB_NAME][collection].find_one()
    return item
