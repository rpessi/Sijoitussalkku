from flaskapp.db import db
from sqlalchemy import text

def get_account_id(account_name, owner_name): #under construction?
    sql = text("SELECT A.id FROM accounts A, owners O\
               WHERE A.owner_id = O.id AND O.name =:owner_name\
               AND A.name=:account_name")
    id = db.session.execute(sql, {"owner_name":owner_name,
                            "account_name":account_name}).fetchone()
    db.session.commit()
    return id[0]

def get_full_buy_events(): 
    sqlb = text("SELECT O.name, A.name, B.date, B.stock, B.number, B.price\
                FROM owners O, accounts A, buy_events B\
                WHERE O.id = A.owner_id AND B.account_id = A.id")
    buy_events = db.session.execute(sqlb).fetchall()
    db.session.commit()
    if buy_events == None:
        return []
    else:
        return buy_events

def get_buy_events(owner_name, account_name, stock):
    '''For showing the events for the user'''
    sql = text("SELECT B.id, B.date, B.stock, B.number, B.sold\
                FROM owners O, accounts A, buy_events B\
                WHERE O.id = A.owner_id AND B.account_id = A.id\
                AND B.sold < B.number AND A.name = :account_name AND\
                O.name = :owner_name AND B.stock = :stock\
                ORDER BY B.date ASC")
    buy_events = db.session.execute(sql, {"account_name":account_name, 
                    "stock":stock, "owner_name":owner_name}).fetchall()
    db.session.commit()
    return buy_events

def check_user_exists(username):
    sql = text("SELECT username FROM users WHERE username=:username")
    user = db.session.execute(sql, {"username":username}).fetchone()
    if user == None:
        return False
    else:
        return user[0] == username

def get_owner_id(name):
    sql = text("SELECT id FROM owners  WHERE name=:name")
    owner_id = db.session.execute(sql, {"name":name}).fetchone()
    return owner_id[0]

def get_user_id(username):
    sql = text("SELECT id FROM users  WHERE username=:username")
    user_id = db.session.execute(sql, {"username":username}).fetchone()
    return user_id[0]

def accounts_by_owner(owner_id):
    sql = text("SELECT name FROM accounts WHERE owner_id=:owner_id")
    accountdata = db.session.execute(sql, {"owner_id":owner_id}).fetchall()
    accountnames = []
    for account in accountdata:
        accountnames.append(account[0])
    return accountnames

def owners_from_db(username):
    user_id = get_user_id(username)
    sql = text("SELECT name FROM owners O, users U\
               WHERE O.user_id = U.id AND U.id=:user_id")
    ownertuples = db.session.execute(sql, {"user_id":user_id}).fetchall()
    db.session.commit()
    owners = []
    for owner in ownertuples:
        owners.append(owner[0])
    return owners

def accounts_from_db(username):
    user_id = get_user_id(username)
    sql = text("SELECT DISTINCT A.name FROM accounts A, owners O, users U\
               WHERE A.owner_id = O.id AND U.id = O.user_id\
               AND U.id=:user_id")
    accounttuples = db.session.execute(sql, {"user_id":user_id}).fetchall()
    db.session.commit()
    accounts = []
    for account in accounttuples:
        accounts.append(account[0])
    return accounts

def stocks_from_db(): #todo, haku username:lla, vaatii scheman muutoksen
    sql = text("SELECT name FROM stocks")
    stocktuples = db.session.execute(sql).fetchall()
    db.session.commit()
    stocks = []
    for stock in stocktuples:
        stocks.append(stock[0])
    return stocks

def owner_exists():
    if len(owners_from_db()) == 0:
        return False
    return True

def owner_stock_account_exists():
    owners = owners_from_db()
    stocks = stocks_from_db()
    accounts = accounts_from_db()
    if len(owners) == 0 or len(stocks) == 0 or len(accounts) == 0:
        return False
    return True

def stocks_available_for_sell(account_id, stock):
    sql = text("SELECT SUM(number) - SUM(sold) as available\
               FROM buy_events\
               WHERE account_id =:account_id AND stock =:stock")
    result = db.session.execute(sql, {"account_id":account_id, 
                                      "stock":stock}).fetchone()
    if result.available == None:
        return 0
    return int(result[0])

def buys_for_pairing(account_id, stock):
    sql = text("SELECT B.id, B.date, B.stock, B.number, B.sold\
               FROM accounts A, buy_events B\
               WHERE B.account_id = A.id AND B.sold < B.number\
               AND A.id =:account_id AND B.stock =:stock\
               ORDER BY B.date ASC")
    buy_events = db.session.execute(sql, {"account_id":account_id,
                                          "stock":stock}).fetchall()
    db.session.commit()
    return buy_events

def get_sell_event_id(account_id, date, stock, number, price):
    sql = text("SELECT id FROM sell_events WHERE account_id =:account_id\
           AND date =:date AND stock =:stock AND number =:number\
           AND price =:price")
    result = db.session.execute(sql, {"account_id":account_id, "date":date,
                        "stock":stock, "number":number, "price":price}).fetchone()
    db.session.commit()
    return result[0]

def get_password(username):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    return user.password

def get_owner_account_pairs(username):
    user_id = get_user_id(username)
    sql = text("SELECT O.name, A.name FROM accounts A, owners O, users U\
            WHERE A.owner_id = O.id AND U.id = O.user_id and U.id =:user_id")
    pairs = db.session.execute(sql, {"user_id":user_id}).fetchall()
    return pairs

def get_years_with_sell_events():
    #todo: fix so that depends on username
    sql = text("SELECT DISTINCT EXTRACT(year FROM date) FROM sell_events;")
    results = db.session.execute(sql).fetchall()
    years = []
    for result in results:
        years.append(result[0])
    return years

def sell_events_by_year(selected_year, username):
    user_id = get_user_id(username)
    sql = text("SELECT O.name as owner, A.name as account, B.date as buydate, B.stock,\
                P.number, B.price as buyprice, S.date as selldate, S.price as sellprice\
                FROM owners O, accounts A, buy_events B, sell_events S, users U, pairing P\
                WHERE O.user_id = U.id AND A.owner_id = O.id AND S.account_id = A.id\
                AND P.sell_id = S.id AND P.buy_id = B.id\
                AND EXTRACT(year FROM S.date) =:selected_year AND U.id =:user_id\
                ORDER BY owner, account, B.stock, selldate ASC")
    results = db.session.execute(sql, {"selected_year":selected_year, "user_id":user_id}).fetchall()
    print("ekarivi", results[0])
    return results
