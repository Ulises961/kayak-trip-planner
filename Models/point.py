import uuid_extension

from Api.database import db
from sqlalchemy import UUID, Integer, Numeric, String, Text, Enum, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from Models.base_model import BaseModel
from Models.point_has_image import PointHasImage
from typing import Optional, List, TYPE_CHECKING
from uuid import UUID as _UUID

if TYPE_CHECKING:
    from Models.image import Image

class PointType(enum.Enum):
    STOP = 'stop'
    POSITION = 'position'
    INTEREST = 'interest'

class Point (BaseModel):
    __table_args__ = (
        ForeignKeyConstraint(['day_id'],['day.id'], name="day_foreign_key_in_point"),
    )

    latitude: Mapped[Optional[Numeric]] = mapped_column(Numeric, nullable=True)
    longitude: Mapped[Optional[Numeric]] = mapped_column(Numeric, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    type: Mapped[Optional[PointType]] = mapped_column(Enum(PointType), nullable=True)
    day_id: Mapped[Optional[_UUID]] = mapped_column(UUID, nullable=True)
    next_id: Mapped[Optional[_UUID]] = mapped_column(UUID, ForeignKey('point.id'), nullable=True)

    next: Mapped[Optional['Point']] = relationship(
        'Point',
        foreign_keys=[next_id],
    remote_side='Point.id',  # Use string reference instead
    uselist=False
)
    images: Mapped[List["Image"]] = relationship(secondary=PointHasImage, lazy="subquery", cascade='all, delete')

    def __repr__(self):
        return f'<Point "({self.latitude}, {self.longitude}), type {self.type}">'
