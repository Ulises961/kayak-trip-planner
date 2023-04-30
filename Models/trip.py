from Api.database import db
from Models.user_has_trip import user_has_trip

class Trip (db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    inventory = db.relationship('Inventory', backref="trip_inventory", uselist=False)
    itinerary = db.relationship('Itinerary', backref="trip_itinerary", uselist=False)
    
