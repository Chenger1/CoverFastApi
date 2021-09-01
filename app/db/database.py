from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext

from ..config import ADMIN_EMAIL, ADMIN_NAME, ADMIN_PASSWORD, DB_NAME, MONGO_PATH


DB_URL = MONGO_PATH


class DataBase:
    """
    Problem with connect to db is a async loop. We cant just define AsyncIOMotorClient, because we will get
    error due to "task attached to a different loop". But also, we cant just define in main.py because
    or circular imports. So, this system helps to get db connection and use it in different handlers
    """
    client: AsyncIOMotorClient = None


db = DataBase()

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


async def get_database() -> AsyncIOMotorClient:
    return db.client


async def connect_to_db():
    db.client = AsyncIOMotorClient(DB_URL)
    user = await db.client[DB_NAME]['user'].find_one({'username': 'admin'})
    if not user:
        await db.client[DB_NAME]['user'].insert_one(
            {'username': ADMIN_NAME,
             'email': ADMIN_EMAIL,
             'password': get_password_hash(ADMIN_PASSWORD),
             'is_admin': True}
        )


async def close_connection():
    db.client.close()
