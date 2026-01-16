from Api.database import db
from sqlalchemy import Table, Column, Integer, ForeignKey

PointHasImage = Table('point_has_image', db.Model.metadata,
    Column('image_id', Integer, ForeignKey('image.id'), primary_key=True),
    Column('point_id', Integer, ForeignKey('point.id'), primary_key=True))
