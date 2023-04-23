from database import db
from Models.user_endorses_log import user_endorses_log

class Log(db.Model):

    id= db.Column('id', db.Integer, primary_key = True, autoincrement = "auto")
    hours = db.Column(db.Numeric)
    avg_sea = db.Column(db.Numeric)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    log_endorsers = db.relationship('Log', secondary=user_endorses_log, backref="log")
    
    def __repr__(self):
        return f'<Log "{self.id}, User {self.user_id}">'
