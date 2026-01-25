from Api.database import db
from sqlalchemy import Integer, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from Models.day import Day
    from Models.trip import Trip


class Itinerary (db.Model):

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    is_public: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    total_miles: Mapped[Optional[Numeric]] = mapped_column(Numeric, nullable=True)
    expected_total_miles: Mapped[Optional[Numeric]] = mapped_column(Numeric, nullable=True)
    trip_id: Mapped[int] = mapped_column(Integer, ForeignKey('trip.id'), nullable=False)
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable= True)
    days: Mapped[List["Day"]] = relationship(lazy='select', cascade='all, delete,save-update')


def __repr__(self):
    return f'<Itinerary "{self.id}, {self.days}, {self.trip_id}">'
