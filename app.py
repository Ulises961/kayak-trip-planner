from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask import Flask

app = Flask(__name__)

app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
bcrypt = Bcrypt()