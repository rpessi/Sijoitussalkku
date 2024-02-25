'''A module for handling the web requests, posts and navigation'''
import secrets
from flask import redirect, render_template, request
from flask import session, abort, flash
from services import events, setup, queries as que
from services import validate as val
from flaskapp.app import app

@app.route("/")
def index():
    session["pre_token"] = secrets.token_hex(16)
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    if session["pre_token"] != request.form["pre_token"]:
        abort(403)
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
    flash("Käyttäjätunnus ja salasana eivät täsmää.")
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if session["pre_token"] != request.form["pre_token"]:
            abort(403)
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
        if password != pwd_check:
            flash("Virhe salasanan uudelleenkirjoituksessa.")
            return redirect("/register")
        if not val.validate_username(username):
            flash("Käyttäjätunnus on liian pitkä.")
            return redirect("/register")
        setup.add_user(username, password)
        flash("Käyttäjätunnus on luotu, voit nyt kirjautua sisään.")
        return redirect("/")
    return render_template("register.html")

@app.route("/logout")
def logout():
    del session["username"]
    del session["csrf_token"]
    del session["pre_token"]
    flash("Olet kirjautunut ulos.")
    return redirect("/")

@app.route("/addowner", methods=["GET", "POST"])
def addowner():
    owners = que.owners_from_db(session["username"])
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if not request.form.get("owner"):
            flash("Täytä kenttä.")
        owner = request.form["owner"]
        if not val.validate_owner(owner):
            flash("Omistajan nimi on liian pitkä.")
            return redirect("/addowner")
        result = setup.add_owner(owner)
        if result:
            return redirect("/addowner")
        flash("Omistaja on jo lisätty.")
        return redirect("/addowner")
    return render_template("addowner.html", owners=owners)

@app.route("/addstock", methods=["GET", "POST"])
def addstock():
    stocks = que.stocks_from_db(session["username"])
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if not request.form.get("stock"):
            flash("Täytä kenttä.")
            return redirect("/addstock")
        stock = request.form["stock"]
        if not val.validate_stock(stock):
            flash("Osakkeen nimi on liian pitkä.")
            return redirect("/addstock")
        result = setup.add_stock(stock)
        if result:
            return redirect("/addstock")
        flash("Osake on jo lisätty.")
        return redirect("/addstock")
    return render_template("addstock.html", stocks=stocks)

@app.route("/add_dividend", methods=["GET", "POST"])
def add_dividend():
    stocks = que.stocks_from_db(session["username"])
    db_dividends = que.dividends_from_db(session["username"])
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        selection = ["stock", "dividend"]
        if not val.check_selection(selection):
            flash("Valitse osake ja täytä kenttä.")
            return redirect("/add_dividend")
        stock = request.form["stock"]
        dividend = request.form["dividend"].replace(",", ".")
        if not val.stock_price_input(dividend):
            flash("Anna osinko numeroina.")
            return redirect("/add_dividend")
        setup.add_dividend(stock, dividend)
        return redirect ("/add_dividend")
    if not stocks:
        flash("Lisää ensin osake.")
        return redirect("/addstock")
    return render_template("add_dividend.html", stocks=stocks,
                            dividends=db_dividends)

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
        if not val.validate_account(account):
            flash("Tilin nimi on liian pitkä.")
            return redirect("/addaccount")
        result = setup.add_account(account, owner)
        if result:
            flash("Tilin lisäys onnistui")
            return redirect("/addaccount")
        flash("Tilin lisäys ei onnistunut")
        return redirect("/addaccount")
    if not owners:
        flash("Lisää ensin omistaja.")
        return redirect("/addowner")
    return render_template("addaccount.html", owners=owners,
                               pairs=pairs)

@app.route("/addevent", methods=["GET"])
def addevent():
    username = session["username"]
    pairs = que.get_owner_account_pairs(username)
    stocks = que.stocks_from_db(username)
    if not pairs:
        flash("Lisää ensin arvo-osuustili.")
        return redirect("/addaccount")
    if not stocks:
        flash("Lisää ensin osake.")
        return redirect("/addstock")
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
    owner, account = pair[0], pair[1]
    date = request.form["date"]
    stock = request.form["stock"]
    number = request.form["number"]
    price = request.form["price"].replace(",", ".")
    if event_type == "buy":
        type_fin = "osto"
    else:
        type_fin = "myynti"
    result, msg = events.add_event(event_type, owner, account, date, stock,
                     number, price)
    if result:
        return render_template("event.html", event_type=type_fin,
            owner=owner, account=account, date=date, stock=stock,
            number=number, price=price)
    flash(msg)
    return redirect("/addevent")

@app.route("/sell_events", methods=["GET", "POST"])
def sell_events():
    username = session["username"]
    years = que.get_years_with_sell_events(username)
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if not request.form.get("year"):
            flash("Valitse vuosi.")
            return redirect("/sell_events")
        selected_year = request.form["year"]
        s_events = que.sell_events_by_year(selected_year, username)
        return render_template("sell_events.html", years=years,
            selected_year=selected_year, events=s_events)
    if not years:
        flash("Myyntitapahtumia ei ole.")
        return redirect("/")
    return render_template("sell_events.html", years=years)

@app.route("/holdings", methods=["GET"])
def holdings():
    username = session["username"]
    report = que.holdings_report(username)
    if not report:
        flash("Lisäämilläsi omistajilla ei ole omistuksia.")
        return redirect("/")
    return render_template("holdings.html", report=report)

@app.route("/dividends", methods=["GET"])
def dividends():
    username = session["username"]
    report = que.dividend_report(username)
    top_report = que.top_dividendyields(username)
    if not report:
        flash("Lisäämilläsi omistajilla ei ole osinkoja\
              tai osakkeille ei ole lisätty osingon määrää.")
        return redirect("/")
    return render_template("dividends.html", report=report, top_report=top_report)

@app.route("/buy_events", methods=["GET"])
def buy_events():
    username = session["username"]
    report = que.buy_event_report(username)
    if not report:
        flash("Myytävissä olevia osakkeita ei ole.")
        return redirect("/")
    return render_template("buy_events.html", report=report)
