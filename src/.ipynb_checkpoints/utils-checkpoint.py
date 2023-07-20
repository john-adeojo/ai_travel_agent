"""
This module provides utility functions
"""

import yaml
import os
from dateutil.relativedelta import relativedelta
import re

def read_config():
    """
    Reads API key and secret from a configuration file.

    This function opens a configuration file named "apikeys.yml", reads the API key and secret for 
    the Amadeus Flights API, and returns these values.

    Returns:
    api_key (str): The API key for the Amadeus Flights API.
    api_secret (str): The API secret for the Amadeus Flights API.
    """
    
    # Get the directory of the current script
    script_dir = "C:/Users/johna/OneDrive/Documents/api_keys"

    # Construct the full path to the configuration file
    file_path = os.path.join(script_dir, "apikeys.yml")

    with open(file_path, 'r') as stream:
        try:
            configs = yaml.safe_load(stream)
            api_key = configs['amadeues_flights']['api_key']
            api_secret = configs['amadeues_flights']['api_secret']

            return api_key, api_secret
        except yaml.YAMLError as exc:
            print(exc)
            
    return api_key, api_secret

class SingletonToken:
    """
    Implements a singleton token.

    This class is used to implement a singleton token which can be set and retrieved using the 
    set_token() and get_token() class methods respectively. The token is stored in a private class 
    variable and can be accessed across different instances of the class.
    """
    __token = None

    @classmethod
    def set_token(cls, token):
        cls.__token = token

    @classmethod
    def get_token(cls):
        return cls.__token


def parse_duration(duration_str):
    """
    Parses a duration string and returns the duration in hours.

    This function takes a duration string of the form 'PTxHxM', where 'x' represents a number, 
    extracts the hours and minutes, and returns the total duration in hours.

    Parameters:
    duration_str (str): A string representing the duration in the form 'PTxHxM'.

    Returns:
    duration_in_hours (float): The total duration in hours.
    """
    
    # Extract hours and minutes from the duration string
    hours = re.search('(\d+)H', duration_str)
    minutes = re.search('(\d+)M', duration_str)
    
    # Convert hours and minutes to integers and calculate the total duration in hours
    hours = int(hours.group(1)) if hours else 0
    minutes = int(minutes.group(1)) if minutes else 0
    duration_in_hours = hours + minutes / 60

    return duration_in_hours

def query_template(num_adults, departureDate, returnDate, destinationLocationCode, originLocationCode, TypeofflightReuqest):

    """
    Generates a formatted query string for flight search based on the user query.

    This function takes a user query about flights and formats it into a string that describes the 
    required structure of the response. The structure includes details about the outbound and inbound 
    flights for each journey, and each leg within these flights.

    Parameters:
    query_user (str): A string representing the user's query about flights.

    Returns:
    query (str): A formatted string that describes the required structure of the response.
    """

    query = f'''Find me the {TypeofflightReuqest} journey from {originLocationCode} to {destinationLocationCode}. 
    Departing from {originLocationCode} on {departureDate} and returning from {destinationLocationCode} on {returnDate}.
    
    respond with following structure delimited by quotation marks as an example for a journey with 4 legs, 2 for Outbound and 2 for Inbound flights:
    
## Journey ID: 1, Total (currency): 

### travel_direction: Outbound, Journey Start: , Journey End: , total_duration(hrs): 
**leg_id:1**
- Departure Time:
- Arrival Time: 
- Intermediate Departure: 	
- Intermediate Arrival:
- Airline:
- flight_duration (hrs):

**leg_id:2**
- Departure Time:######
- Arrival Time: #####
- Intermediate Departure:	
- Intermediate Arrival:
- Airline:
- flight_duration (hrs):

### travel_direction: Inbound, Journey Start: , Journey End: , total_duration(hrs): 
**leg_id:3**
- Departure Time:
- Arrival Time:
- Intermediate Departure:	
- Intermediate Arrival:
- Airline:
- flight_duration (hrs):

**leg_id:4**
- Departure Time
- Arrival Time: 
- Intermediate Departure:	
- Intermediate Arrival:
- Airline:
- flight_duration (hrs):

'''
    return query