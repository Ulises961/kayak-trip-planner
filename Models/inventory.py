from Api.database import db
from Models.inventory_items import inventory_items
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from Models.item import Item
    from Models.trip import Trip

class Inventory(db.Model):
    def __init__(self,items=[],**kwargs):
        self.items = items
        self.__dict__.update(kwargs)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    trip_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('trip.id'), nullable=True)
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable= False)
    items: Mapped[List["Item"]] = relationship(secondary=inventory_items, cascade='all,delete')

    def __repr__(self):
        return f'<Inventory "{self.id}">'
