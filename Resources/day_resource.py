import logging
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from Schemas.day_schema import DaySchema
from Models.day import Day

logger = logging.getLogger(__name__) # It will print the name of this module when the main app is running

DAY_ENDPOINT = "/api/day/<id>"

class DayResource(Resource):

    def retrieveDayById(id):
        day = Day.query.filter_by('id', id).first()
        day_json = DaySchema.dump(day)
        if not day_json:
             raise NoResultFound()
        return day_json
    
    def get(self, id=None):
        """
        DayResource GET method. Retrieves the information related to the day with the passed id in the request
        """
        try:
            self.retrieveDayById(id)
        except NoResultFound:
                abort(404, message=f"Day with id {id} not found in database")
        
