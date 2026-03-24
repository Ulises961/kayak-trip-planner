from Api.database import db
from sqlalchemy import Table, Column, ForeignKey, UUID

inventory_items = Table(
    'inventory_items',
    db.Model.metadata,
    Column('inventory_id', UUID, ForeignKey('inventory.id')),
    Column('item_id', UUID, ForeignKey('item.id')),
    extend_existing=True
)