'''A module for validating user inputs and actions'''
from werkzeug.security import check_password_hash
from datetime import date
from services import queries as que

def validate_login(username, password):
    if que.check_user_exists(username):
        hash_value = que.get_password(username)
        return check_password_hash(hash_value, password)
    else:
        return False

def validate_sell(account_id, date, stock, number, price):
    available = que.stocks_available_for_sell(account_id, stock)
    if not number.isdecimal():
        return (False, "Osakkeiden määrä ei ole kokonaisluku.")
    if available < int(number):
        return (False, "Osakkeiden määrä on liian suuri.")
    if not date_input(date):
        return (False, "Päivämäärä on virheellinen.")
    if not stock_price_input(price):
        return (False, "Osakkeen hinta on virheellinen")
    return (True, "")

def validate_buy(date, number, price):
    if not number.isdecimal():
        return (False, "Osakkeiden määrä ei ole kokonaisluku.")
    if not date_input(date):
        return (False, "Päivämäärä on virheellinen.")
    if not stock_price_input(price):
        return (False, "Osakkeen hinta on virheellinen")
    return (True, "")

def date_input(date_input):
    list = date_input.split(".")
    today = date.today()
    if len(list) != 3:
        return False
    for number in list:
        if not number.isdecimal():
            return False
    day, month, year= int(list[0]), int(list[1]), int(list[2]) 
    if day < 1 or day > 31:
        return False
    if month < 1 or month > 12:
        return False
    if year < 1900 or year > today.year:
        return False
    return True

def stock_price_input(price):
    numbers = price.split(".")
    if len(numbers) > 2:
        return False
    for number in numbers:
        if not number.isdecimal():
            return False
    return True

def owner_name_input(owner:str):
    #todo: length, main function checks for availability
    pass

def account_name_input(account:str):
    #todo: length
    pass

def stock_name_input(stock:str):
    #todo: length, main function checks for availability
    pass

def owner_has_account(account, owner):
    #todo: check if owner has the given account
    pass

