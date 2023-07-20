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
    script_dir = "../src/"

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

# def query_template(query_user):

#     query = f'''Based on the user query about flights:{query_user}, respond with the following structure delimited by quotation marks as an example:
    
# "
# The response should be returned with the structure given for this for the example of a customer flying from London to Tokyo and back requesting the journey: 

# I now have the 20 cheapest Journeys from London to Tokyo departing on the 30th of August 2023 and returning on the 15th of September 2023. 

# |   Journey ID | Travel Direction   | Departure           | Arrival             | Journey Start   | Journey End   | Intermediate Departure   | Intermediate Arrival   | Airline    |   Flight Duration (hrs) | Total       |
# |-------------:|:-------------------|:--------------------|:--------------------|:----------------|:--------------|:-------------------------|:-----------------------|:-----------|------------------------:|:------------|
# |          167 | Outbound           | 2023-08-30T09:40:00 | 2023-08-31T10:40:00 | LHR             | HND           | N/A                      | CDG                    | AIR France |                     10.5 | 1422.79 EUR |
# |          167 | Outbound           | 2023-08-31T10:40:00 | 2023-08-31T22:40:00 | LHR             | HND           | CDG                      | N/A                    | AIR France |                      3.5 |            |
# |          167 | Inbound            | 2023-09-15T09:40:00 | 2023-09-16T05:35:00 | HND             | LHR           | N/A                      | CDG                    | AIR France |                     10.5 |            |
# |          167 | Inbound            | 2023-09-16T06:35:00 | 2023-09-16T07:35:00 | HND             | LHR           | CDG                      | N/A                    | AIR France |                      3.5 |            |
# |          168 | Outbound           | 2023-08-30T09:40:00 | 2023-08-31T22:40:00 | LHR             | HND           | N/A                      | N/A                    | Air Tokyo  |                     10.5 | 1550 EUR    |
# |          168 | Inbound            | 2023-09-15T09:40:00 | 2023-09-16T07:35:00 | HND             | LHR           | n/a                      | N/A                    | Air Tokyo  |                      3.5 |            |

# "
# Return all legs for each Journey ID. when the requests mentions flight or flights, it really means Journey.

# '''
#     return query


def query_template(query_user):

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

    query = f'''Based on the user query about flights:{query_user}, respond with following structure delimited by quotation marks as an example:
    
"
The response should be returned with the structure given which represents one complete journey: 

## Journey ID: , Total (In the currency):

### Outbound
For each leg ID, please consider:
- Departure	
- Arrival	
- Journey Start	
- Journey End 
- Intermediate Departure	
- Intermediate Arrival	
- Airline	
- Total Duration (hrs)	

### Inbound
For each leg ID, please consider:
- Departure	
- Arrival	
- Journey Start	
- Journey End 
- Intermediate Departure	
- Intermediate Arrival	
- Airline	
- Total Duration (hrs)	

"
Please return up to 8 COMPLETE journeys. A complete journey includes all the associated flights.
Return all legs for each Journey ID. when the requests mentions flight or flights, it really means Journey.

'''
    return query