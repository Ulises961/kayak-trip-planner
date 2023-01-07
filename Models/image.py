from app import db

class Image (db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    size = db.Column(db.Numeric)
    name = db.Column(db.String(255))
    location = db.Column(db.String(255))
