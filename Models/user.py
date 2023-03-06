from app import db, bcrypt
from Models.user_has_trip import user_has_trip
from Models.user_endorses_log import user_endorses_log
class User(db.Model):

    def __init__(self, mail, password):
        self.mail = mail
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')

    id= db.Column('id', db.Integer, primary_key = True, autoincrement = "auto")
    mail = db.Column(db.String(255), nullable=False, unique=True)
    pwd = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    surname = db.Column(db.String(255))
    trips = db.relationship('Trip', secondary=user_has_trip, backref="users")
    endorsed_logs = db.relationship('Log', secondary=user_endorses_log, backref="endorsers")
    logs = db.relationship('Log', backref="user")
    
    def __repr__(self):
        return f'<User "{self.mail}, {self.name}, {self.surname}">'

    