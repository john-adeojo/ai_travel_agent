import streamlit as st
import pandas as pd
from utils import SingletonToken
from run_chains import get_args, find_flights
from search_flights import search_for_flights
import io
from io import StringIO
from langchain.chat_models import ChatOpenAI


st.markdown(
    
    """
    #### Prototype Built by [Data-Centric Solutions](https://www.data-centric-solutions.com/)
    """,
    unsafe_allow_html=True,
)

# Side panel for OpenAI token input
st.sidebar.title("Configuration")
openai_key = st.sidebar.text_input("Enter OpenAI Key", type="password")

# Initialize an empty placeholder
placeholder = st.empty()

if openai_key:
    SingletonToken.set_token(openai_key)
    openai_key = SingletonToken.get_token()
    print("API_KEY!!!", openai_key)
    
    # If OpenAI key and data_url are set, enable the chat interface
    st.title("Find my flights🛫 ")
    query_user = placeholder.text_input("Search for flights...")
    query = f'''Based on the user query about flights:{query_user}, respond with the following structure delimited by quotation marks as an example:
    
"
The response should be returned like this for the example of a customer flying from London to Tokyo and back: 

I now have the 5 cheapest Journeys from London to Tokyo departing on the 30th of August 2023 and returning on the 15th of September 2023. 

| Journey ID   |   Leg ID | Outbound Departure   | Outbound Arrival    | Return Departure    | Return Arrival      | Journey Start    | Journey End   | Intermediate Departure   | Intermediate Arrival   | Airline    | Total       |
|:-------------|---------:|:---------------------|:--------------------|:--------------------|:--------------------|:-----------------|:--------------|:-------------------------|:-----------------------|:-----------|:------------|
| 167.0        |        1 | 2023-08-30T09:40:00  | 2023-08-31T10:40:00 | N/A                 | N/A                 | LHR              | HND           | N/A                      | CDG                    | AIR France | 1422.79 EUR |
|              |        2 | 2023-08-31T10:40:00  | 2023-08-31T22:40:00 | N/A                 | N/A                 | LHR              | HND           | CDG                      | N/A                    | AIR France |             |
|              |        1 | N/A                  | N/A                 | 2023-09-15T09:40:00 | 2023-09-16T05:35:00 | HND              | LHR           | N/A                      | CDG                    | AIR France |             |
|              |        2 | N/A                  | N/A                 | 2023-09-16T06:35:00 | 2023-09-16T07:35:00 | HND              | LHR           | CDG                      | N/A                    | AIR France |             |
| 168.0        |        1 | 2023-08-30T09:40:00  | 2023-08-31T22:40:00 | N/A                 | N/A                 | LHR              | HND           | N/A                      | N/A                    | Air Tokyo  | 1550 EUR    |
|              |        1 | N/A                  | N/A                 | 2023-09-15T09:40:00 | 2023-09-16T07:35:00 | HND              | LHR           | N/A                      | N/A                    | Air Tokyo  |             |
   Report all legs for each Journey ID. when the requests mentions flight or flights, it really means Journey.o legs.

'''
    
    if st.button("Submit"):
        num_adults, departureDate, returnDate, destinationLocationCode, originLocationCode = get_args(query_user, openai_key)
        db, df_flights = search_for_flights(originLocationCode, destinationLocationCode, departureDate, returnDate, num_adults)
        llm=ChatOpenAI(temperature=0, model="gpt-4-0613", openai_api_key=openai_key)
        response = find_flights(query, llm, db)
        st.markdown(f"Suggestions: {response}")
        
        # st.write("Response: ", response)

else:
    # If OpenAI key and data_url are not set, show a message
    placeholder.markdown(
        """
        **Please enter your OpenAI key and data URL in the sidebar.**
        
        Follow this [link](https://www.howtogeek.com/885918/how-to-get-an-openai-api-key/) to get your OpenAI API key.
        """,
        unsafe_allow_html=True,
    )
            
            