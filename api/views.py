from createApp import db, app, bcrypt
from flask import Blueprint, request, jsonify
from dbModels import User, UserSession
from jwtservice import generate_access_token, generate_refresh_token
import jwt
from datetime import datetime

user_view = Blueprint('user', __name__)

@user_view.route("/user/signup", methods=['POST'])
def userSignup():   
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"message" : "No data Found"}), 404
        
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
        return jsonify({"message" : "User Added SuccessFully", "accessToken" : accessToken, "refreshToken" : refreshToken}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message" : str(e)}), 500


@user_view.route("/user/login", methods = ['GET'])
def userLogin():
    try:
        data = request.get_json()
    
        email = str(data.get('email'))
        password = str(data.get('password'))
        user = db.get_or_404(User, email)
        is_valid = bcrypt.check_password_hash(user.password, password)
        if is_valid:
            accessToken = generate_access_token(email)
            refreshToken = generate_refresh_token(email)
            return jsonify({"message" : "Successfully LoggedIn","accessToken" : accessToken, "refreshToken" : refreshToken}), 200
        
        return jsonify({"message" : "Credentials Mismatch"}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"message" : str(e)}), 500


@user_view.route("/logout", methods = ['GET'])
def userLogOut():
    jti_id = request.jtiID

    usersession = db.get_or_404(UserSession, jti_id)

    usersession.islogout = True
    usersession.logout = datetime.utcnow()

    db.session.commit()

    return jsonify({"message": "SuccessFully LoggedOut"}),200


@user_view.route("/getprofile", methods = ['GET'])
def userprofile():
    user_id = request.current_user
    user = db.get_or_404(User, user_id)
    result = {"email" : user.email, "mobile" : user.mobile}

    return jsonify(result), 200


@user_view.route("/updateuser", methods = ['PUT'])
def updateProfile():
    data = request.get_json()

    user_id = request.current_user
    user = db.get_or_404(User, user_id)
    
    user.name = data['name']

    db.session.commit()

    return jsonify({"message" : "User Updated SuccessFully"}), 200


@user_view.route("/user/session", methods = ['GET'])
def userSession():
    usersession = db.session.execute(db.select(UserSession)).scalars()

    users = [{"jti": row.jti, "logIn": row.logIn, "logout": row.logout, "user_id": row.user_id, "islogout": row.islogout} for row in usersession]

    return jsonify(users), 200








@app.before_request
def authenticate():

    auth_exempt_routes = ['/user/login', '/user/session', '/user/signup']

    if request.path in auth_exempt_routes:
        return
    
    token = request.headers.get('Authorization').split(" ")[1]
    if not token:
        return jsonify({'message': 'Missing token'}), 401
    
    try:
        data = jwt.decode(token, str(app.config['SECRET_KEY']), algorithms=['HS256'])

        jti_id = data['jti']
        user_id = data['id']
        
        db.get_or_404(User, user_id)
        print("hello world @!")
        userSession = db.get_or_404(UserSession, jti_id)

        print(userSession.islogout)
        if userSession.islogout == True:
            print("logged out")
            return jsonify({'message' : 'Session Expired'}), 400

    except Exception as e:
        return jsonify({'message':str(e)}), 401

    request.current_user = user_id
    request.jtiID = jti_id


