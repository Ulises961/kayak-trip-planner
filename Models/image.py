from Api.database import db
from sqlalchemy import Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from Models.point import Point
    from Models.user import User

class Image (db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    size: Mapped[Optional[Numeric]] = mapped_column(Numeric, nullable=True)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    public_id: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self):
        return f'<Image "name {self.name}, path {self.location}, size {self.size}">'
