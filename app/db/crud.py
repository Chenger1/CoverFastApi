from bson.objectid import ObjectId

from database import db_collections


async def retrieve_from_collections(collection: str) -> list[dict]:
    objects = []
    async for obj in db_collections[collection].find():
        objects.append(obj)
    return objects


async def retrieve_data(id: str, collection: str) -> dict:
    obj = await db_collections[collection].find_one({'_id': ObjectId(id)})
    return obj
