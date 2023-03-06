from app import db
import enum

class PointType(enum.Enum):
    STOP = 'stop'
    POSITION = 'position'
    INTEREST = 'interest'

point_previous_next = db.Table(
    'point_previous_next',
    db.Column('previous_point_id', db.Integer, db.ForeignKey('point.id')),
    db.Column('next_point_id', db.Integer, db.ForeignKey('point.id'))
)

nearby_point = db.Table('point_is_nearby', 
    db.Column('nearby_point_id',db.Integer, db.ForeignKey('point.id'))
)


class Point (db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    gps = db.Column(db.Numeric)
    notes = db.Column(db.Text)
    type = enum.Enum(PointType)
    day_number = db.Column(db.Integer,db.ForeignKey('day.day_number'))
    date  = db.Column(db.Integer,db.ForeignKey('day.date'))
    itinerary_id  = db.Column(db.Integer,db.ForeignKey('day.itinerary_id'))
    previous  = db.relationship('Point',secondary=point_previous_next,backref='points')
    next = db.relationship('Point',secondary=point_previous_next,backref='points')
    nearby = db.relationship('Point',secondary=nearby_point,backref='points')
    images= db.relationship('Image', backref='point')
