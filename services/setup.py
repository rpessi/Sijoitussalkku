from flaskapp.db import db
from sqlalchemy import text
from services import queries as que

'''A module for setting up names for owners and accounts'''

def add_owner(name):
    db_owners = que.owners_from_db()
    if name not in db_owners:
        sql = text("INSERT INTO owners (name) VALUES (:name)")
        db.session.execute(sql, {"name":name})
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
    owners = que.owners_from_db()
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










