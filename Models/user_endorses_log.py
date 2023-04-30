from Api.database import db

user_endorses_log = db.Table('user_endorses_log',
    db.Column('log_id',db.Integer, db.ForeignKey('log.id'), primary_key=True),
    db.Column('endorsers',db.Integer, db.ForeignKey('users.id')))
