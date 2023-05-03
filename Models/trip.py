from Api.database import db

class Trip (db.Model):
    def __init__(self, inventory, itinerary):
        self.inventory = inventory
        self.itinerary = itinerary
    id = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    inventory = db.relationship('Inventory', backref="trip_inventory", uselist=False)
    itinerary = db.relationship('Itinerary', backref="trip_itinerary", uselist=False)
    
