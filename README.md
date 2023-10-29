# Flight Search

#### Video Demo:


## Overview
This is a website which is using HTML/CSS/Javascript (FRONT-END) and Python and Flask (BACK-END). On a website named 'Star Travel', you are
given the opportunity to use Tequila by KIWI's flight search api via a website to search for cheap flights. For the time being only the cheapest flight for any given inquiry is returned


## Installation

1. Ensure you have Python 3.8 or newer installed on your system. You can download it from [here](https://www.python.org/downloads/).
2. Install the required packages:
    -flask
    -flask-Session
    -Flask-SQLAlchemy
    -requests
    -datetime
    -pytz

### Usage
    This is a html5 website which allows you to search for cheap flights via the root ('/') webpage via the short form search for flights or through a more visually appealing flights.html form.


#### Design Choices
    After scouring over many different flight search websites, I decided to have a multi-page website, which includes:
        - Home/Index, which shows the top 3 current travel destinations via an image carousel, an 'app' which is a link to either google play store or the Apple App store, as well as a quick search function
        - Flights, which allows you to enter a departure, destination, departure date, return date, and the number of adults
        - About, brief history of the website
        - FAQs page, which answers frequently asked questions with a sidebar with on-page links
        - results page which is the return of the /flight form post method which shows the flight in a tabular format


##### Options
The basic search query is ran via Tequila via KIWI's API with the following options:

    - Departure
    - Destination
    - Departure Date
    - Return Date
    - Number of adults


###### Usage/Flow
For the basic usage of the program, it doesn't require you to enter the IATA (Airport code) for the departure or destination airport instead,
the user inputs their desired departure and destination cities.

These cities are then passed through to Kiwi's location API, which queries for their corresponding IATA code for the desired city, if multiple are listed, it returns only one.

The IATA code is then passed in as a JSON payload along with other parameters

Kiwi requires a specific date format, so when the user's input is captured via the "Date" type from HTML, it is then sent to the search class, which converts it from:
YYYY-MM-DD to MM/DD/YYYY as requried by the KIWI flight search

The FlightSearch Class then takes these parameters along with the number of adults and queries the main v2/search for a JSON of the cheapest flight available for the date range given

The user is then redirected to the /results page where the results are shown along with a Book button, which allows the user to actually book and pay for the flight VIA Kiwi's websitea


###### Future Design implmentations
I would like to add the following features to future versions of this website:
    - More search parameters, allowing the website to show more than just one flight
    - Login/Logout feature with a history tab, showing all purchased flights, along with other features
        - The login/logout feature was developed on my local VSCODE IDE, however CS50's library and online VSCode editor were having compatibility issues with SQL-Alchemy, so I just removed the feature, however the forms and backend logic are still there to be seen
    - Update the page with a better UX/UI, to me at the moment it looks decent, but I would like to develop this site further
