from Api.database import db
from sqlalchemy import Integer, Time, Numeric, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from Models.sea import Sea

class SeaState (db.Model):
    __table_args__ = (
        ForeignKeyConstraint(['day_id'], ['sea.day_id'], name="sea_day_foreign_key_in_sea_state"),
    )
    day_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    time: Mapped[Time] = mapped_column(Time, primary_key=True)
    wave_height: Mapped[Optional[Numeric]] = mapped_column(Numeric, nullable=True)
    wave_direction: Mapped[Optional[Numeric]] = mapped_column(Numeric, nullable=True)
    swell_direction: Mapped[Optional[Numeric]] = mapped_column(Numeric, nullable=True)
    swell_period: Mapped[Optional[Numeric]] = mapped_column(Numeric, nullable=True)
