from Api.database import db
from sqlalchemy import UUID, Table, Column, Integer, ForeignKey

PointHasImage = Table(
    'point_has_image',
    db.Model.metadata,
    Column('image_id', UUID, ForeignKey('image.id'), primary_key=True),
    Column('point_id', UUID, ForeignKey('point.id'), primary_key=True),
    extend_existing=True
)
