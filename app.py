from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask import Flask
from Models.user import  User

app = Flask(__name__)

app.config.from_pyfile('config.py')


if __name__ == "__main__":
    app.run()
