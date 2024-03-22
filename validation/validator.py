from marshmallow import Schema, fields

class LoginSchema(Schema):
    email = fields.Email(required=True)

class AddUserSchema(Schema):
    email = fields.Email(required=True)
    name = fields.String(required=True)

class UserGroup(Schema):
    email =fields.Email(required = True)
    grp_name = fields.String(required=True)

class ApiGroup(Schema):
    base_path =fields.String(required = True)
    grp_name = fields.String(required=True)

class GrantPermission(Schema):
    email = fields.Email(required=True)

class AddGroup(Schema):
    grp_name = fields.String(required=True)