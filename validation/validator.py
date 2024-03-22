from marshmallow import Schema, fields

class LoginSchema(Schema):
    email = fields.Email(required=True)