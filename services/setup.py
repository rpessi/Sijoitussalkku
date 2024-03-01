'''A module for adding user and basic settings'''

from flask import session
from sqlalchemy import text
from werkzeug.security import generate_password_hash
from services import queries as que
from flaskapp.db import db

def add_user(username:str, password:str) -> None:
    pwd_hashed = generate_password_hash(password)
    sql = text(
            """INSERT INTO users (username, password)
               VALUES (:username, :password)"""
               )
    db.session.execute(sql, {"username":username, "password":pwd_hashed})
    db.session.commit()

def add_owner(name:str) -> bool:
    username = session["username"]
    db_owners = que.owners_from_db(username)
    if name not in db_owners:
        user_id = que.get_user_id(username)
        sql = text("INSERT INTO owners (name, user_id) VALUES (:name, :user_id)")
        db.session.execute(sql, {"name":name, "user_id":user_id})
        db.session.commit()
        return True
    return False

def add_stock(name:str, dividend=0) -> bool:
    username = session["username"]
    db_stocks = que.stocks_from_db(username)
    if name not in db_stocks:
        user_id = que.get_user_id(username)
        sql = text(
                """INSERT INTO stocks (name, dividend, user_id)
                   VALUES (:name, :dividend, :user_id)"""
                   )
        db.session.execute(sql, {"name":name, "dividend":dividend, "user_id":user_id})
        db.session.commit()
        return True
    return False

def add_account(name:str, owner:str) -> bool:
    owner_id = que.get_owner_id(owner)
    accounts = que.accounts_by_owner(owner_id)
    if name not in accounts:
        sql = text("INSERT INTO accounts (name, owner_id) VALUES (:name, :owner_id)")
        db.session.execute(sql, {"name":name, "owner_id":owner_id})
        db.session.commit()
        return True
    return False

def add_dividend(stock:str, dividend:str) -> None:
    user_id = que.get_user_id(session["username"])
    sql = text(
            """UPDATE stocks SET dividend=:dividend
            WHERE name=:stock AND user_id=:user_id"""
            )
    db.session.execute(sql, {"dividend":dividend, "stock":stock, "user_id":user_id})
    db.session.commit()
