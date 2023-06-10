from Api.database import db
from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from Models.point import Point
from Models.weather import Weather
from Models.sea import Sea
from sqlalchemy import UniqueConstraint

class Day (db.Model):
    __table_args__ = (
        UniqueConstraint("day_number", "itinerary_id", "date"),
    )
    id = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    day_number = db.Column(db.Integer)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itinerary.id'))
    date = db.Column(db.Date)
    points:Mapped[Optional[List[Point]]] = db.relationship(backref='day')
    weather:Mapped[Optional[Weather]] = db.relationship(backref='day', uselist=False, cascade='all, delete, delete-orphan,save-update')
    sea:Mapped[Optional[Sea]] = db.relationship(backref='day', uselist=False, cascade='all, delete, delete-orphan,save-update')
    

    def __repr__(self):
        return f'<Day "{self.day_number}, Date {self.date}, Itinerary {self.itinerary_id}">'
