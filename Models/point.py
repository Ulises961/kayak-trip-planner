from Api.database import db
from sqlalchemy import Integer, Numeric, Text, Enum, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from Models.point_has_image import PointHasImage
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from Models.image import Image
    from Models.day import Day

class PointType(enum.Enum):
    STOP = 'stop'
    POSITION = 'position'
    INTEREST = 'interest'

class Point (db.Model):
    __table_args__ = (
        ForeignKeyConstraint(['day_id'],['day.id'], name="day_foreign_key_in_point"),
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    latitude: Mapped[Optional[Numeric]] = mapped_column(Numeric, nullable=True)
    longitude: Mapped[Optional[Numeric]] = mapped_column(Numeric, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    type: Mapped[Optional[PointType]] = mapped_column(Enum(PointType), nullable=True)
    day_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    next_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('point.id'), nullable=True)

    next: Mapped[Optional['Point']] = relationship('Point', foreign_keys=[next_id], remote_side=[id], uselist=False)
    images: Mapped[List["Image"]] = relationship(secondary=PointHasImage, lazy="subquery", cascade='all, delete')

    def __repr__(self):
        return f'<Point "({self.latitude}, {self.longitude}), type {self.type}">'
