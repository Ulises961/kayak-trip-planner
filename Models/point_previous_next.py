from app import db

point_previous_next = db.Table(
    'point_previous_next',
    db.Column('current_point_id', db.Integer, db.ForeignKey('point.id'), primary_key=True),
    db.Column('previous_point_id', db.Integer, db.ForeignKey('point.id')),
    db.Column('next_point_id', db.Integer, db.ForeignKey('point.id'))
)