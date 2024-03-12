import jwt
from datetime import datetime, timedelta
import uuid
from create_app import app, db
from dbModels import user_session, master as user
from flask import request
from errorhandling import ErrorHandling


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

    usersession = user_session(jti=uniqueId, logIn=logintime, user_id=user_id, logout=None, islogout=False)

    db.session.add(usersession)
    db.session.commit()
    return jwt.encode(payload, str(app.config['SECRET_KEY']), algorithm='HS256')

def generate_refresh_token(user_id):
    expires_in=86400
    payload = {
        'exp': logintime + timedelta(seconds=expires_in),
        'iat': logintime,
        'jti': uniqueId,
        'id': user_id,
    }
    return jwt.encode(payload, str(app.config['SECRET_KEY']), algorithm='HS256')


def authenticate():

    auth_exempt_routes = ['/api/v1/login', '/api/v1/session', '/api/v1/signup']

    if request.path in auth_exempt_routes:
        return
    
    token = request.headers.get('Authorization').split(" ")[1]
    if not token:
        return ErrorHandling.handle_unauthorize("Missing Token")
    
    try:
        data = jwt.decode(token, str(app.config['SECRET_KEY']), algorithms=['HS256'])

        jti_id = data['jti']
        user_id = data['id']

        try:
            existing_user = db.get_or_404(user, user_id)
        except:
            return ErrorHandling.handle_not_found("No User Found")
        
        try:
            userSession = db.get_or_404(user_session, jti_id)
        except:
            return ErrorHandling.handle_not_found("No Session Found")

        if userSession.islogout == True:
            return ErrorHandling.hanlde_bad_request("Session Expired")

    except Exception as e:
        return ErrorHandling.handle_unauthorize("Invalid Token")

    request.current_user = user_id
    request.jtiID = jti_id
