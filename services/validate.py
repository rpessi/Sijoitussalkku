'''A module for validating user inputs and actions'''
from werkzeug.security import check_password_hash
from services import queries as que

def validate_login(username, password):
    hash_value = que.get_password(username)
    return check_password_hash(hash_value, password)


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

def stock_price(price):
    #todo: check for format, fix if necessary
    #return (TRUE/FALSE, price)
    pass

def number(number):
    #todo: check number format (Integer)
    pass