from app import db

class Weather (db.Model):
    day_number   = db.Column(db.Integer, db.ForeignKey('day.day_number'), primary_key=True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('day.itinerary_id'), primary_key=True)
    date = db.Column(db.Date, db.ForeignKey('day.date'),primary_key=True)
    time = db.Column(db.Time)
    model = db.Column(db.String(255))