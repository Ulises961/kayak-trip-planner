from Api.database import db
import enum
from Models.point_has_image import PointHasImage
from typing import Optional,List

class PointType(enum.Enum):
    STOP = 'stop'
    POSITION = 'position'
    INTEREST = 'interest'

class Point (db.Model):
    __table_args__ = (
        db.ForeignKeyConstraint(['day_id'],['day.id'], name="day_foreign_key_in_point"),
    )
    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    gps = db.Column(db.Numeric)
    notes = db.Column(db.Text)
    type = db.Column(db.Enum(PointType))
    day_id = db.Column(db.Integer)
    previous_id= db.Column(db.Integer, db.ForeignKey('point.id')) 
    next_id= db.Column(db.Integer, db.ForeignKey('point.id')) 
    reference_id = db.Column(db.Integer, db.ForeignKey('point.id')) 
    previous : db.Mapped[Optional['Point']]  = db.relationship('Point', foreign_keys=[previous_id], uselist =False, back_populates='next', remote_side=[id])
    next : db.Mapped[Optional['Point']] = db.relationship('Point', foreign_keys=[next_id], uselist=False, back_populates='previous')
    reference : db.Mapped[Optional['Point']]  = db.relationship('Point',  foreign_keys=[reference_id], back_populates='nearby', remote_side=[id])
    nearby : db.Mapped[List[Optional['Point']]] = db.relationship('Point',  foreign_keys=[reference_id])
    images = db.relationship('Image', secondary=PointHasImage,
                             lazy="subquery", backref=db.backref('point', lazy=True), cascade='all, delete')

    def __repr__(self):
        return f'<Point "{self.gps}, type {self.type}">'
