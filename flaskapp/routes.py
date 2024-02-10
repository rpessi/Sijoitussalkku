# A module handling the web requests, posts and navigation
from flaskapp.app import app
from flaskapp.db import db
from flask import redirect, render_template, request
from services import events, setup as set, queries as que

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/setup", methods=["GET"])
def setup(): 
    return render_template("/setup.html")

@app.route("/addowner", methods=["GET", "POST"])
def addowner():
    owners = que.owners_from_db()
    if request.method == "POST":
        owner = request.form["owner"]
        result = set.add_owner(owner)
        #owners = set.owners_from_db()
        if result == True:
            return redirect("/addowner")
        else:
            #todo, joku error-sivu?
            return redirect("/")
    else:
        #owners = set.owners_from_db()
        return render_template("addowner.html", owners=owners)

@app.route("/addstock", methods=["GET", "POST"])
def addstock():
    stocks = que.stocks_from_db()
    if request.method == "POST":
        stock = request.form["stock"]
        result = set.add_stock(stock)
        stocks = que.stocks_from_db()
        if result == True: #success
            #todo
            return redirect("/addstock")
        else:
            #todo, error message
            return redirect("/")
    else:
        return render_template("addstock.html", stocks=stocks)

@app.route("/addaccount", methods=["GET", "POST"])
def addaccount():
    owners = que.owners_from_db()
    if request.method == "POST":
        owner = request.form["owner"]
        account = request.form["account"]
        result = set.add_account(account, owner)
        if result == True:
            return redirect("/addaccount")
        else:
            #todo, error
            return redirect("/")
    else:
        return render_template("addaccount.html", owners=owners)


@app.route("/addevent", methods=["GET", "POST"])
def addevent():
    owners = que.owners_from_db()
    stocks = que.stocks_from_db()
    accounts = que.accounts_from_db()
    return render_template("addevent.html", stocks=stocks,
                           owners=owners, accounts=accounts)

@app.route("/event", methods=["POST"])
def event():
    event_type = request.form["event_type"]
    owner = request.form["owner"]
    account = request.form["account"]
    date = request.form["date"]
    stock = request.form["stock"]
    number = request.form["number"]
    price = request.form["price"]
    if event_type == "buy":
        type = "osto"
    else:
        type = "myynti"
    events.add_event(event_type, owner, account, date, stock,
                     number, price)
    return render_template("event.html", event_type=type,
        owner=owner, account=account, date=date, stock=stock,
        number=number, price=price)

@app.route("/holdings", methods=["GET", "POST"])
def holdings():
    if request.method == "GET":
        return render_template("holdings.html")
