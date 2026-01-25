# database.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

metadata = MetaData(schema='kplanner')
db = SQLAlchemy(metadata=metadata)
