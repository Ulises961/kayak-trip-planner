from app import db

class UserEndorsesLog (db.Model):
    log_id   = db.Column(db.Integer, db.ForeignKey('log.id'), primary_key=True)
    endorser = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    endorsed = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
