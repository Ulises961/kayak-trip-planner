from Api.database import db
from sqlalchemy import Table, Column, Integer, ForeignKey

user_has_trip = Table(
    'user_has_trip',
    db.Model.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('trip_id', Integer, ForeignKey('trip.id')),
    extend_existing=True
)
   