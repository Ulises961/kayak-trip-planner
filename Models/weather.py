from app import db

class Weather (db.Model):
    day_number = db.Column(db.Integer, primary_key=True)
    itinerary_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    time = db.Column(db.Time)
    model = db.Column(db.String(255))