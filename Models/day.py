from Api.database import db

class Day (db.Model):
    day_number = db.Column(db.Integer, primary_key = True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itinerary.id'), primary_key=True)
    date = db.Column(db.Date, primary_key = True)
    points = db.relationship('Point', backref='day')
    

    def __repr__(self):
        return f'<Day "{self.day_number}, Date {self.date}">'
