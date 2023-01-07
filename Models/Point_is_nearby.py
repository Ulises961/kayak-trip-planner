from app import db

nearby_point = db.Table('point_is_nearby', 
    db.Column('reference_point_id',db.Integer, db.ForeignKey('point.id'), primary_key=True),
    db.Column('nearb_point_id',db.Integer, db.ForeignKey('point.id'))

