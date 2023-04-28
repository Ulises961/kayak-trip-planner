
from database import db

class Sea (db.Model):
    __table_args__ = (
        db.ForeignKeyConstraint(['day_number','itinerary_id','date'],['day.day_number','day.itinerary_id','day.date'], name="day_primary_key_in_sea"),
    )
    day_number   = db.Column(db.Integer, primary_key=True)
    itinerary_id = db.Column(db.Integer,  primary_key=True)
    date         = db.Column(db.Date,primary_key=True)
    moon_phase   = db.Column(db.String(255))
    high_tide    = db.Column(db.Time)
    low_tide     = db.Column(db.Time)
    