from app import db

class Itinerary (db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    is_public = db.Column(db.Boolean)
    total_miles = db.Column(db.Numeric)
    expected_total_miles = db.Column(db.Numeric)
    days = db.relationship('Day', backref='itinerary')
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)

def __repr__(self):
        return f'<Itinerary "{self.id}, {self.days}, {self.trip_id}">'
