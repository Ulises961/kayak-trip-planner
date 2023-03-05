
from app import db

class Sea (db.Model):
    day_number      = db.Column(db.Integer, db.ForeignKey('weather.day_number'), primary_key=True)
    itinerary_id    = db.Column(db.Integer, db.ForeignKey('weather.itinerary_id'), primary_key=True)
    date            = db.Column(db.Date,db.ForeignKey('weather.date'), primary_key=True)
    time           = db.Column(db.Time, primary_key=True)
    temperature    = db.Column(db.Numeric)
    precipitation  = db.Column(db.Numeric)
    wind_direction = db.Column(db.Numeric)
    wind_force     = db.Column(db.Numeric)
    cloud          = db.Column(db.String(255))
