import os
import openai
import streamlit as st
from dotenv import load_dotenv


def setup_api_keys():
    """
    Set up and retrieve API keys for OpenAI and Stable Diffusion.
    
    Function loads environment variables containing API keys and initializes the necessary configurations for OpenAI and Stable Diffusion.
    """
    
    # Load environment variables from .env file
    load_dotenv()

    # Retrieve and set the OpenAI API key from Streamlit's secrets
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    os.environ['OPENAI_API_KEY'] = openai_api_key
    openai.api_key = openai_api_key

    # Retrieve Stable Diffusion API key, Host and Engine from Streamlit's secrets
    engine_id = "stable-diffusion-xl-1024-v1-0"  # Default engine ID
    api_host = st.secrets.get("api_host", 'https://api.stability.ai')
    sd_api_key = st.secrets["STABILITY_API_KEY"]

    return engine_id, api_host, sd_api_key
