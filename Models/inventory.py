from database import db
from Models.inventory_items import inventory_items

class Inventory(db.Model):

    id= db.Column('id', db.Integer, primary_key = True, autoincrement = "auto")
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'))
    items = db.relationship('Item', secondary = inventory_items, backref='inventories')
    
    def __repr__(self):
        return f'<Inventory "{self.id}">'
