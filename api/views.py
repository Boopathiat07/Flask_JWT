from create_app import db, bcrypt, redis_cache
from flask import Blueprint, request
from dbModels import user as User, user_session
from jwtservice import generate_access_token, generate_refresh_token,authenticate
from datetime import datetime
from response import response
from errorhandling import ErrorHandling

user_view= Blueprint('user', __name__, url_prefix='/api/v1/')

@user_view.route("/signup", methods=['POST'])
def user_signup():
    try:
        data = request.get_json()

        if data is None:
            return ErrorHandling.hanlde_bad_request("No Data found")
        

        if 'email' not in data or 'mobile' not in data or 'password' not in data or 'name' not in data:
            return ErrorHandling.hanlde_bad_request("required field should not be empty")

        email = data.get('email')
        mobile = data.get('mobile')
        password = data.get('password')
        name = data.get('name')
    
        hashed_pswd = bcrypt.generate_password_hash(password).decode('utf-8')
    
        new_user = User(email=email, mobile=mobile, password=hashed_pswd, name=name)
        db.session.add(new_user)
        db.session.commit()

        accessToken = generate_access_token(email)
        refreshToken = generate_refresh_token(email)

        token = {
            "accessToken" : accessToken, 
            "refreshToken" : refreshToken
        }
        return response.function(token)
    
    except Exception as e:
        db.session.rollback()
        return ErrorHandling.hanlde_bad_request("User Already exist")
    

@user_view.route("/login", methods = ['GET'])
def userLogin():
    try:
        data = request.get_json()
         
        email = str(data.get('email'))
        password = str(data.get('password'))
        try:
            user = db.get_or_404(User,email)
        except:
            return ErrorHandling.handle_not_found("No User Found")
        
        is_valid = bcrypt.check_password_hash(user.password, password)
        if is_valid:
            accessToken = generate_access_token(email)
            refreshToken = generate_refresh_token(email)
            token = {
            "accessToken" : accessToken, 
            "refreshToken" : refreshToken
            }

            return response.function(token)
        
        return ErrorHandling.hanlde_bad_request("Credentials Mismatch")

    except Exception as e:
        db.session.rollback()
        return ErrorHandling.handle_server_request(str(e))


@user_view.route("/logout", methods = ['GET'])
def userLogOut():
    jti_id = request.jtiID

    try:
        usersession = db.get_or_404(user_session, jti_id)
    except:
        return ErrorHandling.handle_not_found("No Session Found")

    usersession.islogout = True
    usersession.logout = datetime.utcnow()

    db.session.commit()

    return response.function("SuccessFully LoggedOut")


@user_view.route("/getprofile", methods = ['GET'])
def userprofile():
    user_id = request.current_user
    try:
        user = db.get_or_404(User, user_id)
    except:
        return ErrorHandling.handle_not_found("No User Found")
    result = {"email" : user.email, "mobile" : user.mobile}

    return response.function(result)


@user_view.route("/updateuser", methods = ['PUT'])
def updateProfile():
    data = request.get_json()

    user_id = request.current_user
    try:
        user = db.get_or_404(User, user_id)
    except:
        return ErrorHandling.handle_not_found("No User Found")
    
    user.name = data['name']

    db.session.commit()

    return response.function("Updated SuccessFully")


@user_view.route("/session", methods = ['GET'])
def userSession():
    usersession = db.session.execute(db.select(user_session)).scalars()

    users = [{"jti": row.jti, "logIn": row.logIn, "logout": row.logout, "user_id": row.user_id, "islogout": row.islogout} for row in usersession]

    return response.function(users)


@user_view.before_request
def jwt_authentication():
    authenticate()



