class Portfolio:
    '''A class for creating portfolio objects'''
    #attributes: name, owner, accounts
    #methods: init, add_account, holdings
    pass

class Account:
    '''A class for creating account objects for a portfolio'''
    #attributes: events
    #methods: add_stock, sell_stock
    pass

class Event:
    '''A class for creating event objects for an account'''
    #attributes: day, stock, number, price
    #methods: pairing
    pass

class Stock:
    '''A class for creating stock objects for an event'''
    #attributes: name, quote, dividend, stocks
    #methods: update_quote, update_dividend
