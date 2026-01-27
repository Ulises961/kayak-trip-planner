from Api.database import db
from sqlalchemy import Table, Column, Integer, ForeignKey

userHasProfilePicture = Table(
    'user_has_profile_picture',
    db.Model.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('image_id ', Integer, ForeignKey('image.id')),
    extend_existing=True
)

