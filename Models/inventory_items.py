from Api.database import db
from sqlalchemy import Table, Column, Integer, ForeignKey

inventory_items = Table(
    'inventory_items',
    db.Model.metadata,
    Column('inventory_id', Integer, ForeignKey('inventory.id')),
    Column('item_id', Integer, ForeignKey('item.id')),
    extend_existing=True
)