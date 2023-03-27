from marshmallow import Schema, fields, post_load
from Models.log import Log


class LogSchema(Schema):
    """ 
    Log Schema
    used for loading/dumping Log entities
    """

    id = fields.Integer(allow_none=True)
    hours =fields.Float(allow_none=False)
    avg_sea=fields.Float(allow_none=True)
    user_id=fields.Integer(allow_none=False)

    @post_load
    def make_log(self, data, **kwargs):
        return Log(**data)