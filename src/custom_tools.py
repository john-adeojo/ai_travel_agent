from amadeus import Client, ResponseError
from datetime import datetime



@tool
def search_for_flights(originLocationCode: str, destinationLocationCode: str, departureDate: datetime, num_adults: int) -> list:
    """ Searches Amadeous API for flights"""
    
    # Assuming you've defined api_key and api_secret somewhere else
    amadeus = Client(client_id=api_key, client_secret=api_secret)

    # Defining the parameters for the flight
    params = {
        'originLocationCode': originLocationCode,
        'destinationLocationCode': destinationLocationCode,
        'departureDate': departureDate.strftime('%Y-%m-%d'),  # API might require specific date format
        'adults': num_adults
        # add or modify other parameters according to your needs
    }
    
    try:
        response_flights = amadeus.shopping.flight_offers_search.get(**params)
        
    except ResponseError as error:
        print(f"ResponseError occurred: {error}")
        print(f"Error code: {error.code}")
        print(f"Error message: {error.description}")
        return []  # return an empty list in case of an error

    return response_flights.data
