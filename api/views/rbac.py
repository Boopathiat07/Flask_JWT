from flask import Blueprint, request
from response.response import response
from config import Session
from models.db_models import User, Group, Api
from response.errorhandling import ErrorHandling
from validation.validator import *
session = Session()

rbac_view = Blueprint("rbac_view", __name__, url_prefix="/rbac/api/v2")

@rbac_view.route("/user_group",methods = ['PUT'])
def add_group_to_user():
    try:
        data = request.get_json()    
        schema = UserGroup()
        try:
            schema.load(data)  
        except Exception as e:
            return ErrorHandling.hanlde_bad_request(str(e))
        email = data['email']
        grp_name = data['grp_name']

        user = session.query(User).filter_by(email=email).first()
        group = session.query(Group).filter_by(grp_name=grp_name).one()
    
        user.group_id = group.id
        session.commit()

        return response.function(f"User Added to the {grp_name}")
    except Exception as e:
        return ErrorHandling.hanlde_bad_request(str(e))

@rbac_view.route("/api_group",methods = ['POST'])
def add_api_to_group():
    try:
        data = request.get_json()
        schema = ApiGroup()
        try:
            schema.load(data)  
        except Exception as e:
            return ErrorHandling.hanlde_bad_request(str(e))
        base_path = data['base_path']
        grp_name = data['grp_name']
        
        api = session.query(Api).filter_by(base_path=base_path).one()

        group = session.query(Group).filter_by(grp_name=grp_name).one()

        api.groups.append(group)
        group.apis.append(api)
        session.commit()

        return response.function(f"api added to this {grp_name} group")
    except Exception as e:
        return ErrorHandling.hanlde_bad_request(str(e))


@rbac_view.route("/grant_permission", methods=['PUT'])
def grant_permission():
    try:
        data = request.get_json()
        schema = GrantPermission()
        try:
            schema.load(data)  
        except Exception as e:
            return ErrorHandling.hanlde_bad_request(str(e))
        email = data['email']
        
        user = session.query(User).filter_by(email=email).one() 

        user.is_writable = True

        session.commit()
        
        return response.function(f"User granted Permission to write")
    except Exception as e:
        return ErrorHandling.hanlde_bad_request(str(e))


@rbac_view.route("/add_group", methods =['POST'])
def add_group():
    try:
        data = request.get_json()
        schema = AddGroup()
        try:
            schema.load(data)  
        except Exception as e:
            return ErrorHandling.hanlde_bad_request(str(e))
        grp_name = data['grp_name']
    
        groups = Group(grp_name=grp_name)

        session = Session()
        session.add(groups)
        session.commit()
        session.close()

        return response.function("New Group {grp_name} added") 
    except Exception as e:
        return ErrorHandling.hanlde_bad_request(str(e))