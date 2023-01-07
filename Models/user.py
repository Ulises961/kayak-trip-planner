from app import db, bcrypt

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
    
    
    
    