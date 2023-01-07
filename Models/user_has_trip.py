from app import db

class UserHasTrip (db.Model):    
    user_id      = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), primary_key=True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itinerary.id'), primary_key=True)
