from flask import Flask
from config import SQLALCHEMY_DATABASE_URI, cluster, Config, SQLALCHEMY_ST_DATABASE_URI
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_caching import Cache
import os
from dotenv import load_dotenv
import redis
from flask_crontab import Crontab
from api.smtp_service import send_email
# import logging

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('APP_SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

app.config['SQLALCHEMY_BINDS'] = {'slave' : SQLALCHEMY_DATABASE_URI,
                                  'spatial_db' : SQLALCHEMY_ST_DATABASE_URI}


app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

bcrypt = Bcrypt(app) 

db = SQLAlchemy(app)

MONGODB_CLUSTER=os.getenv('MONGODB_CLUSTER')
MONGODB_COLLECTION=os.getenv('MONGODB_COLLECTION')

data_base = cluster[MONGODB_CLUSTER]
col = data_base[MONGODB_COLLECTION]

app.config.from_object(Config) 
redis_cache = redis.Redis(host=Config.CACHE_REDIS_HOST, port=Config.CACHE_REDIS_PORT,db=Config.CACHE_REDIS_DB)

# cache = Cache(config={'CACHE_TYPE': 'redis'})

cache = Cache(app)

# logging.basicConfig(filename='cron.log', level=logging.DEBUG)

crontab = Crontab(app)
@crontab.job(minute="*/10")
def display():
    send_email()
    # logging.debug("Hello")
