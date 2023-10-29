import requests
from datetime import datetime
import pytz

class FlightSearch():
    def __init__(self) -> None:
        self.search_endpoint = "https://api.tequila.kiwi.com/v2/search"
        self.api_key = "YOUR KEY AS AN ENV VARIABLE"
        self.header = {
            "apikey" : self.api_key
        }

    def reformat_date(self, date:str) -> str:
        """
        Summary
            Takes a date in YYYY-mm-dd format and converts it to dd/mm/YYYY
        Args:
            date (str): YYYY-mm-dd formatted Date
        Returns:
            str: formatted date dd/mm/YYYY
        """

        dt = datetime.strptime(date, "%Y-%m-%d")

        return dt.strftime("%d/%m/%Y")

    def format_times(self, iso_time) -> tuple:
        """
        Summary
            Takes a time in ISO format and converts it to a more userfriendly time
        Args:
            iso_time (str): ISO formatted time
        Returns:
            tuple: formatted date and time
        """
        # Parse
        dt = datetime.fromisoformat(iso_time.replace("z", "+00:00"))

        # Set the timezone
        local_timezone = pytz.timezone("US/Central")
        local_dt = dt.astimezone(local_timezone)

        # Format the Date and Time
        formatted_date = local_dt.strftime("%Y-%m-%d")
        formatted_time = local_dt.strftime("%H:%M %p")

        return formatted_date, formatted_time

    def get_iata_code(self, city) -> str:
        """
        Summary
            Takes a city (Las Vegas) as a parameter and returns the associated IATA code(LAS)
        Args:
            city (str): A city
        Returns:
            str: IATA Code (str)
        """
        self.locations_endpoint = "https://api.tequila.kiwi.com/locations/query"

        params = {
            "term" : city,
            "location_types" : "airport",
            "limit" : 1
        }

        iata_response = requests.get(self.locations_endpoint, headers=self.header, params=params)
        iata_response.raise_for_status()
        data = iata_response.json()

        if data["locations"]:
            iata_code = data["locations"][0]["id"]
            print(iata_code)
            return iata_code
        else:
            return None


    def search_request(self, departure:str, destination:str, departure_date, return_date, adults) -> dict:
        """
        Summary:
            Takes a series of strings as an argument and then formats the data into a query matching the dictionary data to
            parameters inside of the API request.
        Args:
            str(multiple): Departure, Destination, Date From, Date To, Adults
        Returns:
            dict: A dict with the details of the flight
        """
        self.search_params = {
            "fly_from" : departure,
            "fly_to" : destination,
            "date_from" : departure_date,
            "date_to" : departure_date,
            "return_from" : return_date,
            "return_to" : return_date,
            "adults": adults,
            "one_per_date" : 1,
            "curr" : "USD"
        }

        search_response = requests.get(self.search_endpoint, headers=self.header, params=self.search_params)
        search_response.raise_for_status()
        flight_data = search_response.json()["data"]

        if flight_data:
            flight = flight_data[0]
            fly_from = flight["flyFrom"]
            fly_to = flight["flyTo"]
            price = flight["price"]
            departure_time = flight["local_departure"]
            arrival_time = flight["local_arrival"]
            link = flight["deep_link"]

            departure_date, departure_time = self.format_times(departure_time)
            arrival_date, arrival_time = self.format_times(arrival_time)

            found_flight = {
                "from" : fly_from,
                "to" : fly_to,
                "price" : price,
                "departureDate" : departure_date,
                "departureTime" : departure_time,
                "arrivalDate" : arrival_date,
                "arrivalTime" : arrival_time,
                "link" : link
            }

            return found_flight






