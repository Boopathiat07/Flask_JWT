import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

USER_NAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
DB_NAME = os.getenv("DB_NAME")
SPATIAL_DB_NAME = os.getenv("SPATIAL_DB_NAME")

SQLALCHEMY_DATABASE_URI = f"mysql://{USER_NAME}:{PASSWORD}@{HOST}/{DB_NAME}"

SQLALCHEMY_ST_DATABASE_URI = f"mysql://{USER_NAME}:{PASSWORD}@{HOST}/{SPATIAL_DB_NAME}"

MONGODB_URI = os.getenv('MONGODB_URI')

cluster = MongoClient(MONGODB_URI)

class Config(object):
    CACHE_TYPE = os.environ['CACHE_TYPE']
    CACHE_REDIS_HOST = os.environ['CACHE_REDIS_HOST']
    CACHE_REDIS_PORT = os.environ['CACHE_REDIS_PORT']
    CACHE_REDIS_DB = os.environ['CACHE_REDIS_DB']

    print(CACHE_REDIS_DB, CACHE_REDIS_HOST, CACHE_REDIS_PORT, CACHE_TYPE)

    # CACHE_REDIS_URL = os.environ['CACHE_REDIS_URL']
    # CACHE_DEFAULT_TIMEOUT = os.environ['CACHE_DEFAULT_TIMEOUT']