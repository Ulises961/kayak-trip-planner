from app import db

class InventoryHasItem (db.Model):
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), primary_key=True )
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)

