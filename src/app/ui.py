import json

import streamlit as st
import requests



st.title("LLM-WebToGraph")
st.text('This project using langchain and OpenAI LLM to transform data from different sources (weblinks/csv) to knowledge graph and store then in neo4j DB.')
st.write('Press submit to upload process the data and generate knowledge graph.')

if st.button("Submit"):
    # Send user_input to FastAPI
    fastapi_url = "http://localhost:8000/generate_tags"
    response = requests.get(fastapi_url)
    if response.status_code == 200:
        st.write(f"{response.text}")
    else:
        st.error(f"Error: {response.status_code}")


