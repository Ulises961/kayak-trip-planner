from sqlalchemy import UUID, UniqueConstraint, Integer, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional, TYPE_CHECKING

from Models.base_model import BaseModel
from uuid import UUID as _UUID

if TYPE_CHECKING:
    from Models.point import Point
    from Models.weather import Weather
    from Models.sea import Sea
    from Models.itinerary import Itinerary


class Day(BaseModel):
    __table_args__ = (UniqueConstraint("day_number", "itinerary_id", "date"),)

    day_number: Mapped[int] = mapped_column(Integer)
    itinerary_id: Mapped[_UUID] = mapped_column(UUID, ForeignKey("itinerary.id"))
    date: Mapped[Date] = mapped_column(Date)

    # Relationships with proper Mapped[] syntax
    points: Mapped[Optional[List["Point"]]] = relationship(foreign_keys="Point.day_id")
    weather: Mapped[Optional["Weather"]] = relationship(
        foreign_keys="Weather.day_id", uselist=False, cascade="all,delete,save-update"
    )
    sea: Mapped[Optional["Sea"]] = relationship(
        foreign_keys="Sea.day_id", uselist=False, cascade="all, delete,save-update"
    )

    def __repr__(self):
        return f'<Day "{self.day_number}, Date {self.date}, Itinerary {self.itinerary_id}">'
