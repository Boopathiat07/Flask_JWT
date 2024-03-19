from factory import create_app
from flask import Blueprint, request
from api.service.response import response
from api.service.errorhandling import ErrorHandling

col = create_app.col
mongodb_view = Blueprint('mongodb_view', __name__,url_prefix='/api/v2')

@mongodb_view.route("/adduser", methods=['POST'])
def add_user():
    try:    
        data = request.get_json()
        name = data['name']
        email = data['email']
    
        user = {
            "name" : name,
            "email" : email
        }
        res = col.insert_one(user)
        return response.function("User Inserted SuccessFully")
    
    except:
        return ErrorHandling.handle_server_request("Server Busy")


@mongodb_view.route("/view", methods=['GET'])
def view_users():
    try:
        users = col.find()       
        user_list = []
        for res in users:
            user = {
            "name" : res['name'],
            "email" : res['email']
            }
            user_list.append(user)    
        return response.function(user_list)
    except:
        return ErrorHandling.handle_server_request("Server Busy")


@mongodb_view.route("/updateuser/<email>", methods=['PUT'])
def update_user(email):
    try:  
        data = request.get_json() 
        col.update_many({'email':email}, {'$set':data})  
        return response.function("User Updated SucessFully")
    except:
        return ErrorHandling.handle_server_request("Server Busy")


@mongodb_view.route("/delete/<email>", methods=['DELETE'])
def delete_user(email):
    try:
        col.delete_one({'email':email})
        return response.function("User Deleted SucessFully")
    except:
        return ErrorHandling.handle_server_request("Server Busy")


@mongodb_view.route("/viewbyid/<email>", methods=['GET'])
def view_user_by_id(email):
    try:
        user = col.find_one({'email':email})   
        user_list = {
            "name" : user['name'],
            "email" : user['email']
        }
        return response.function(user_list)
    except Exception as e:
        return ErrorHandling.handle_server_request(str(e))