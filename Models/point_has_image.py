from database import db

PointHasImage = db.Table('point_has_image',
                         db.Column('image_id', db.Integer, db.ForeignKey(
                             'image.id'), primary_key=True),
                         db.Column('point_id', db.Integer, db.ForeignKey('point.id'), primary_key=True))
