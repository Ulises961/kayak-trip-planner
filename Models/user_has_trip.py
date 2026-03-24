from Api.database import db
from sqlalchemy import Table, Column, UUID, ForeignKey

user_has_trip = Table(
    'user_has_trip',
    db.Model.metadata,
    Column('user_id', UUID, ForeignKey('users.id')),
    Column('trip_id', UUID, ForeignKey('trip.id')),
    extend_existing=True
)
   