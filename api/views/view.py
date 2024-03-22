from config import Session
from flask import Blueprint, request
from models.db_models import User, Group, Api
from response.response import response
from response.errorhandling import ErrorHandling
from validation.validator import LoginSchema, AddUserSchema
from service.jwt_service import generate_access_token, generate_refresh_token

view = Blueprint("view", __name__ , url_prefix="/api/v1")
session = Session()

@view.route("/login")
def login():
    try:
        data = request.get_json()
        schema = LoginSchema()
        try:
            schema.load(data)  
        except Exception as e:
            return ErrorHandling.hanlde_bad_request(str(e))
        email = data['email']
        
        try:
            user = session.query(User).filter_by(email=email).one()
            accessToken = generate_access_token(email)
            refreshToken = generate_refresh_token(email)
            token = {
            "accessToken" : accessToken, 
            "refreshToken" : refreshToken
            }
        except Exception as e:
            return ErrorHandling.hanlde_bad_request(str(e))
        
        return token
    except Exception as e:
        return ErrorHandling.handle_server_request(str(e))

@view.route("/add_user",methods = ['POST'])
def add_user():
    data = request.get_json()
    schema = AddUserSchema()
    try:
        schema.load(data)  
    except Exception as e:
        return ErrorHandling.hanlde_bad_request(str(e))
    
    username = data['name']
    email = data['emal']
    is_writable = False    
    user = User(username=username, email=email, is_writable=is_writable)
    session.add(user)
    session.commit()
    return response.function("User Added") 

