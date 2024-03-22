import jwt 
from datetime import datetime, timedelta
import uuid
import os
from dotenv import load_dotenv
load_dotenv()

uniqueId = str(uuid.uuid4())
logintime = datetime.utcnow()
def generate_access_token(user_id):  
    expires_in=3600
    payload = {
        'exp': logintime + timedelta(seconds=expires_in),
        'iat': logintime,
        'jti': uniqueId,
        'id': user_id,
    }    
    return jwt.encode(payload,str(os.getenv('JWT_SECRET_KEY')), algorithm='HS256')

def generate_refresh_token(user_id):
    expires_in=86400
    payload = {
        'exp': logintime + timedelta(seconds=expires_in),
        'iat': logintime,
        'jti': uniqueId,
        'id': user_id,
    }
    return jwt.encode(payload, str(os.getenv('JWT_SECRET_KEY')), algorithm='HS256')
