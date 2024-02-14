'''A module for handling the login'''
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash
from flaskapp.db import db

def add_user(username, password):
    #todo, check if user already exists
    pwd_hashed = generate_password_hash(password)
    sql = text("INSERT INTO users (username, password)\
               VALUES (:username, :password)")
    db.session.execute(sql, {"username":username, "password":pwd_hashed})
    db.session.commit()
