import uuid

import uuid_extension
from Api.database import db
from Models.base_model import BaseModel
from Models.user_endorses_log import user_endorses_log
from sqlalchemy import UUID, Integer, Numeric, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional, TYPE_CHECKING
from uuid import UUID as _UUID

if TYPE_CHECKING:
    from Models.user import User

class Log(BaseModel):
    hours: Mapped[Optional[Numeric]] = mapped_column(Numeric, nullable=True)
    avg_sea: Mapped[Optional[Numeric]] = mapped_column(Numeric, nullable=True)
    user_id: Mapped[Optional[_UUID]] = mapped_column(UUID, ForeignKey('users.id'), nullable=True)
    
    user_logs: Mapped[List["User"]] = relationship(back_populates='logs')
    user_endorsed_logs: Mapped[List["User"]] = relationship(secondary=user_endorses_log, back_populates='endorsed_logs')

    def __repr__(self):
        return f'<Log "{self.id}, User {self.user_id}">'
