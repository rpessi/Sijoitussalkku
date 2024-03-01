'''A module for setting up the database'''
from os import getenv
from flask_sqlalchemy import SQLAlchemy
from flaskapp.app import app

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
