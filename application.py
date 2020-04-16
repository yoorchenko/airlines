import os

from flask import Flask, render_template, request, redirect, url_for

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

app = Flask(__name__)

engine = create_engine("postgresql://postgres:Yurchenko26@localhost:5432/lecture3")
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    flights = db.execute("SELECT * FROM flights ORDER BY id ASC").fetchall()
    return render_template("index.html", flights=flights)

@app.route("/flight/<int:flight_id>", methods=["POST", "GET"])
def flight(flight_id):
    flight = db.execute("SELECT * FROM flights WHERE id=:id", {"id":flight_id}).fetchone()

    if flight is None:
        return render_template("error.html", message="No such flight")

    passengers = db.execute("SELECT name FROM passengers WHERE flight_id=:id", {"id":flight_id}).fetchall()
    if request.method == "POST":
        name = request.form.get("name")
        db.execute("INSERT INTO passengers(name, flight_id) VALUES(:name, :flight_id)", {"name":name, "flight_id":flight_id})
        db.commit()
        return redirect(f"/flight/{flight_id}")

    return render_template("flight.html", flight=flight, passengers=passengers)

@app.route("/register")
def register():
    flights = db.execute("SELECT * FROM flights").fetchall()
    return render_template("register.html", flights=flights)

@app.route("/book", methods=["POST"])
def book():
    name = request.form.get("name")
    try:
        flight_id = int(request.form.get("flight_id"))
    except ValueError:
        return render_template("error.html", message="Wrong flight id")

    db.execute("INSERT INTO passengers(name, flight_id) VALUES(:name, :flight_id)", {"name":name, "flight_id":flight_id})
    db.commit()
    return redirect(f"/flight/{flight_id}")