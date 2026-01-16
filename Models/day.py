from sqlalchemy import UniqueConstraint, Integer, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Api.database import db
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from Models.point import Point
    from Models.weather import Weather
    from Models.sea import Sea
    from Models.itinerary import Itinerary


class Day(db.Model):
    __table_args__ = (
        UniqueConstraint("day_number", "itinerary_id", "date"),
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    day_number: Mapped[int] = mapped_column(Integer)
    itinerary_id: Mapped[int] = mapped_column(Integer, ForeignKey('itinerary.id'))
    date: Mapped[Date] = mapped_column(Date)
    
    # Relationships with proper Mapped[] syntax
    points: Mapped[Optional[List["Point"]]] = relationship(foreign_keys="Point.day_id")
    weather: Mapped[Optional["Weather"]] = relationship(foreign_keys="Weather.day_id", uselist=False, cascade='all,delete,save-update')
    sea: Mapped[Optional["Sea"]] = relationship(foreign_keys="Sea.day_id", uselist=False, cascade='all, delete,save-update')

    def __repr__(self):
        return f'<Day "{self.day_number}, Date {self.date}, Itinerary {self.itinerary_id}">'
