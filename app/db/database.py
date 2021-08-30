import motor.motor_asyncio

DB_URL = 'mongodb://localhost:27017'

client = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)
database = client.cover

main_page_collection = database.get_collection('main_page_collection')
features_collection = database.get_collection('features_collection')
contacts_collection = database.get_collection('contacts_collection')
user_collection = database.get_collection('user_collection')


db_collections = {
    'main': main_page_collection,
    'features': features_collection,
    'contacts': contacts_collection,
    'user': user_collection
}
