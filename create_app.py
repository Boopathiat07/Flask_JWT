from flask import Flask
from config import SQLALCHEMY_DATABASE_URI, cluster
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
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
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

bcrypt = Bcrypt(app) 

db = SQLAlchemy(app)

MONGODB_CLUSTER=os.getenv('MONGODB_CLUSTER')
MONGODB_COLLECTION=os.getenv('MONGODB_COLLECTION')

data_base = cluster[MONGODB_CLUSTER]
col = data_base[MONGODB_COLLECTION]

app.config.from_object('config.Config') 
redis_cache = redis.Redis()



# logging.basicConfig(filename='cron.log', level=logging.DEBUG)

crontab = Crontab(app)
@crontab.job(minute="*/10")
def display():
    send_email()
    # logging.debug("Hello")
