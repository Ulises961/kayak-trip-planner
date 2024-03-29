
from Api.database import db

class WeatherState (db.Model):
    __table_args__ = (
        db.ForeignKeyConstraint(['day_id'], [
                                'weather.day_id'], name="weather_day_foreign_keys_in_weather_state"),
    )
    day_id = db.Column(db.Integer,  primary_key=True)
    time = db.Column(db.Time, primary_key=True)
    temperature = db.Column(db.Numeric)
    precipitation = db.Column(db.Numeric)
    wind_direction = db.Column(db.Numeric)
    wind_force = db.Column(db.Numeric)
    cloud = db.Column(db.String(255))

    def __repr__(self):
        return f'<Weather state " time {self.time}, temperature {self.temperature}, wind direction {self.wind_direction}, wind force {self.wind_force}">'
