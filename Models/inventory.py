from app import db, bcrypt

class Inventory(db.Model):

    id= db.Column('id', db.Integer, primary_key = True, autoincrement = "auto")
    
    