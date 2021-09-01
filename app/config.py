from environs import Env

env = Env()
env.read_env()

SECRET_KEY = env.str('SECRET_KEY')
DB_NAME = env.str('DB_NAME')

ADMIN_EMAIL = env.str('ADMIN_EMAIL')
ADMIN_NAME = env.str('ADMIN_NAME')
ADMIN_PASSWORD = env.str('ADMIN_PASSWORD')
