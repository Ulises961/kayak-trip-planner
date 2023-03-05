from app import db

class Day (db.Model):
    day_number = db.Column(db.Integer)
    date = db.Column(db.Date)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itinerary.id'))
    points = db.relationship('Point', backref='day')
    id = db.Column(db.Integer, primary_key=True)
    def __repr__(self):
        return f'<Day "{self.title}">'
