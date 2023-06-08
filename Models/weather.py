from Api.database import db
from typing import Optional
from typing import List
from sqlalchemy.orm import Mapped
from Models.weather_state import WeatherState


class Weather (db.Model):
    __table_args__ = (
        db.ForeignKeyConstraint(['day_id'],['day.id'], name="day_foreign_key_in_weather"),
    )
    day_id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(255))
    weather_states: Mapped[Optional[List[WeatherState]]] = db.relationship(
        backref='weather', cascade='all, delete, delete-orphan,save-update')

    def __repr__(self):
        return f'<Weather "Day id {self.day_id}, Model {self.model} Weather states {self.weather_states}">'
