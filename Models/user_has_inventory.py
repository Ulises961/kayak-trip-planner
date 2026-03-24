from Api.database import db
from sqlalchemy import UUID, Table, Column, ForeignKey

user_has_inventory = Table(
    'user_has_inventory',
    db.Model.metadata,
    Column('user_id', UUID, ForeignKey('users.id')),
    Column('inventory_id', UUID, ForeignKey('inventory.id')),
    extend_existing=True
)
   