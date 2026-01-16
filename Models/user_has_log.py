from Api.database import db
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class UserHasLog (db.Model):
    log_id: Mapped[int] = mapped_column(Integer, ForeignKey('log.id'), primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), primary_key=True)
