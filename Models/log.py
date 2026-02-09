import uuid
from Api.database import db
from Models.user_endorses_log import user_endorses_log
from sqlalchemy import Integer, Numeric, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from Models.user import User

class Log(db.Model):

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hours: Mapped[Optional[Numeric]] = mapped_column(Numeric, nullable=True)
    avg_sea: Mapped[Optional[Numeric]] = mapped_column(Numeric, nullable=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('users.id'), nullable=True)
    
    user_logs: Mapped[List["User"]] = relationship(back_populates='logs')
    user_endorsed_logs: Mapped[List["User"]] = relationship(secondary=user_endorses_log, back_populates='endorsed_logs')
    public_id: Mapped[str] = mapped_column(String(255), nullable=False, default=lambda: str(uuid.uuid4()))
    
    def __repr__(self):
        return f'<Log "{self.id}, User {self.user_id}">'
