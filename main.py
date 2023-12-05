import streamlit as st
from marketing_generator.ui_framework import api_ui_framework, display_login
from marketing_generator.user_config import setup_api_keys
from marketing_generator.prompt_generator import generate_prompts
from marketing_generator.llm_chain import run_llm_chain
# from marketing_generator.llm_chain import run_llm_chain, email_attachments
from marketing_generator.user_login_logout import authenticate_and_login, user_logout, create_authenticator
from marketing_generator.final_result_generator import display_final_result

# Initialize the session state variable
if "current_view" not in st.session_state:
    st.session_state.current_view = "main"


# Call function to initialize OpenAI
engine_id, api_host, sd_api_key = setup_api_keys()

# Call function to initialize authenticator
authenticator = create_authenticator()

# Call function to authenticate user
name, authentication_status, username = authenticate_and_login(authenticator)

# If user is not authenticated stop
if authentication_status is None:
    st.stop()

# If the user is authenticated, proceed
if st.session_state.current_view == "main":

    # If reset_main True -> Reset start page
    if st.session_state.get('reset_main', False):
        
        st.session_state.title_template = None
        st.session_state.linkedin_template = None
        # st.session_state.title = None
        # st.session_state.linkedin = None
        # st.session_state.camera_picture = None
        # st.session_state.upload_image = None
        # st.session_state.generated_image_data = None

        # Clear text session states
        #st.session_state.title_text = None
        #st.session_state.linkedin_text = None

        # Reset the flag
        st.session_state.take_picture_button = False
        st.session_state.reset_main = False

    # If the user is authenticated, proceed
    if authentication_status:
        prompt, webpage, uploaded_file, upload_image, camera_picture, tonality, subject, generatepicture, title_template, linkedin_template, imgdescription_template, default_url, default_name  = api_ui_framework(name)

        if uploaded_file is None or upload_image is None or camera_picture is None :
            pass
        
        # Call llm chain function to get the generated title and LinkedIn data
        output = run_llm_chain(name, title_template, linkedin_template, imgdescription_template, prompt, webpage, subject, generatepicture, default_url, default_name)

        # if there is an output send the output as an email
        if output:
            name, title, linkedin, imgdescription_chain, generated_image_data, title_chain, linkedin_chain, prompt, webpage_data = output
            st.session_state.title_chain = title_chain
            st.session_state.linkedin_chain = linkedin_chain
            st.session_state.prompt = prompt
            st.session_state.webpage_data = webpage_data
            
            run = display_final_result(name, title, linkedin, camera_picture, upload_image, generated_image_data, prompt, webpage_data, subject, default_url, default_name, title_chain, linkedin_chain, authenticator)

            st.session_state.title = title
            st.session_state.linkedin = linkedin
            st.session_state.camera_picture = camera_picture
            st.session_state.upload_image = upload_image
            st.session_state.generated_image_data = generated_image_data
            st.session_state.subject = subject
            st.session_state.default_url = default_url
            st.session_state.default_name = default_name

            st.session_state.current_view = "results"
            st.experimental_rerun()

        # Handle user logout
        logout_option = user_logout(authenticator)

if st.session_state.current_view == "results":
    if st.session_state.current_view == "results":
        display_final_result(name, st.session_state.title, st.session_state.linkedin, st.session_state.camera_picture, st.session_state.upload_image, st.session_state.generated_image_data, st.session_state.title_chain, st.session_state.linkedin_chain, st.session_state.prompt, st.session_state.webpage_data, st.session_state.subject, st.session_state.default_url, st.session_state.default_name, authenticator)
