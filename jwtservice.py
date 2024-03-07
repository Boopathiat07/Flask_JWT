import jwt
from datetime import datetime, timedelta
import uuid
from createApp import app, db
from dbModels import UserSession

uniqueId = str(uuid.uuid4())
logintime = datetime.utcnow()
def generate_access_token(user_id):  
    expires_in=3600
    payload = {
        'exp': datetime.utcnow() + timedelta(seconds=expires_in),
        'iat': logintime,
        'jti': uniqueId,
        'id': user_id,
    }
    

    usersession = UserSession(jti=uniqueId, logIn=logintime, user_id=user_id, logout=None, islogout=False)

    db.session.add(usersession)
    db.session.commit()
    return jwt.encode(payload, str(app.config['SECRET_KEY']), algorithm='HS256')

def generate_refresh_token(user_id):
    expires_in=86400
    payload = {
        'exp': datetime.utcnow() + timedelta(seconds=expires_in),
        'iat': logintime,
        'jti': uniqueId,
        'id': user_id,
    }
    return jwt.encode(payload, str(app.config['SECRET_KEY']), algorithm='HS256')