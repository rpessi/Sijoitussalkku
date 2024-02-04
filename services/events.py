#importteja?
from flaskapp.app import db
from sqlalchemy import text

def get_account_id(owner_name, account_name): #under construction
    return 1

def add_event(event_type, owner_name, account_name,
              date, stock, number, price):
    account_id = get_account_id(account_name, owner_name)
    print(f"event: {event_type}, owner: {owner_name}, account: {account_name} ")
    print(f"date: {date}, stock: {stock}, number:{number}, price: {price} ")
    if event_type == "sell":
        sql = text("INSERT INTO sell_events (account_id, date, stock,\
                   number, price) VALUES (:account_id, :date, :stock, \
                   :number, :price)")
        db.session.execute(sql, {"account_id":account_id, "date":date, "stock":stock,\
                            "number":number, "price":price})
        #kutsu pairing-funktiota ja päivitä buy-taulun sold-sarake
        #pairing pitää tehdä ennen myynnin kirjausta
    else:
        sql = text("INSERT INTO buy_events (account_id, date, stock,\
                   number, price, sold) VALUES (:account_id, :date, :stock, \
                   :number, :price, :sold)")

        db.session.execute(sql, {"account_id":account_id, "date":date, "stock":stock,\
                            "number":number, "price":price, "sold":0})
    db.session.commit()
    get_events()

def get_events(): #for test printing, trying to understand the database data types
    sqlb = text("SELECT * FROM buy_events")
    buy_events = db.session.execute(sqlb).fetchall()
    db.session.commit()
    for event in buy_events:
        print(event[3], float(event[5]))

def pairing():
    '''a function for pairing sell- and buy-events'''
    pass

def get_buy_events(owner_name, account_name, stock):
    '''A helper-function for pairing'''
    pass