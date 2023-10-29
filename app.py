# Import libraries
import re

from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from search import FlightSearch


# Initialize Classes
app = Flask(__name__)
search = FlightSearch()


# Routes
@app.route("/")
def index():
    """
        Summary:
            Directs to the main index page of the website
    """
    return render_template("index.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    """
        Summary:
            Directs to the signup page or the login page depending on method
        Returns:
            signup.html or login.html depending on method
        """
    if request.method == "POST":
        # Get the input values from the form
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("confirmation")

        # Back-end password validation
        if password != password_confirm:
            error = "Password's do not match"
            return render_template("signup.html", error=error)

        # Hash the password
        hashed_password = generate_password_hash(password, method="sha256")

        # Create a new user in the database
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Successfully registered as a new user!", "success")
        return redirect("/login")
    else:
        return render_template("signup.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    """
        Summary:
            Obtains input values from the login form and if valid redirects to '/'
        Returns:
            index page if valid credentials else returns the login page to try again
        """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            flash("Login Successful", "success")
            return redirect("/")
    else:
        flash("Either your username doesn't exist, or the password is not correct", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    """
        Summary:
            Logs the user out and clears their session
        Returns:
            index.html
        """

    # Clear the current session(user_id)
    session.clear()

    # Show log out process was successfull
    flash("Successfully logged out")

    # Redirect to index
    return redirect("/")


@app.route("/flight", methods=["POST", "GET"])
def flights():
    """
        Summary:
            Obtains user input from the flight form and parses the data,
            obtains the IATA code for the specified city, and then makes an API
            query to Tequila by Kiwi flight search
        Returns:
            a dictionary which is passed to the results.html page
        """
    if request.method == "POST":

        # Get the Departure and Arrival IATA Code from the city
        departure_city = request.form.get("departureCity")
        destination_city = request.form.get("destinationCity")

        # Obtain IATA codes for cities
        departure_iata = search.get_iata_code(departure_city)
        destination_iata = search.get_iata_code(destination_city)

        # Get Dates and Adults from forms
        departure_date_input = request.form.get("departureDateStart")
        return_date_input = request.form.get("departureDateEnd")
        adults = request.form.get("adults")

        # Format date to: DD/MM/YYYY for search api requirements
        departure_date = search.reformat_date(departure_date_input)
        return_date = search.reformat_date(return_date_input)

        # Search API for flight
        flight_data = search.search_request(departure=departure_iata, destination=destination_iata, departure_date=departure_date, return_date=return_date, adults=adults)

        return render_template("results.html", flight=flight_data)

    else:
        return render_template("flight.html")


@app.route("/about")
def about():
    """
        Summary:
            Directs the user to the About page
        """
    return render_template("about.html")


@app.route("/faqs")
def faqs():
    """
        Summary:
            Directs the user to the FAQs page
        """
    return render_template("faqs.html")


@app.route("/history")
#LOGIN REQUIRED
def history():
    """
        Summary:
            Directs the user to the About page
        """
    pass

