from Api.database import db
from sqlalchemy import Integer, Time, Numeric, String, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from Models.weather import Weather

class WeatherState (db.Model):
    __table_args__ = (
        ForeignKeyConstraint(['day_id'], ['weather.day_id'], name="weather_day_foreign_keys_in_weather_state"),
    )
    day_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    time: Mapped[Time] = mapped_column(Time, primary_key=True)
    temperature: Mapped[Optional[Numeric]] = mapped_column(Numeric, nullable=True)
    precipitation: Mapped[Optional[Numeric]] = mapped_column(Numeric, nullable=True)
    wind_direction: Mapped[Optional[Numeric]] = mapped_column(Numeric, nullable=True)
    wind_force: Mapped[Optional[Numeric]] = mapped_column(Numeric, nullable=True)
    cloud: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)


    def __repr__(self):
        return f'<Weather state " time {self.time}, temperature {self.temperature}, wind direction {self.wind_direction}, wind force {self.wind_force}">'
