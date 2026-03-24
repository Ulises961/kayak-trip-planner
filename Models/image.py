
from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from Models.base_model import BaseModel



class Image (BaseModel):
    size: Mapped[Optional[Numeric]] = mapped_column(Numeric, nullable=True)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    def __repr__(self):
        return f'<Image "name {self.name}, path {self.location}, size {self.size}">'
