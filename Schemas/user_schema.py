from marshmallow import Schema, fields, post_load
from Models.user import User
from Schemas.log_schema import LogSchema
from Schemas.trip_schema import TripSchema
from Schemas.image_schema import ImageSchema

class UserSchema(Schema):
    """ 
    User Schema
    used for loading/dumping User entities
    """

    id   = fields.Integer(allow_none=False)
    public_id = fields.String(allow_none=False)
    mail = fields.Email(allow_none=True)
    pwd = fields.String(allow_none=True)
    phone = fields.String(allow_none=True)  
    name = fields.String(allow_none=True)  
    surname = fields.String(allow_none=True)  
    trip = fields.Nested(TripSchema, allow_none=True)  
    endorsed_logs = fields.List(fields.Nested(LogSchema), allow_none=True)  
    logs = fields.List(fields.Nested(LogSchema), allow_none=True )
    image = fields.Nested(ImageSchema, allow_none=True)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)