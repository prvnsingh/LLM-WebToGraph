import requests
import streamlit as st

st.title("LLM-WebToGraph")
st.text(
    'This project using langchain and OpenAI LLM to transform data from different sources (weblinks/csv) to knowledge graph and store then in neo4j DB.')
st.write('Press submit to upload process the data and generate knowledge graph.')

if st.button("process csv files and generate knowledge graph"):
    # Send user_input to FastAPI
    fastapi_url = "http://localhost:8000//generate_tags_from_csv"
    response = requests.get(fastapi_url)
    if response.status_code == 200:
        st.write(f"{response.text}")
    else:
        st.error(f"Error: {response.status_code}")

if st.button("process html links and generate knowledge graph"):
    # Send user_input to FastAPI
    fastapi_url = "http://localhost:8000//generate_tags_from_html"
    response = requests.get(fastapi_url)
    if response.status_code == 200:
        st.write(f"{response.text}")
    else:
        st.error(f"Error: {response.status_code}")

user_input = st.text_input("ask any question about data")
if st.button('submit'):
    # Send user_input to FastAPI
    fastapi_url = f"http://localhost:8000/query_graph/{user_input}"
    response = requests.get(fastapi_url)
    if response.status_code == 200:
        st.write(f"{response.text}")
    else:
        st.error(f"Error: {response.status_code}")
