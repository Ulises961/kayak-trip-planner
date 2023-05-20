from Api.database import db
from typing import Optional
from typing import List
from sqlalchemy.orm import Mapped
from Models.weather_state import WeatherState


class Weather (db.Model):
    __table_args__ = (
        db.ForeignKeyConstraint(['day_number', 'itinerary_id', 'date'], [
                                'day.day_number', 'day.itinerary_id', 'day.date'], name="day_foreign_key_in_weather"),
    )
    day_number = db.Column(db.Integer, primary_key=True)
    itinerary_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    model = db.Column(db.String(255))
    weather_states: Mapped[Optional[List[WeatherState]]] = db.relationship(
        backref='weather', cascade='all, delete')

    def __repr__(self):
        return f'<Weather "Itinerary id {self.itinerary_id}, Date {self.date}, Day number {self.day_number}, Weather states {self.weather_states}">'
