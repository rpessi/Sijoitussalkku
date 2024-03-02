'''A module for database queries'''

from sqlalchemy import text
from flaskapp.db import db

def get_account_id(account_name:str, owner_name:str, username:str) -> str:
    user_id = get_user_id(username)
    sql = text(
            """SELECT A.id FROM accounts A, owners O, users U
               WHERE A.owner_id = O.id AND O.user_id = U.id
               AND O.name =:owner_name AND U.id =:user_id
               AND A.name=:account_name"""
               )
    acc_id = db.session.execute(sql, {"owner_name":owner_name, "user_id":user_id,
                            "account_name":account_name}).fetchone()
    return acc_id[0]

def check_user_exists(username:str) -> bool:
    sql = text("SELECT username FROM users WHERE username=:username")
    user = db.session.execute(sql, {"username":username}).fetchone()
    if not user:
        return False
    return True

def get_owner_id(name:str, username:str) -> str:
    user_id = get_user_id(username)
    sql = text(
            """SELECT O.id FROM owners O, users U
               WHERE O.user_id = U.id AND O.name=:name
               AND U.id=:user_id"""
               )
    owner_id = db.session.execute(sql, {"name":name, "user_id":user_id}).fetchone()
    return owner_id[0]

def get_user_id(username:str) -> str:
    sql = text("SELECT id FROM users  WHERE username=:username")
    user_id = db.session.execute(sql, {"username":username}).fetchone()
    return user_id[0]

def accounts_by_owner(owner_id:str) -> list:
    sql = text("SELECT name FROM accounts WHERE owner_id=:owner_id")
    accountdata = db.session.execute(sql, {"owner_id":owner_id}).fetchall()
    return [account[0] for account in accountdata]

def owners_from_db(username:str) -> list:
    user_id = get_user_id(username)
    sql = text(
            """SELECT name FROM owners O, users U
               WHERE O.user_id = U.id AND U.id=:user_id"""
               )
    result = db.session.execute(sql, {"user_id":user_id}).fetchall()
    db.session.commit()
    return [owner[0] for owner in result]

def stocks_from_db(username:str) -> list:
    user_id = get_user_id(username)
    sql = text(
            """SELECT name FROM stocks WHERE user_id=:user_id
               ORDER BY name ASC"""
               )
    result = db.session.execute(sql, {"user_id":user_id}).fetchall()
    db.session.commit()
    return [stock[0] for stock in result]

def dividends_from_db(username:str) -> list:
    user_id = get_user_id(username)
    sql = text(
            """SELECT name, dividend
               FROM stocks WHERE user_id =:user_id
               ORDER BY name ASC"""
               )
    result = db.session.execute(sql, {"user_id":user_id}).fetchall()
    return [(row.name, row.dividend) for row in result if row.dividend > 0]

def stocks_available_for_sell(account_id:str, stock:str) -> int:
    '''A helper function for validating sell-events'''
    sql = text(
            """SELECT SUM(number) - SUM(sold) as available
               FROM buy_events
               WHERE account_id =:account_id AND stock =:stock"""
               )
    result = db.session.execute(sql, {"account_id":account_id,
                                      "stock":stock}).fetchone()
    if not result:
        return 0
    return int(result[0])

def buys_for_pairing(account_id:str, stock:str) -> list:
    '''A helper function for pairing sell- and buy-events according to FIFO-principle'''
    sql = text(
            """SELECT B.id, B.date, B.stock, B.number, B.sold
               FROM accounts A, buy_events B
               WHERE B.account_id = A.id AND B.sold < B.number
               AND A.id =:account_id AND B.stock =:stock
               ORDER BY B.date ASC"""
               )
    buy_events = db.session.execute(sql, {"account_id":account_id,
                                          "stock":stock}).fetchall()
    return buy_events

def get_sell_event_id(account_id:str, date:str, stock:str, number:str, price:str) -> str:
    '''A helper function for add_sell_event'''
    sql = text(
            """SELECT id FROM sell_events WHERE account_id =:account_id
               AND date =:date AND stock =:stock AND number =:number
               AND price =:price"""
               )
    result = db.session.execute(sql, {"account_id":account_id, "date":date,
                        "stock":stock, "number":number, "price":price}).fetchone()
    return result[0]

def get_password(username:str) -> str:
    '''A helper function for validating login attempts'''
    user_id = get_user_id(username)
    sql = text("SELECT id, password FROM users WHERE users.id=:user_id")
    result = db.session.execute(sql, {"user_id":user_id}).fetchone()
    return result.password

def get_owner_account_pairs(username:str) -> list:
    '''A function for getting the owner-account pairs for rendering a form'''
    user_id = get_user_id(username)
    sql = text(
            """SELECT O.name AS owner, A.name AS account FROM owners O
               INNER JOIN accounts A ON O.id = A.owner_id
               WHERE O.user_id =:user_id
               ORDER BY owner, account ASC"""
               )
    pairs = db.session.execute(sql, {"user_id":user_id}).fetchall()
    return pairs

def get_years_with_sell_events(username:str) -> list:
    '''A function for getting the years with sell events for rendering a form'''
    user_id = get_user_id(username)
    sql = text(
            """SELECT DISTINCT EXTRACT(year FROM S.date) as year
               FROM sell_events S, accounts A, owners O, users U
               WHERE S.account_id = A.id AND A.owner_id = O.id
               AND O.user_id = U.id AND U.id =:user_id"""
               )
    results = db.session.execute(sql, {"user_id":user_id}).fetchall()
    return [int(result.year) for result in results]

def sell_events_by_year(selected_year:str, username:str) -> list:
    '''A function for reporting sell events for the selected year'''
    user_id = get_user_id(username)
    sql = text(
            """SELECT O.name AS owner, A.name AS account, B.date AS buydate, B.stock,
               P.number, P.number*B.price AS buytotal, S.date AS selldate,
               P.number*S.price AS selltotal
               FROM users U JOIN owners O ON U.id = O.user_id
               JOIN accounts A ON A.owner_id = O.id
               JOIN buy_events B ON B.account_id = A.id
               JOIN pairing P ON B.id = P.buy_id
               JOIN sell_events S ON P.sell_id = S.id
               WHERE EXTRACT(year FROM S.date) =:selected_year AND U.id =:user_id
               ORDER BY owner, account, B.stock, selldate ASC"""
                )
    results = db.session.execute(sql, {"selected_year":selected_year, "user_id":user_id}).fetchall()
    results_formatted = []
    for row in results:
        buydate = f"{row.buydate.day}.{row.buydate.month}.{row.buydate.year}"
        stock, number, buytotal = row.stock, row.number, round(float(row.buytotal), 2)
        selldate = f"{row.selldate.day}.{row.selldate.month}.{row.selldate.year}"
        selltotal = round(float(row.selltotal), 2)
        newrow = (row.owner, row.account, buydate, stock, number, buytotal, selldate, selltotal)
        results_formatted.append(newrow)
    return results_formatted

def holdings_report(username:str) -> list:
    '''A function for reporting the holdings of the owners'''
    user_id = get_user_id(username)
    sql = text(
            """SELECT O.name as owner, B.stock, SUM(B.number-B.sold) as number,
               (SUM((B.number-B.sold)*B.price)/SUM(B.number-B.sold)) AS avgprice
               FROM users U JOIN owners O on U.id = O.user_id
               JOIN accounts A ON A.owner_id = O.id
               JOIN buy_events B ON B.account_id = A.id
               WHERE U.id =:user_id
               GROUP BY owner, B.stock HAVING SUM(B.number-B.sold) > 0
               ORDER BY owner, B.stock ASC"""
               )
    results = db.session.execute(sql, {"user_id":user_id}).fetchall()
    results_formatted = []
    for row in results:
        owner, stock, number = row.owner, row.stock, row.number
        avgprice = round(float(row.avgprice), 2)
        newrow = (owner, stock, number, avgprice)
        results_formatted.append(newrow)
    return results_formatted

def dividend_report(username:str) -> list:
    '''A function for reporting the dividends of the owners'''
    user_id = get_user_id(username)
    sql = text(
            """SELECT O.name AS owner, B.stock, SUM(B.number-B.sold) AS number,
               SUM(B.number-B.sold)*S.dividend AS dividends
               FROM users U JOIN owners O ON U.id = O.user_id
               JOIN accounts A ON A.owner_id = O.id
               JOIN buy_events B ON B.account_id = A.id
               JOIN stocks S ON B.stock = S.name
               WHERE U.id =:user_id AND S.user_id = U.id
               GROUP BY owner, B.stock, S.dividend HAVING SUM(B.number-B.sold) > 0
               ORDER BY owner, B.stock ASC"""
               )
    results = db.session.execute(sql, {"user_id":user_id}).fetchall()
    results_formatted = []
    for row in results:
        owner, stock, number = row.owner, row.stock, row.number
        dividends = round(float(row.dividends), 2)
        newrow = (owner, stock, number, dividends)
        results_formatted.append(newrow)
    return results_formatted

def buy_event_report(username:str) -> list:
    '''A function for reporting stocks available for sell'''
    user_id = get_user_id(username)
    sql = text(
            """SELECT O.name AS owner, B.stock, A.name AS account, B.date as buydate,
               B.number-B.sold as number, B.price as buyprice
               FROM users U JOIN owners O ON U.id = O.user_id
               JOIN accounts A ON O.id = A.owner_ID
               JOIN buy_events B on B.account_id = A.id
               WHERE U.id =:user_id AND B.number-B.sold > 0
               ORDER BY owner, B.stock, account, buydate ASC"""
               )
    results = db.session.execute(sql, {"user_id":user_id}).fetchall()
    results_formatted = []
    for row in results:
        owner, stock, account = row.owner, row.stock, row.account
        buydate = f"{row.buydate.day}.{row.buydate.month}.{row.buydate.year}"
        buyprice = round(float(row.buyprice), 2)
        newrow = (owner, stock, account, buydate, row.number, buyprice)
        results_formatted.append(newrow)
    return results_formatted

def top_dividendyields(username:str) -> list:
    '''A function for finding best dividend yield for each owner'''
    user_id = get_user_id(username)
    sql = text(
            """SELECT DISTINCT ON (O.name) O.name AS owner, B.stock, B.date, B.price,
               MAX(100*S.dividend/B.price) AS top_yield
               FROM users U JOIN owners O ON U.id = O.user_id
               JOIN accounts A ON O.id = A.owner_id
               JOIN buy_events B ON B.account_id = A.id
               JOIN stocks S ON B.stock = S.name
               WHERE U.id =:user_id AND S.user_id = U.id
               GROUP BY owner, B.stock, B.date, B.price, B.number - B.sold
               HAVING B.number - B.sold > 0
               ORDER BY owner, top_yield DESC"""
               )
    results = db.session.execute(sql, {"user_id":user_id}).fetchall()
    results_formatted = []
    for row in results:
        owner, stock = row.owner, row.stock
        date = f"{row.date.day}.{row.date.month}.{row.date.year}"
        price = round(float(row.price), 2)
        top_yield = round(float(row.top_yield), 2)
        newrow = (owner, stock, date, price, top_yield)
        results_formatted.append(newrow)
    return results_formatted
