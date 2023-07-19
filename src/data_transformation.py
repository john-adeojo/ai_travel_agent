import pandas as pd

def journey_data(response_flights_data, response_airline_lookup_data, originLocationCode, destinationLocationCode):
    # Load the data into a DataFrame
    df = pd.DataFrame(response_flights_data)
    df_airline_codes = pd.json_normalize(response_airline_lookup_data)
    
    # Extract itineraries, validatingAirlineCodes, price (total and currency) and id into separate dataframes
    df_itineraries = df[['id', 'itineraries']].explode('itineraries').reset_index(drop=True)
    
    # In the itineraries column, each cell is a dictionary. So, we need to convert those dictionaries into separate columns.
    df_itineraries = df_itineraries.join(pd.json_normalize(df_itineraries['itineraries'])).drop(columns='itineraries')
    
    # At this point, 'segments' column is a list of dictionaries where each dictionary represents a leg of the journey.
    # We want each leg to be a separate row in the dataframe. So, explode the 'segments' column.
    df_itineraries = df_itineraries.explode('segments').reset_index(drop=True)
    
    # Add a 'leg_id' column to identify each leg of the journey
    df_itineraries['leg_id'] = df_itineraries.groupby('id').cumcount() + 1
    
    # Now, convert the dictionaries in the 'segments' column into separate columns
    df_segments = pd.json_normalize(df_itineraries['segments'])
    
    # To avoid overlapping columns, add a prefix to the column names of the new dataframe
    df_segments.columns = ['flight_' + str(col) for col in df_segments.columns]
    
    # Now join the original dataframe with the new one
    df_itineraries = df_itineraries.join(df_segments).drop(columns='segments')
    
    df_validatingAirlineCodes = df[['id', 'validatingAirlineCodes']]
    
    # For the price column, we only need total and currency. So, extract only those into a new dataframe
    df_price = df['price'].apply(pd.Series)[['total', 'currency']]
    df_price['id'] = df['id']
    
    # Now join these dataframes on the 'id' column
    df_flights = pd.merge(df_itineraries, df_validatingAirlineCodes, on='id')
    df_flights = pd.merge(df_flights, df_price, on='id')
    
    # Create a new column for the total number of legs per journey
    df_flights['total_legs'] = df_flights.groupby('id')['leg_id'].transform('max')
    
    df_flights = df_flights.merge(right=df_airline_codes, how='left', left_on="flight_operating.carrierCode", right_on="iataCode")
    df_flights.rename(columns={"id":"journey_id", "commonName":"airline", "flight_arrival_at": "flight_arrival_time", "flight_departure_at": "flight_departure_time"  }, inplace=True)

    df_flights.drop(columns=["flight_id", "validatingAirlineCodes", "businessName", "flight_operating.carrierCode", "flight_aircraft.code", "flight_stops"], inplace=True)

    df_flights.columns = df_flights.columns.str.replace('.', '_')
    df_flights['total'] = pd.to_numeric(df_flights['total'], errors='coerce')

    outbound_origin = originLocationCode
    outbound_destination = destinationLocationCode
    inbound_origin = destinationLocationCode
    inbound_destination = originLocationCode

    # Create conditions
    cond1 = (df_flights['flight_departure_iataCode'] == outbound_origin) | (df_flights['flight_arrival_iataCode'] == destinationLocationCode)
    cond2 = (df_flights['flight_departure_iataCode'] == inbound_origin) | (df_flights['flight_arrival_iataCode'] == inbound_destination)

    # Update 'Journey Start' and 'Journey End' based on conditions
    df_flights.loc[cond1, 'Journey Start'] = originLocationCode
    df_flights.loc[cond1, 'Journey End'] = destinationLocationCode
    df_flights.loc[cond2, 'Journey Start'] = destinationLocationCode
    df_flights.loc[cond2, 'Journey End'] = originLocationCode
    
    # Update 'travel_direction' based on 'Journey Start'
    df_flights.loc[df_flights['Journey Start'] == originLocationCode, 'travel_direction'] = 'Inbound'
    df_flights.loc[df_flights['Journey Start'] == destinationLocationCode, 'travel_direction'] = 'Outbound'

    df_flights.loc[df_flights['flight_arrival_iataCode'] == df_flights['Journey End'], 'flight_arrival_iataCode'] = 'N/A'
    df_flights.loc[df_flights['flight_departure_iataCode'] == df_flights['Journey Start'], 'flight_departure_iataCode'] = 'N/A'

    df_flights.rename(columns={'flight_departure_iataCode': 'intermediate_journey_departure', 
                           'flight_arrival_iataCode': 'intermediate_journey_arrival'}, inplace=True)

    return df_flights