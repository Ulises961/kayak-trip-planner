
from sqlalchemy import UUID, ForeignKey, String, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from Models.base_model import BaseModel
import enum
from uuid import UUID as _UUID


class ItemCategoryType(enum.Enum):
    FIRST_AID = "first_aid"
    CAMPING = "camping"
    REPAIR = "repair"
    TRAVEL = "travel"
    GENERIC = "generic"
    FOOD = "food"

class Item(BaseModel):

    category: Mapped[Optional[ItemCategoryType]] = mapped_column(
        Enum(ItemCategoryType), nullable=True
    )
    checked: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    user_id: Mapped[_UUID] = mapped_column(UUID, ForeignKey('users.id'),nullable=False)
