import json
import openai
from langchain.tools import tool
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
# from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI


def get_args(query_user, openai_key):
    # OpenAI function calling

    function_call = [
    {
      "name": "search_for_flights",
      "description": "Requests flight data from Amadeus API and writes to SQLite database",
      "parameters": {
        "type": "object",
        "properties": {
            "num_adults":{
                "type":"integer",
                "description": '''Based on the query, respond with the number of adults'''
            },
            "departureDate": {
                "type":"string",
                "description": '''Based on the query, respond with the Departure Date. Dates are specified in the ISO 8601 YYYY-MM-DD format. '''
            },
            "returnDate": {
                "type":"string",
                "description": '''Based on the query, respond with the Return Date. Dates are specified in the ISO 8601 YYYY-MM-DD format. '''
            },
            "destinationLocationCode":{
                "type":"string",
                "description": '''Based on the query, respond with an airport IATA code from the city which the traveler is going. E.g CDG for Charles de Gaulle Airport'''
            },
          "originLocationCode": {
            "type": "string",
            "description": '''Based on the query, respond with an airport IATA code from the city which the traveler will depart from. E.g CDG for Charles de Gaulle Airport'''
          },

        },
        "required": ["destinationLocationCode", "originLocationCode", "departureDate", "returnDate", "num_adults"]
      }
    }
    ]
    
    openai.api_key = openai_key

    message = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[{"role": "user", "content": query_user}],
        functions = function_call,
        function_call = 'auto',
        temperature=0
    )
    response_message = message["choices"][0]["message"]["function_call"]["arguments"]

    parsed_data = json.loads(response_message)

    # Accessing variables
    num_adults = parsed_data['num_adults']
    departureDate = parsed_data['departureDate']
    returnDate = parsed_data['returnDate']
    destinationLocationCode = parsed_data['destinationLocationCode']
    originLocationCode = parsed_data['originLocationCode']
    
    print("Number of Adults: ", num_adults)
    print("Departure Date: ", departureDate)
    print("Return Date: ", returnDate)
    print("Destination Location Code: ", destinationLocationCode)
    print("Origin Location Code: ", originLocationCode)

    return num_adults, departureDate, returnDate, destinationLocationCode, originLocationCode


# run SQLDatabase chain
def find_flights(query, llm, db):
    
    llm=llm
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )
 
    return agent_executor.run(query)


