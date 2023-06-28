from Api.database import db
from Models.inventory_items import inventory_items
from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from Models.item import Item

class Inventory(db.Model):
    def __init__(self,items=[],**kwargs):
        self.items = items
        self.__dict__.update(kwargs)

    id= db.Column('id', db.Integer, primary_key = True, autoincrement = "auto")
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'))
    items : Mapped[Optional[List[Item]]]= db.relationship( secondary = inventory_items, backref='inventories', cascade='all,delete')
    
    def __repr__(self):
        return f'<Inventory "{self.id}">'
