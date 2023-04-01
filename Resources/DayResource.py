import logging
from flask import request
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound


logger = logging.getLogger(__name__) # It will print the name of this module when the main app is running
