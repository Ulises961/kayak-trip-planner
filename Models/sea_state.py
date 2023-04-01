from database import db

class SeaState (db.Model):
    day_number      = db.Column(db.Integer, db.ForeignKey('sea.day_number'), primary_key=True)
    itinerary_id    = db.Column(db.Integer, db.ForeignKey('sea.itinerary_id'), primary_key=True)
    date            = db.Column(db.Date,db.ForeignKey('sea.date'), primary_key=True)
    time            = db.Column(db.Time, primary_key=True)
    wave_height     = db.Column(db.Numeric)
    wave_direction  = db.Column(db.Numeric)
    swell_direction = db.Column(db.Numeric)
    swell_period    = db.Column(db.Numeric)