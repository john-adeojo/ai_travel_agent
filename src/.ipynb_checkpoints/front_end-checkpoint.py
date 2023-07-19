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
    query = f'''Based on the user query: {query_user} do the following: 
Return all of the relevant information required to book the flights.
Some Journeys are indirect meaning they have multiple legs, remember to factor this into your calculation. The prices quoted are the total price for the journey. Use search to return links to the flight booking pages.
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
            
            