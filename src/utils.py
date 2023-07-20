import yaml
import os

def read_config():
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
    __token = None

    @classmethod
    def set_token(cls, token):
        cls.__token = token

    @classmethod
    def get_token(cls):
        return cls.__token

from dateutil.relativedelta import relativedelta
import re

def parse_duration(duration_str):
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

    query = f'''Based on the user query about flights:{query_user}, respond with following structure delimited by quotation marks as an example:
    
"
The response should be returned with the structure given which represents one complete journey: 

Journey ID - Outbound
- Departure	
- Arrival	
- Journey Start	
- Journey End 
- Intermediate Departure	
- Intermediate Arrival	
- Airline	
- Flight Duration (hrs)	
- Total

Journey ID - Inbound
- Departure	
- Arrival	
- Journey Start	
- Journey End 
- Intermediate Departure	
- Intermediate Arrival	
- Airline	
- Flight Duration (hrs)	
- Total

return up to five complete journeys. A complete journey includes all the associated flights.

"
Return all legs for each Journey ID. when the requests mentions flight or flights, it really means Journey.

'''
    return query