import json
# import os
import streamlit as st
from PIL import Image
from marketing_generator.user_login_logout import authenticate_and_login
from marketing_generator.camera_picture_generator import take_picture_with_camera
from marketing_generator.prompt_generator import generate_prompts


# Logoneeds to be implemented with an URL Link
# logo_url = 'data:image/png;base64,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'
logo_url = Image.open('./marketing_generator/data/Logo_Reply.png')

def display_login():
    """
    Display login interface.
    """    
    return authenticate_and_login()


def load_customize():
    """
    Load customization settings from JSON file to display restaurant name and url.
    """
 
    with open('./marketing_generator/customize.json', 'r') as f:
        return json.load(f)



def api_ui_framework(name):   
    """
    Create UI framework for the application.
    
    Function sets up the Streamlit user interface and provides options to upload or take pictures and generate prompts.
    """

    # Load the customization dictionary from the JSON file
    login_customize_dict = load_customize()

    # Retrieve URL and Name based on login credentials
    default_url = login_customize_dict.get(name, {}).get("URL", "")
    default_name = login_customize_dict.get(name, {}).get("Name", "")

    # Display logo -> Set to width 300 to keep app mobile responsive
    st.image(logo_url, width=250)
    
    # Set app title based on name from dictionary
    st.title(f'{default_name} Social Media Content Generator')

    # Choose the template for post type and tonality
    tonality, subject,  title_template, linkedin_template, imgdescription_template = generate_prompts()
    
    # Input field for the post topic
    prompt = st.text_input('Post topic: ')
    # prompt = st.text_input('Thema des Beitrags:') 
        
    # Set default URL based on the name
    webpage = st.text_input('Webpage Link:', default_url)
    # webpage = st.text_input('Link zur Webseite:', default_url)
    

    # # Old webpage logic that if the name is not in the dictionary the URL field will be empty 
    # # -> But URL is always provided so no need to check

    # if name in login_customize_dict:
    #     default_url = login_customize_dict[name]["URL"]
    # else:
    #     default_url = ''
    # webpage = st.text_input('Link zur Webseite:', default_url)

    st.write('What type of image would you like to use?')
    # st.write('Welche Art von Bild möchtest du verwenden?')

    # Checkbox for the user to choose if he wants to generate an image with AI
    generatepicture = st.checkbox('Generate image with AI')
    # generatepicture = st.checkbox('Bild mit KI generiern')

    # Option for the user to take a picture using his camera
    st.write('Click on "Take a photo" to take a picture:')
    # st.write('Klicke auf "Foto aufnehmen" um ein Bild aufzunehmen:')
    camera_picture = take_picture_with_camera()
    
    # Option for the user to upload an image from his device -> Needs to be in the format 'png', 'jpg', 'jpeg'
    st.write('Or upload a picture here:')
    #st.write('Oder lade hier ein Bild hoch:')
    uploaded_file = st.file_uploader('Upload image:',
                                    accept_multiple_files=False,
                                    type=['png', 'jpg', 'jpeg']
                                    )
            
    # If file is uploaded display the image in the app
    if uploaded_file:
        Image.open(uploaded_file)
        st.image(uploaded_file)

    # Read the uploaded file into an Image object
    if uploaded_file:
        upload_image = Image.open(uploaded_file)

    else:
        upload_image = None
        uploaded_file = None
         

    return prompt, webpage, uploaded_file, upload_image, camera_picture, tonality, subject, generatepicture, title_template, linkedin_template, imgdescription_template, default_url, default_name
