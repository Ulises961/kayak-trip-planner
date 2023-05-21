from marshmallow import fields, post_load
from Models.user import User
from Schemas.log_schema import LogSchema
from Schemas.trip_schema import TripSchema
from Schemas.image_schema import ImageSchema
from marshmallow_sqlalchemy import SQLAlchemySchema
from Api.database import db

class UserSchema(SQLAlchemySchema):
    """ 
    User Schema
    used for loading/dumping User entities
    """
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session

    id   = fields.Integer(allow_none=False)
    mail = fields.Email(allow_none=False)
    pwd = fields.String(allow_none=False)
    phone = fields.String(allow_none=False)  
    name = fields.String(allow_none=False)  
    surname = fields.String(allow_none=True)  
    trip = fields.Nested(TripSchema, allow_none=True)  
    endorsed_logs = fields.List(fields.Nested(LogSchema), allow_none=True)  
    logs = fields.List(fields.Nested(LogSchema), allow_none=True )
    image = fields.Nested(ImageSchema, allow_none=True)

    # @post_load
    # def make_user(self, data, **kwargs):
    #     return User(**data)