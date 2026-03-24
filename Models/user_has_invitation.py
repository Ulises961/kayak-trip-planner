from Api.database import db
from sqlalchemy import Date, Table, Column, UUID, ForeignKey

user_has_invitation = Table(
    'user_has_invitation',
    db.Model.metadata,
    Column('user_id', UUID, ForeignKey('users.id')),
    Column('trip_id', UUID, ForeignKey('trip.id')),
    Column('expiration_date', Date),
    extend_existing=True
)
   