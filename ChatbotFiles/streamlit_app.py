import streamlit as st
from openai import OpenAI
from bd_model import get_response
import os, traceback
from pubmed_parser import MetadataFinder
def read_api_key(file_path):
    try:
        with open(file_path, 'r') as file:
            api_key = file.read().strip()  # Read the key and strip any extra whitespace
        return api_key
    except FileNotFoundError:
        print("API key file not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

OPENAPI_API_KEY='./GMU_HAP_OPENAI_API_KEY.txt'
OPENAPI_API_KEY = read_api_key(OPENAPI_API_KEY)
os.environ['OPENAI_API_KEY'] = OPENAPI_API_KEY

st.title("💬 Bipolar Disorder Queries")
query = st.text_area("What would you like to ask?")

if st.button("Submit"):
    if not query.strip():
        st.error(f"Please provide the search query.")
    else:
        try:
            response, resp_src = get_response(query)
            # print(f"###########{response.filename}########")
            st.success(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.error(traceback.format_exc())