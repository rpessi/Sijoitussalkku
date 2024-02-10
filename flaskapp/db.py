from os import getenv
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flaskapp.app import app

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)