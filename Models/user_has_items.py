from Api.database import db
from sqlalchemy import Table, Column, UUID, ForeignKey

user_has_items = Table(
    'user_has_items',
    db.Model.metadata,
    Column('user_id', UUID, ForeignKey('users.id')),
    Column('item_id', UUID, ForeignKey('item.id')),
    extend_existing=True
)
   