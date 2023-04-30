from Api.database import db
import enum

class ItemCategoryType(enum.Enum):
    FIRST_AID = 'first_aid'
    CAMPING = 'camping'
    REPAIR = 'repair'
    TRAVEL = 'travel'
    GENERIC = 'generic'

class Item (db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    category = db.Column(db.Enum(ItemCategoryType)) 
    checked = db.Column(db.Boolean)
    name = db.Column(db.String(255))