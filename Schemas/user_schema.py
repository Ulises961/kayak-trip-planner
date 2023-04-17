from marshmallow import Schema, fields, post_load
from Models.user import User
from Schemas.log_schema import LogSchema



class UserSchema(Schema):
    """ 
    User Schema
    used for loading/dumping User entities
    """

    id   = fields.Integer(allow_none=False)
    mail = fields.String(allow_none=False)
    pwd = fields.String(allow_none=False)
    phone = fields.Integer(allow_none=False)  
    name = fields.String(allow_none=False)  
    surname = fields.String(allow_none=False)  
    trip = fields.Integer(allow_none=False)  
    endorsed_logs = fields.List(fields.Nested(LogSchema), allow_none=True)  
    logs = fields.List(fields.Nested(LogSchema), allow_none=True )
    image = fields.Integer(allow_none=True)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)