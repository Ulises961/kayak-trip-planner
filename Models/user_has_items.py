from Api.database import db
from sqlalchemy import Table, Column, Integer, ForeignKey

user_has_items = Table(
    'user_has_items',
    db.Model.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('item_id', Integer, ForeignKey('item.id')),
    extend_existing=True
)
   