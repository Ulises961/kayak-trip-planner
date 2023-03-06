from app import db

class Trip (db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    inventory = db.relationship('Inventory', backref="trip", uselist=False)
    itinerary = db.relationship('Itinerary', backref="trip", uselist=False)

