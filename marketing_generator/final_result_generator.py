import json
import io
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from marketing_generator.user_login_logout import user_logout
# from marketing_generator.llm_chain import email_attachments


def load_customize():
    """
    Load customization settings from JSON file.
    """
    with open('./marketing_generator/customize.json', 'r') as f:
        return json.load(f)


def display_final_result(name, title, linkedin, camera_picture, upload_image, generated_image_data, title_chain, linkedin_chain, prompt, webpage_data, subject, default_url, default_name, authenticator):
    """
    Display the final social media content, allow text regeneration, and handle email sending.

    Function displays title, text and image for the social media content with the option to change the text, 
    go back to the main menu or confrim the post and send it out as an email.
    """

    # Load the dictionary from the JSON file
    login_customize_dict = load_customize()

    # Initialize session state for title and linkedin if they don't exist
    if 'title_text' not in st.session_state:
        st.session_state.title_text = title
    if 'linkedin_text' not in st.session_state:
        st.session_state.linkedin_text = linkedin

    # Set default restaurant name based on the restaurant name from login credentials
    default_name = login_customize_dict.get(name, {}).get("Name", "")

    # Create the title for the final display of the post
    st.title(f'{default_name} Social Media Post')

    # Logic to get back to main menu
    # Create button to go back and create a new post
    if st.button("Back to the main menu"):
    # if st.button("Zurück zum Hauptmenü"):
        # Set session state variables view to the main menu and reset main 
        st.session_state.current_view = 'main'
        st.session_state.reset_main = True
        
        # Rerun the Streamlit app to reflect changes
        st.experimental_rerun()

    #Set session state for text an title
    st.write(st.session_state.title_text)
    st.write(st.session_state.linkedin_text)

    # Placeholder for more space between both text elements
    st.text("")
    st.text("")

    # Display text in bold
    new_title = '<p style="font-family:sans-serif; font-size: 16px; font-weight: bold;">If you like the text, simply copy it from this field:</p>'
    st.markdown(new_title, unsafe_allow_html=True)
    new_sub_title = '<p style="font-family:sans-serif; font-size: 16px; ">** Click in the field and then on the "Copy" symbol in the top right-hand corner</p>'
    st.markdown(new_sub_title, unsafe_allow_html=True)

    # Combine title and text to display in one code box
    combined_text = f"{st.session_state.title_text}\n\n{st.session_state.linkedin_text}"
    
    # Codebox displaying title and text -> With the Option to copy the content
    with stylable_container(
        "codeblock",
        """
        code {
            white-space: pre-wrap !important;
        }
        """,
    ):
        st.code(
            combined_text, language="HTML"
        )

    # Logic to change text
    # Create button to change the text
    if st.button("Generate new text"):
    # if st.button("Text neu generieren"):

        # If Text neu generieren button is clickes the chain for title and text run again
        new_title = title_chain.run(topic=prompt, webpage_data=webpage_data, subject=subject, default_name=default_name)
        new_linkedin = linkedin_chain.run(topic=prompt, webpage_data=webpage_data, subject=subject, default_url=default_url, default_name=default_name)
        
        # Update the session state with the new generated title and text
        st.session_state.title_text = new_title
        st.session_state.linkedin_text = new_linkedin

        title = new_title  # store updated title in local variable
        linkedin = new_linkedin  # store updated LinkedIn text in local variable
        
        # Rerun the Streamlit app to reflect changes
        st.experimental_rerun()
    

    # Display the images which are there
    if camera_picture:
        st.image(camera_picture)

        byte_arr = io.BytesIO()
        camera_picture.save(byte_arr, format="JPEG")
        image_data = byte_arr.getvalue()
        st.download_button(label="Download image", data=image_data, mime="image/jpg")

    if upload_image:
        st.image(upload_image)

        byte_arr = io.BytesIO()
        upload_image.save(byte_arr, format=upload_image.format)
        image_data = byte_arr.getvalue()
        mime_type = "image/png" if upload_image.format == "PNG" else "image/jpg"
        st.download_button(label="Download image", data=image_data, mime=mime_type, file_name="downloaded_image.jpg")

    
    if generated_image_data:
        st.image(generated_image_data)
        st.download_button(label="Download image", data=generated_image_data, mime="image/jpg")
    

    # # Logic to confirm post and trigger email sending
    # # If 'confirm_button' key not in session_state -> session_state is False
    # if 'confirm_button' not in st.session_state:
    #     st.session_state.confirm_button = False

    # # Create confirm button for sending email
    # confirm_button = st.button('Beitrag bestätigen und E-Mail versenden')

    # if confirm_button:
    #     # Change session state variable to True to indicate confirmation
    #     st.session_state.confirm_button = True

    #     # Call email attachments function 
    #     email_attachments(upload_image, camera_picture, generated_image_data, st.session_state.linkedin_text, st.session_state.title_text, name) 
    #     # If E-Mail got send -> Show confirmation
    #     st.success("E-Mail erfolgreich versendet!")

    # Handle user logout
    user_logout(authenticator)