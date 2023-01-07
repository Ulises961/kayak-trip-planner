
from app import db

class Sea (db.Model):
    day_number   = db.Column(db.Integer, primary_key=True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itinerary.id'), primary_key=True)
    date         = db.Column(db.Date, primary_key=True)
    moon_phase   = db.Column(db.String(255))
    high_tide    = db.Column(db.Time)
    low_tide     = db.Column(db.Time)
    