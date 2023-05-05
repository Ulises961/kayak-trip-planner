from Api.database import db
from typing import Optional
from typing import List
from sqlalchemy.orm import Mapped
from Models.weather_state import WeatherState

class Weather (db.Model):
    __table_args__ = (
        db.ForeignKeyConstraint(['day_number','itinerary_id','date'],['day.day_number','day.itinerary_id','day.date'], name="day_primary_key_in_weather"),
    )
    day_number   = db.Column(db.Integer, primary_key=True)
    itinerary_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date,primary_key=True)
    time = db.Column(db.Time)
    model = db.Column(db.String(255))
    weather_states: Mapped[Optional[List[WeatherState]]]
      
    def __repr__(self):
        return f'<Weather "{self.time}, Itinerary id {self.itinerary_id}, date {self.date}, day number {self.day_number}">'

    