from app import db

user_endorses_log = db.Table('user_endorses_log',
    log_id   = db.Column(db.Integer, db.ForeignKey('log.id'), primary_key=True),
    endorsers = db.Column(db.Integer, db.ForeignKey('endorsers.id'), primary_key=True))
