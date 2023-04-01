
from database import db

class Sea (db.Model):
    day_number   = db.Column(db.Integer, db.ForeignKey('day.day_number'), primary_key=True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('day.itinerary_id'), primary_key=True)
    date         = db.Column(db.Date, db.ForeignKey('day.date'),primary_key=True)
    moon_phase   = db.Column(db.String(255))
    high_tide    = db.Column(db.Time)
    low_tide     = db.Column(db.Time)
    