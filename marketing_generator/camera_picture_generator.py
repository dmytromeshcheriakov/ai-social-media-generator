import streamlit as st
from PIL import Image

def take_picture_with_camera():
    """
    Take a picture using the device's camera and return it as a PIL image.

    Function creates a Streamlit interface for taking a picture using the device's camera.
    It provides a button to initiate the camera capture and returns the captured image as a PIL image object.
    """

    # If 'take_picture_button' key not in session_state -> session_state is False
    # This way the camera of the device is not automatically active
    if 'take_picture_button' not in st.session_state:
        st.session_state.take_picture_button = False

    # Create Take Picture Button
    take_picture_button = st.button('Take a photo')
    # take_picture_button = st.button('Foto aufnehmen')

    # If Take Picture button is clicked -> session_state is True
    if take_picture_button:
        st.session_state.take_picture_button = True

    # If session stateis True -> Show Camera 
    if st.session_state.take_picture_button:
        picture = st.camera_input('Camera Input', label_visibility='hidden')

        # If Confirm Button is True -> return picture
        if picture is not None:
           camera_picture = Image.open(picture)
           return camera_picture
        
    return None