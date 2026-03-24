from Api.database import db
from sqlalchemy import UUID, Integer, String, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List, TYPE_CHECKING
from uuid import UUID as _UUID

if TYPE_CHECKING:
    from Models.weather_state import WeatherState


class Weather (db.Model):
    __table_args__ = (
        ForeignKeyConstraint(['day_id'],['day.id'], name="day_foreign_key_in_weather"),
    )
    day_id: Mapped[_UUID] = mapped_column(UUID, primary_key=True)
    model: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    weather_states: Mapped[List["WeatherState"]] = relationship(foreign_keys="WeatherState.day_id", cascade='all, delete,save-update')

    def __repr__(self):
        return f'<Weather "Day id {self.day_id}, Model {self.model} Weather states {self.weather_states}">'
