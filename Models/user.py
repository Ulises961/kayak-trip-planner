from Api.database import db
from flask_bcrypt import generate_password_hash
from Models.user_has_trip import user_has_trip
from Models.user_endorses_log import user_endorses_log
from Models.user_has_profile_picture import userHasProfilePicture


class User(db.Model):
    __tablename__ = 'users'
    def __init__(self, mail, pwd, name, phone, **kwargs):
        self.mail = mail
        self.pwd = generate_password_hash(pwd).decode('UTF-8')
        self.phone = phone
        self.name = name
        self.__dict__.update(kwargs)

    id = db.Column('id', db.Integer, primary_key=True, autoincrement="auto")
    mail = db.Column(db.String(255), nullable=False, unique=True)
    pwd = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    surname = db.Column(db.String(255), nullable=True)
    trips = db.relationship('Trip', secondary=user_has_trip, backref="travellers")
    endorsed_logs = db.relationship(
        'Log', secondary=user_endorses_log, backref="user_endorsed_logs")
    logs = db.relationship('Log', backref="user_logs")
    image = db.relationship(
        'Image', secondary=userHasProfilePicture, backref=db.backref('user_picture', lazy=True))

    def __repr__(self):
        return f'<User "{self.mail}, {self.name}, {self.surname}">'
