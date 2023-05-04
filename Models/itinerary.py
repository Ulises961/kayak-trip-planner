from Api.database import db
from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from Models.day import Day


class Itinerary (db.Model):
    def __init__(self, is_public, total_miles, days = []):
        self.is_public = is_public
        self.total_miles = total_miles
        self.days = days
    id = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    is_public = db.Column(db.Boolean)
    total_miles = db.Column(db.Numeric)
    expected_total_miles = db.Column(db.Numeric)
    days: Mapped[Optional[List[Day]]] = db.relationship(backref='itinerary')
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)


def __repr__(self):
    return f'<Itinerary "{self.id}, {self.days}, {self.trip_id}">'
