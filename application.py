from models import *
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Yurchenko26@localhost:5432/lecture3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)



@app.route("/")
def index():
    flights = Flight.query.all()
    return render_template("index.html", flights=flights)

@app.route("/flight/<int:flight_id>", methods=["POST", "GET"])
def flight(flight_id):
    flight = Flight.query.get(flight_id)

    if flight is None:
        return render_template("error.html", message="No such flight")

    passengers = Passenger.query.filter_by(flight_id = flight_id).all()
    if request.method == "POST":
        name = request.form.get("name")
        passenger = Passenger(name = name, flight_id = flight_id)
        db.session.add(passenger)
        db.session.commit()
        return redirect(f"/flight/{flight_id}")

    return render_template("flight.html", flight=flight, passengers=passengers)

@app.route("/register")
def register():
    flights = Flight.query.all()
    return render_template("register.html", flights=flights)

@app.route("/book", methods=["POST"])
def book():
    name = request.form.get("name")
    try:
        flight_id = int(request.form.get("flight_id"))
    except ValueError:
        return render_template("error.html", message="Wrong flight id")

    passenger = Passenger(name = name, flight_id = flight_id)
    db.session.add(passenger)
    db.session.commit()

    return redirect(f"/flight/{flight_id}")