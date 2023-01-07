from app import db

class PointHasImage (db.Model):
    image_id   = db.Column(db.Integer, db.ForeignKey('image.id'), primary_key=True)
    point_id = db.Column(db.Integer, db.ForeignKey('point.id'), primary_key=True)
