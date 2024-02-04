# A module handling the web requests, posts and navigation
from flaskapp.app import app
from flask import flash, redirect, render_template, request
from services import events

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/setup", methods=["GET", "POST"])
def setup(): #under construction
    if request.method == "GET": #?
        return render_template("setup.html")
    if request.method == "POST":
        #kutsutaan funktiota, joka tallentaa tiedot?
        return redirect("/")

@app.route("/addevent", methods=["GET", "POST"])
def addevent():
    #if request.method == "GET": #?
    return render_template("addevent.html")
    #if request.method == "POST":
        #flash("Tapahtuman lisäys onnistui!")
    #    return redirect("/")

@app.route("/event", methods=["POST"])
def event():
    event_type = request.form["event_type"]
    owner = request.form["owner"]
    account = request.form["account"]
    date = request.form["date"]
    stock = request.form["stock"]
    number = request.form["number"]
    price = request.form["price"]
    events.add_event(event_type, owner, account, date, stock,
                     number, price)
    return render_template("event.html", event_type=event_type,
        owner=owner, account=account, date=date, stock=stock,
        number=number, price=price)

@app.route("/holdings", methods=["GET", "POST"])
def holdings():
    if request.method == "GET":
        return render_template("holdings.html")
