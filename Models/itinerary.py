from app import db

class Itinerary (db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    is_public = db.Column(db.Boolean, primary_key=False)
    total_miles = db.Column(db.Numeric, primary_key=False)
    expected_total_miles = db.Column(db.Numeric, primary_key=False) 

