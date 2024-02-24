'''A module for database queries'''

from flaskapp.db import db
from sqlalchemy import text

def get_account_id(account_name, owner_name):
    sql = text("""SELECT A.id FROM accounts A, owners O
               WHERE A.owner_id = O.id AND O.name =:owner_name
               AND A.name=:account_name""")
    acc_id = db.session.execute(sql, {"owner_name":owner_name,
                            "account_name":account_name}).fetchone()
    db.session.commit()
    return acc_id[0]

def get_full_buy_events():
    sqlb = text("""SELECT O.name, A.name, B.date, B.stock, B.number, B.price
                FROM owners O, accounts A, buy_events B
                WHERE O.id = A.owner_id AND B.account_id = A.id""")
    buy_events = db.session.execute(sqlb).fetchall()
    db.session.commit()
    if not buy_events:
        return []
    return buy_events

def get_buy_events(owner_name, account_name, stock):
    '''For showing the events for the user'''
    sql = text("""SELECT B.id, B.date, B.stock, B.number, B.sold
                FROM owners O, accounts A, buy_events B
                WHERE O.id = A.owner_id AND B.account_id = A.id
                AND B.sold < B.number AND A.name = :account_name AND
                O.name = :owner_name AND B.stock = :stock
                ORDER BY B.date ASC""")
    buy_events = db.session.execute(sql, {"account_name":account_name,
                    "stock":stock, "owner_name":owner_name}).fetchall()
    db.session.commit()
    return buy_events

def check_user_exists(username):
    sql = text("SELECT username FROM users WHERE username=:username")
    user = db.session.execute(sql, {"username":username}).fetchone()
    if not user:
        return False
    return True

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
    sql = text("""SELECT name FROM owners O, users U
               WHERE O.user_id = U.id AND U.id=:user_id""")
    ownertuples = db.session.execute(sql, {"user_id":user_id}).fetchall()
    db.session.commit()
    owners = []
    for owner in ownertuples:
        owners.append(owner[0])
    return owners

def accounts_from_db(username):
    user_id = get_user_id(username)
    sql = text("""SELECT DISTINCT A.name FROM accounts A, owners O, users U
               WHERE A.owner_id = O.id AND U.id = O.user_id
               AND U.id=:user_id""")
    accounttuples = db.session.execute(sql, {"user_id":user_id}).fetchall()
    db.session.commit()
    accounts = []
    for account in accounttuples:
        accounts.append(account[0])
    return accounts

def stocks_from_db(username):
    user_id = get_user_id(username)
    sql = text("""SELECT name FROM stocks WHERE user_id=:user_id
               ORDER BY name ASC""")
    stocktuples = db.session.execute(sql, {"user_id":user_id}).fetchall()
    db.session.commit()
    stocks = []
    for stock in stocktuples:
        stocks.append(stock[0])
    return stocks

def dividends_from_db(username):
    user_id = get_user_id(username)
    sql = text("""SELECT name, dividend FROM stocks WHERE user_id =:user_id
               ORDER BY name ASC""")
    result = db.session.execute(sql, {"user_id":user_id}).fetchall()
    dividends = []
    for row in result:
        if row.dividend > 0:
            dividends.append((row.name, row.dividend))
    return dividends

def stocks_available_for_sell(account_id, stock):
    sql = text("""SELECT SUM(number) - SUM(sold) as available
               FROM buy_events
               WHERE account_id =:account_id AND stock =:stock""")
    result = db.session.execute(sql, {"account_id":account_id,
                                      "stock":stock}).fetchone()
    if not result:
        return 0
    return int(result[0])

def buys_for_pairing(account_id, stock):
    sql = text("""SELECT B.id, B.date, B.stock, B.number, B.sold
               FROM accounts A, buy_events B
               WHERE B.account_id = A.id AND B.sold < B.number
               AND A.id =:account_id AND B.stock =:stock
               ORDER BY B.date ASC""")
    buy_events = db.session.execute(sql, {"account_id":account_id,
                                          "stock":stock}).fetchall()
    db.session.commit()
    return buy_events

def get_sell_event_id(account_id, date, stock, number, price):
    sql = text("""SELECT id FROM sell_events WHERE account_id =:account_id
           AND date =:date AND stock =:stock AND number =:number
           AND price =:price""")
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
    sql = text("""SELECT O.name AS owner, A.name AS account FROM owners O
               INNER JOIN accounts A ON O.id = A.owner_id
               WHERE O.user_id =:user_id""")
    pairs = db.session.execute(sql, {"user_id":user_id}).fetchall()
    return pairs

def get_years_with_sell_events(username):
    user_id = get_user_id(username)
    sql = text("""SELECT DISTINCT EXTRACT(year FROM S.date) as year
               FROM sell_events S, accounts A, owners O, users U
               WHERE S.account_id = A.id AND A.owner_id = O.id
               AND O.user_id = U.id AND U.id =:user_id""")
    results = db.session.execute(sql, {"user_id":user_id}).fetchall()
    years = []
    if results:
        for result in results:
            years.append(result[0])
    return years

def sell_events_by_year(selected_year, username):
    user_id = get_user_id(username)
    sql = text("""SELECT O.name AS owner, A.name AS account, B.date AS buydate, B.stock,
                P.number, P.number*B.price AS buytotal, S.date AS selldate,
                P.number*S.price AS selltotal
                FROM users U JOIN owners O ON U.id = O.user_id
                JOIN accounts A ON A.owner_id = O.id
                JOIN buy_events B ON B.account_id = A.id
                JOIN pairing P ON B.id = P.buy_id
                JOIN sell_events S ON P.sell_id = S.id
                WHERE EXTRACT(year FROM S.date) =:selected_year AND U.id =:user_id
                ORDER BY owner, account, B.stock, selldate ASC""")
    results = db.session.execute(sql, {"selected_year":selected_year, "user_id":user_id}).fetchall()
    results_formatted = []
    for row in results:
        buydate = f"{row.buydate.day}.{row.buydate.month}.{row.buydate.year}"
        stock, number, buytotal = row.stock, row.number, round(float(row.buytotal),2)
        selldate = f"{row.selldate.day}.{row.selldate.month}.{row.selldate.year}"
        selltotal = round(float(row.selltotal), 2)
        string = f"{row.owner:20}{row.account:>20}: osto {buydate:15}{stock:20}{number:6}kpl\
                 yht. {buytotal:8}€, myynti {selldate:15}yht. {selltotal:8}€"
        results_formatted.append(string)
    return results_formatted

def holdings_report(username):
    sql = text("""SELECT O.name as owner, B.stock, SUM(B.number-B.sold) as number,
               (SUM((B.number-B.sold)*B.price)/SUM(B.number-B.sold)) AS avgprice
               FROM users U JOIN owners O on U.id = O.user_id
               JOIN accounts A ON A.owner_id = O.id
               JOIN buy_events B ON B.account_id = A.id
               WHERE U.username =:username
               GROUP BY owner, B.stock HAVING SUM(B.number-B.sold) > 0
               ORDER BY owner, B.stock ASC""")
    results = db.session.execute(sql, {"username":username}).fetchall()
    results_formatted = []
    for row in results:
        owner, stock, number = row.owner, row.stock, row.number
        avgprice = round(float(row.avgprice),2)
        string = f"{owner:20} - {stock:>20}: {number:8}kpl, keskihinta {avgprice:8}€"
        results_formatted.append(string)
    return results_formatted

def dividend_report(username):
    sql = text("""SELECT O.name AS owner, B.stock, SUM(B.number-B.sold) AS number,
               SUM(B.number-B.sold)*S.dividend AS dividends
               FROM users U JOIN owners O ON U.id = O.user_id
               JOIN accounts A ON A.owner_id = O.id
               JOIN buy_events B ON B.account_id = A.id
               JOIN stocks S ON B.stock = S.name
               WHERE U.username =:username AND S.user_id = U.id
               GROUP BY owner, B.stock, S.dividend HAVING SUM(B.number-B.sold) > 0
               ORDER BY owner, B.stock ASC""")
    results = db.session.execute(sql, {"username":username}).fetchall()
    results_formatted = []
    for row in results:
        owner, stock, number = row.owner, row.stock, row.number
        dividends = round(float(row.dividends),2)
        string = f"{owner:20} - {stock:>20}: {number:8}kpl, osingot {dividends:8}€"
        results_formatted.append(string)
    return results_formatted
