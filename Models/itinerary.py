import uuid_extension
from Api.database import db
from sqlalchemy import UUID, Integer, Boolean, Numeric, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional, TYPE_CHECKING
from uuid import UUID as _UUID
from Models.base_model import BaseModel

if TYPE_CHECKING:
    from Models.day import Day


class Itinerary(BaseModel):
    is_public: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    total_miles: Mapped[Optional[Numeric]] = mapped_column(Numeric, nullable=True)
    expected_total_miles: Mapped[Optional[Numeric]] = mapped_column(
        Numeric, nullable=True
    )
    trip_id: Mapped[_UUID] = mapped_column(UUID, ForeignKey("trip.id"), nullable=False)
    user_id: Mapped[_UUID] = mapped_column(UUID, ForeignKey("users.id"), nullable=True)
    days: Mapped[List["Day"]] = relationship(
        lazy="select", cascade="all, delete,save-update"
    )


def __repr__(self):
    return f'<Itinerary "{self.id}, {self.days}, {self.trip_id}">'
