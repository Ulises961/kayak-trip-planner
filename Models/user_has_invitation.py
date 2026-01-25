from Api.database import db
from sqlalchemy import Date, Table, Column, Integer, ForeignKey

user_has_invitation = Table('user_has_trip', db.Model.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('trip_id', Integer, ForeignKey('trip.id')),
    Column('expiration_date', Date)
    )
   