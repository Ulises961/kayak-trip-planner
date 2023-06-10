from Api.database import db


class SeaState (db.Model):
    __table_args__ = (
        db.ForeignKeyConstraint(['day_id'], [
                                'sea.day_id'], name="sea_day_foreign_key_in_sea_state"),
    )
    day_id = db.Column(db.Integer,  primary_key=True)
    time = db.Column(db.Time, primary_key=True)
    wave_height = db.Column(db.Numeric)
    wave_direction = db.Column(db.Numeric)
    swell_direction = db.Column(db.Numeric)
    swell_period = db.Column(db.Numeric)
