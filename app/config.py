from environs import Env

env = Env()
env.read_env()

SECRET_KEY = env.str('SECRET_KEY')
DB_NAME = env.str('DB_NAME')

ADMIN_EMAIL = env.str('ADMIN_EMAIL')
ADMIN_NAME = env.str('ADMIN_NAME')
ADMIN_PASSWORD = env.str('ADMIN_PASSWORD')

DEBUG = env.str('DEBUG')

if bool(int(DEBUG)):
    MONGO_PATH = 'mongodb://localhost:27017'
else:
    MONGO_PATH = env.str('MONGO_PATH')
