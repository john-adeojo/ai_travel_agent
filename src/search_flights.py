from amadeus import Client, ResponseError
from create_database import load_data
from data_transformation import journey_data
from utils import read_config
import os


def search_for_flights(originLocationCode, destinationLocationCode, departureDate, returnDate, num_adults):
    # get API keys
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

    df_flights = journey_data(response_flights.data, response_airline_lookup.data, originLocationCode, destinationLocationCode)
    db = load_data(df_flights)

    return db, df_flights
