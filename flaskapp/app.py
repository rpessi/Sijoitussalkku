"""A module for initializing the app object"""

from os import getenv
from flask import Flask

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import flaskapp.routes

if __name__ == "__main__":
    app.run(host='0.0.0.0')

