from database import db

inventory_items = db.Table('inventory_items',
    db.Column('inventory_id', db.Integer, db.ForeignKey('inventory.id')),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id')))