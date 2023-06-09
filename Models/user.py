from Api.database import db
from flask_bcrypt import generate_password_hash
from Models.user_has_trip import user_has_trip
from Models.user_endorses_log import user_endorses_log
from Models.user_has_profile_picture import userHasProfilePicture
from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from Models.log import Log
from Models.image import Image
from Models.trip import Trip

class User(db.Model):
    __tablename__ = 'users'
    def __init__(self, pwd=None, endorsed_logs=[], logs=[], **kwargs):
        if pwd:
            self.pwd = generate_password_hash(pwd).decode('UTF-8')
            
        self.endorsed_logs = endorsed_logs
        self.logs = logs
        
        self.__dict__.update(kwargs)

    id = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    public_id = db.Column(db.String(255), nullable=False, unique=True)
    mail = db.Column(db.String(255), nullable=False, unique=True)
    pwd = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    surname = db.Column(db.String(255), nullable=True)
    trips : Mapped[Optional[List[Trip]]] = db.relationship(secondary=user_has_trip, backref="travellers")
    endorsed_logs : Mapped[Optional[List[Log]]] = db.relationship(
         secondary=user_endorses_log, backref="user_endorsed_logs")
    logs : Mapped[Optional[List[Log]]] = db.relationship(backref="user_logs")
    image:  Mapped[Optional[Image]]  = db.relationship(
        'Image', secondary=userHasProfilePicture, uselist=False, backref=db.backref('user_picture', lazy=True))

    def __repr__(self):
        return f'<User "{self.id} {self.mail}, {self.name}, {self.surname}, {self.pwd}">'
