from Api.database import db
from sqlalchemy import DateTime, Integer, String, Time, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from Models.sea_state import SeaState
    from Models.day import Day

class Sea (db.Model):
    __table_args__ = (
        ForeignKeyConstraint(['day_id'],['day.id'], name="day_foreign_key_in_sea"),
    )
    day_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    moon_phase: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    high_tide: Mapped[Optional[Time]] = mapped_column(Time, nullable=True)
    low_tide: Mapped[Optional[Time]] = mapped_column(Time, nullable=True)
    
    sea_states: Mapped[List["SeaState"]] = relationship(foreign_keys="SeaState.day_id", cascade='all, delete,save-update')
    recorded_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, server_default=db.func.now())