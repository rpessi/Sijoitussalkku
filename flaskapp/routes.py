'''A module handling the web requests, posts and navigation'''
import secrets
from flaskapp.app import app
from flask import redirect, render_template, request
from flask import session, abort, flash
from services import events, setup as set, queries as que
from services import validate as val

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    selection = ["username", "password"]
    if not val.check_selection(selection):
        flash("Täytä molemmat kentät.")
        return redirect("/")
    username = request.form["username"]
    password = request.form["password"]
    if val.validate_login(username, password):
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")
    else:
        flash("Käyttäjätunnus ja salasana eivät täsmää.")
        return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        selection = ["username", "password", "pwd_check"]
        if not val.check_selection(selection):
            flash("Täytä kaikki kentät.")
            return redirect("/register")
        username = request.form["username"]
        password = request.form["password"]
        pwd_check = request.form["pwd_check"]
        if que.check_user_exists(username):
            flash("Käyttäjätunnus on varattu, valitse uusi.")
            return redirect("/register")
        elif password != pwd_check:
            flash("Virhe salasanan uudelleenkirjoituksessa.")
            return redirect("/register")
        else: 
            set.add_user(username, password)
            flash("Käyttäjätunnus on luotu, voit nyt kirjautua sisään.")
            return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    del session["csrf_token"]
    flash("Olet kirjautunut ulos.")
    return redirect("/")

@app.route("/addowner", methods=["GET", "POST"])
def addowner():
    owners = que.owners_from_db(session["username"])
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            flash("Tokenisssa ongelmaa")
            abort(403)
        if not request.form.get("owner"):
            flash("Täytä kenttä.")
            return redirect("/addowner")
        owner = request.form["owner"]
        result = set.add_owner(owner)
        if result == True:
            return redirect("/addowner")
        else:
            flash("Omistaja on jo lisätty.")
            return redirect("/addowner")
    else:
        return render_template("addowner.html", owners=owners)

@app.route("/addstock", methods=["GET", "POST"])
def addstock():
    stocks = que.stocks_from_db()
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if not request.form.get("stock"):
            flash("Täytä kenttä.")
            return redirect("/addstock")
        stock = request.form["stock"]
        result = set.add_stock(stock)
        if result == True:
            return redirect("/addstock")
        else:
            flash("Osake on jo lisätty.")
            return redirect("/addstock")
    else:
        return render_template("addstock.html", stocks=stocks)

@app.route("/addaccount", methods=["GET", "POST"])
def addaccount():
    owners = que.owners_from_db(session["username"])
    pairs = que.get_owner_account_pairs(session["username"])
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        selection = ["owner", "account"]
        if not val.check_selection(selection):
            flash("Valitse omistaja ja täytä kenttä.")
            return redirect("/addaccount")
        owner = request.form["owner"]
        account = request.form["account"]
        result = set.add_account(account, owner)
        if result == True:
            flash("Tilin lisäys onnistui")
            return redirect("/addaccount")
        else:
            flash("Tilin lisäys ei onnistunut")
            return redirect("/addaccount")
    else:
        return render_template("addaccount.html", owners=owners,
                               pairs=pairs)

@app.route("/addevent", methods=["GET"])
def addevent():
    username = session["username"]
    pairs = que.get_owner_account_pairs(username)
    stocks = que.stocks_from_db()
    return render_template("addevent.html", stocks=stocks,
                           pairs=pairs)

@app.route("/event", methods=["POST"])
def event():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    selection = ["event_type", "pair", "date", "stock",
                 "number", "price"]
    if not val.check_selection(selection):
        flash("Suorita kaikki valinnat ja täytä kentät.")
        return redirect("/addevent")
    event_type = request.form["event_type"]
    pair = request.form["pair"]
    pair = pair.split("+")
    owner = pair[0]
    account = pair[1]
    date = request.form["date"]
    stock = request.form["stock"]
    number = request.form["number"]
    price = request.form["price"].replace(",", ".")
    if event_type == "buy":
        type = "osto"
    else:
        type = "myynti"
    result, msg = events.add_event(event_type, owner, account, date, stock,
                     number, price)
    if result:
        return render_template("event.html", event_type=type,
            owner=owner, account=account, date=date, stock=stock,
            number=number, price=price)
    else:
        flash(msg)
        return redirect("/addevent")

@app.route("/sell_events", methods=["GET", "POST"])
def sell_events():
    username = session["username"]
    years = que.get_years_with_sell_events(username)
    if request.method =="GET":
        if years == []:
            flash("Myyntitapahtumia ei ole.")
            return redirect("/")
        return render_template("sell_events.html", years=years)
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if not request.form.get("year"):
            flash("Valitse vuosi.")
            return redirect("/sell_events")
        selected_year = request.form["year"]
        sell_events = que.sell_events_by_year(selected_year, username)
        return render_template("sell_events.html", years=years,
            selected_year=selected_year, events=sell_events)

@app.route("/holdings", methods=["GET"])
def holdings():
    username = session["username"]
    if request.method == "GET":
        report = que.holdings_report(username)
        if report == []:
            flash("Lisäämilläsi omistajilla ei ole omistuksia.")
            return redirect("/")
        return render_template("holdings.html", report=report)
