from sqlalchemy import text
from flaskapp.db import db
from services import queries as que

def add_event(event_type, owner_name, account_name,
              date, stock, number, price):
    account_id = que.get_account_id(account_name, owner_name)
    if event_type == "sell":
        #todo, validate first
        sql = text("INSERT INTO sell_events (account_id, date, stock,\
                   number, price) VALUES (:account_id, :date, :stock, \
                   :number, :price)")
        db.session.execute(sql, {"account_id":account_id, "date":date,\
                                "stock":stock, "number":number, "price":price})
        db.session.commit()
        sell_id = que.get_sell_event_id(account_id, date, stock, number, price)
        pairing(account_id, stock, sell_id, number)
    else:
        sql = text("INSERT INTO buy_events (account_id, date, stock,\
                   number, price, sold) VALUES (:account_id, :date, :stock, \
                   :number, :price, :sold)")

        db.session.execute(sql, {"account_id":account_id, "date":date, "stock":stock,\
                            "number":number, "price":price, "sold":0})
        db.session.commit()

def pairing(account_id, stock, sell_id, number):
    '''a function for pairing sell- and buy-events'''
    buy_events = que.buys_for_pairing(account_id, stock)
    sell_number = int(number)
    for event in buy_events:
        buy_id, buy_number, sold = event[0], event[3], event[4]
        available = buy_number - sold
        pair_number = min(sell_number, available)
        if pair_number > 0:
            sold_new = pair_number + sold
            update_buy_event(buy_id, sold_new)
            update_pairing_table(buy_id, sell_id, pair_number)
        sell_number -= pair_number
        if sell_number == 0:
            break

def update_buy_event(buy_id, sold_new):
    sql = text("UPDATE buy_events SET sold =:sold_new\
               WHERE id =:buy_id")
    db.session.execute(sql, {"sold_new":sold_new, "buy_id":buy_id})
    db.session.commit()

def update_pairing_table(buy_id, sell_id, number):
    number = number
    sql = text("INSERT INTO pairing (buy_id, sell_id, number)\
           VALUES (:buy_id, :sell_id, :number)")
    db.session.execute(sql, {"buy_id":buy_id, "sell_id":sell_id, "number":number})
    db.session.commit()
