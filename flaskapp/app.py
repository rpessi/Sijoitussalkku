# A module for running the flask-app
from os import getenv #to be used later
from flask import Flask

app = Flask(__name__)


import routes
