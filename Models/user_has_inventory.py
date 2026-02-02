from Api.database import db
from sqlalchemy import Table, Column, Integer, ForeignKey

user_has_inventory = Table(
    'user_has_inventory',
    db.Model.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('inventory_id', Integer, ForeignKey('inventory.id')),
    extend_existing=True
)
   