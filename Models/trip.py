

from app import db

class Trip (db.Model):
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), primary_key=True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itinerary.id'), primary_key=True)
