from Api.database import db
from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from Models.point import Point
from Models.weather import Weather
from Models.sea import Sea

class Day (db.Model):
    day_number = db.Column(db.Integer, primary_key = True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itinerary.id'), primary_key=True)
    date = db.Column(db.Date, primary_key = True)
    points:Mapped[Optional[List[Point]]] = db.relationship(backref='day')
    weather:Mapped[Optional[Weather]] = db.relationship(backref='day', uselist=False)
    sea:Mapped[Optional[Sea]] = db.relationship(backref='day', uselist=False)
    

    def __repr__(self):
        return f'<Day "{self.day_number}, Date {self.date}">'