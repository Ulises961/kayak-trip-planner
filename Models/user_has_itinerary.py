from Api.database import db
from sqlalchemy import Table, Column, Integer, ForeignKey

user_has_itinerary = Table(
    'user_has_itinerary',
    db.Model.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('itinerary_id', Integer, ForeignKey('itinerary.id')),
    extend_existing=True
)
   