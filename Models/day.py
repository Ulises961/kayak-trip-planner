from app import db

class Item (db.Model):
    day_number = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itinerary.id'), primary_key=True)
