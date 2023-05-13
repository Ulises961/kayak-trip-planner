from Api.database import db
import enum
from Models.point_has_image import PointHasImage


class PointType(enum.Enum):
    STOP = 'stop'
    POSITION = 'position'
    INTEREST = 'interest'


point_next_to = db.Table(
    'point_previous_next',
    db.Column('previous_point_id', db.Integer, db.ForeignKey('point.id')),
    db.Column('next_point_id', db.Integer, db.ForeignKey('point.id'))
)

nearby_point = db.Table('point_is_nearby',
                        db.Column('nearby_point_id', db.Integer,
                                  db.ForeignKey('point.id'))
                        )


class Point (db.Model):
    __table_args__ = (
        db.ForeignKeyConstraint(['day_number','itinerary_id','date'],['day.day_number','day.itinerary_id','day.date'], name="day_foreign_key_in_point"),
    )
    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    gps = db.Column(db.Numeric)
    notes = db.Column(db.Text)
    type = db.Column(db.Enum(PointType))
    day_number = db.Column(db.Integer)
    date = db.Column(db.Date)
    itinerary_id = db.Column(db.Integer)
    previous = db.Column(db.Integer, db.ForeignKey('point.id'))
    next =  db.Column(db.Integer, db.ForeignKey('point.id'))
    nearby = db.relationship('Point', secondary=nearby_point, backref='points')
    images = db.relationship('Image', secondary=PointHasImage,
                             lazy="subquery", backref=db.backref('point', lazy=True))

    def __repr__(self):
        return f'<Point "{self.gps}, type {self.type}">'
