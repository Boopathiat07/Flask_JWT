from flask import request
from config import Session
from models.db_models import User
from response.errorhandling import ErrorHandling
import jwt
from config import Session

import os
from dotenv import load_dotenv
load_dotenv()


http_methods = {'POST','PUT','DELETE'}

def jwt_authentication():
    try:
        auth_exempt_routes = ['/api/v1/login', '/api/v1/signup']

        if request.path in auth_exempt_routes:
            return
        
        barear_token = request.headers.get('Authorization')

        if barear_token is None:
            raise Exception("No Token Found")

        token = barear_token.split(" ")[1]
        if not token:
            return ErrorHandling.handle_unauthorize("Missing Token")
        
        try:
            data = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])

            jti_id = data['jti']
            user_id = data['id']
            session = Session()
            try:
                session.query(User).filter_by(email=user_id).one()
            except:
                return ErrorHandling.handle_not_found("No User Found")

        except Exception as e:
            return ErrorHandling.handle_unauthorize("Invalid Token")

        request.current_user = user_id
        request.jtiID = jti_id
        res = rbac_authenticate()
        return res
    except Exception as e:
        return ErrorHandling.handle_forbidden(str(e))
    
def rbac_authenticate():
    try:    
        data = request.get_json()

        email = data['email']
        
        api_name = request.path
        http_method = request.method
        
        session = Session()
        user = session.query(User).filter_by(email=email).one()
        groups = user.group    
        apis = groups.apis
        try:
            if len(apis) == 0:
                raise Exception("No Service For You")
        except Exception as e:
            return ErrorHandling.handle_unauthorize(str(e))
        
        for i in apis:
            try:
                print(i.base_path, api_name)
                if(i.base_path == api_name):
                    if user.is_writable == False:
                        try:
                            if http_method != 'GET':
                                raise Exception("unauthorized")
                        except Exception as e:
                            return ErrorHandling.handle_unauthorize(str(e))
                else:
                    raise Exception("No Service For you")
            except Exception as e:
                return ErrorHandling.handle_forbidden(str(e))
            
    except Exception as e: 
        return ErrorHandling.hanlde_bad_request("No user Found")


