from motor.motor_asyncio import AsyncIOMotorClient


DB_URL = 'mongodb://localhost:27017'


class DataBase:
    """
    Problem with connect to db is a async loop. We cant just define AsyncIOMotorClient, because we will get
    error due to "task attached to a different loop". But also, we cant just define in main.py because
    or circular imports. So, this system helps to get db connection and use it in different handlers
    """
    client: AsyncIOMotorClient = None


db = DataBase()


async def get_database() -> AsyncIOMotorClient:
    return db.client


async def connect_to_db():
    db.client = AsyncIOMotorClient(DB_URL)


async def close_connection():
    db.client.close()
