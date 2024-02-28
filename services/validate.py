'''A module for validating user inputs and actions'''

from datetime import date
from werkzeug.security import check_password_hash
from flask import request
from services import queries as que

def validate_login(username:str, password:str) -> bool:
    if que.check_user_exists(username):
        hash_value = que.get_password(username)
        return check_password_hash(hash_value, password)
    return False

def validate_sell(account_id:str, date_str:str, stock:str, number:str,
                  price:str) -> tuple[bool, str]:
    available = que.stocks_available_for_sell(account_id, stock)
    if not number.isdecimal():
        return (False, "Osakkeiden määrä ei ole kokonaisluku.")
    if available < int(number):
        return (False, "Osakkeiden määrä on liian suuri.")
    if not date_input(date_str):
        return (False, "Päivämäärä on virheellinen.")
    if not stock_price_input(price):
        return (False, "Osakkeen hinta on virheellinen")
    return (True, "")

def validate_buy(date_str:str, number:str, price:str) -> tuple[bool, str]:
    if not number.isdecimal():
        return (False, "Osakkeiden määrä ei ole kokonaisluku.")
    if not date_input(date_str):
        return (False, "Päivämäärä on virheellinen.")
    if not stock_price_input(price):
        return (False, "Osakkeen hinta on virheellinen")
    return (True, "")

def date_input(date_str:str) -> bool:
    parts = date_str.split(".")
    today = date.today()
    if len(parts) != 3:
        return False
    for number in parts:
        if not number.isdecimal():
            return False
    day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
    if day < 1 or day > 31:
        return False
    if month < 1 or month > 12:
        return False
    if year < 1900 or year > today.year:
        return False
    return True

def stock_price_input(price:str) -> bool:
    numbers = price.split(".")
    for number in numbers:
        if not number.isdecimal():
            return False
    return True

def check_selection(selection:list[str]) -> bool:
    '''Checks for empty values or missing selections'''
    for value in selection:
        if not request.form.get(value):
            return False
    return True

def validate_username(username:str) -> bool:
    if len(username) > 20:
        return False
    return True

def validate_stock(stock:str) -> bool:
    if len(stock) > 30:
        return False
    return True

def validate_account_name(name:str) -> bool:
    if len(name) > 30:
        return False
    return True

def validate_owner(owner:str) -> bool:
    if len(owner) > 30:
        return False
    return True
