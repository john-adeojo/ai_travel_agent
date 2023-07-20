"""
This module provides the function for requesting data from the flights API.
It uses transform_data() and load_data() to transform the data and load it
into the sqllite database.
"""

from amadeus import Client, ResponseError
from create_database import load_data
from data_transformation import transform_data
from utils import read_config
import os

def pull_flights(originLocationCode, destinationLocationCode, departureDate, returnDate, num_adults):
    """
    Searches for flights using the Amadeus API and returns structured data.

    This function uses the Amadeus flight search API to find flights matching the given parameters. 
    It also retrieves airline lookup data using the Amadeus reference data API. The raw response data 
    from both APIs is processed into structured dataframes using the `journey_data()` function. 
    This processed data is then loaded into an SQLite database using the `load_data()` function.

    Parameters:
    originLocationCode (str): The IATA code of the origin location.
    destinationLocationCode (str): The IATA code of the destination location.
    departureDate (str): The desired departure date in 'YYYY-MM-DD' format.
    returnDate (str): The desired return date in 'YYYY-MM-DD' format.
    num_adults (int): The number of adults for the flight.

    Returns:
    db (SQLDatabase): An SQLite database containing the processed flight data.
    """

    
    try:
        api_key, api_secret = read_config()
    except Exception as e:
        print(f"Failed to read API key from config: {e}, trying other key")
        api_key = os.getenv('API_KEY')  # make sure this environment variable is set
        api_secret = os.getenv('API_SECRET')

    # Assuming you've defined api_key and api_secret somewhere else
    amadeus = Client(client_id=api_key, client_secret=api_secret)

    # Defining the parameters for the flight
    params = {
        'originLocationCode': originLocationCode,
        'destinationLocationCode': destinationLocationCode,
        'departureDate': departureDate,
        'returnDate': returnDate,
        'adults': num_adults
    }
    
    try:
        response_flights = amadeus.shopping.flight_offers_search.get(**params)
        
    except ResponseError as error:
        print(f"ResponseError occurred flights: {error}")
        print(f"Error code flights: {error.code}")
        print(f"Error message flights: {error.description}")
        return []  # return an empty list in case of an error

    try:
        response_airline_lookup = amadeus.reference_data.airlines.get()

    except ResponseError as error:
        print(f"ResponseError occurred airline lookup: {error}")
        print(f"Error code airline lookup: {error.code}")
        print(f"Error message airline lookup: {error.description}")

    df_flights, journey_pricing, flights = transform_data(response_flights.data, response_airline_lookup.data, destinationLocationCode, originLocationCode)
    print(df_flights.dtypes)
    db = load_data(journey_pricing, flights)

    return db
