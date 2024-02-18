from flask import session
from sqlalchemy import text
from werkzeug.security import generate_password_hash
from flaskapp.db import db
from services import queries as que

'''A module for adding user and basic settings'''

def add_user(username, password):
    pwd_hashed = generate_password_hash(password)
    sql = text("""INSERT INTO users (username, password)
               VALUES (:username, :password)""")
    db.session.execute(sql, {"username":username, "password":pwd_hashed})
    db.session.commit()

def add_owner(name):
    username = session["username"]
    db_owners = que.owners_from_db(username)
    if name not in db_owners:
        user_id = que.get_user_id(username)
        sql = text("INSERT INTO owners (name, user_id) VALUES (:name, :user_id)")
        db.session.execute(sql, {"name":name, "user_id":user_id})
        db.session.commit()
        return True
    else:
        return False

def add_stock(name, dividend=0):
    db_stocks = que.stocks_from_db()
    if name not in db_stocks:
        sql = text("INSERT INTO stocks (name, dividend) VALUES (:name, :dividend)")
        db.session.execute(sql, {"name":name, "dividend":dividend})
        db.session.commit()
        return True
    else:
        return False

def add_account(name, owner):
    owners = que.owners_from_db(session["username"])
    owner_id = que.get_owner_id(owner)
    accounts = que.accounts_by_owner(owner_id)
    if name not in accounts:
        sql = text("INSERT INTO accounts (name, owner_id) VALUES (:name, :owner_id)")
        db.session.execute(sql, {"name":name, "owner_id":owner_id})
        db.session.commit()
        #todo, success
        return True
    else:
        #todo, error
        return False
