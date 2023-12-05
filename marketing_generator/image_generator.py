import base64
import requests
import streamlit as st
from marketing_generator.user_config import setup_api_keys


def sd_generate_image(imgdescription):
    """
    Generate an image using the Stable Diffusion API based on text description.

    Function generate an image based on the provided text description.
    """

    # Get the engine ID, API host, and SD API key from config
    engine_id, api_host, sd_api_key = setup_api_keys()

    # Check if the SD API key is missing
    if sd_api_key is None:
        raise Exception("Missing Stability API key.")

    # Send a POST request to the SD API to generate an image
    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {sd_api_key}"
        },
        json={
            "text_prompts": [
                {
                    "text": imgdescription
                }
            ],
            "cfg_scale": 7,
            "clip_guidance_preset": "FAST_BLUE",
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 40,
        },
    )

    # Check if response status is not 200 (Status Code 200 -> success)
    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    # Parse response JSON data
    data = response.json()

    # Parse the response JSON data
    for i, image in enumerate(data["artifacts"]):
        image_data = base64.b64decode(image["base64"])

        # Display generated image in the App
        st.image(image_data, caption='Stable Diffusion Generated Image')
       
        return image_data