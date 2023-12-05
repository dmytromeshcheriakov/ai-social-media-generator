import streamlit as st
from streamlit_authenticator import Authenticate
import yaml
from yaml.loader import SafeLoader


def create_authenticator():
    """
    Create an authenticator for user login.
    
    Function reads the configuration from YAML file and initializes an authentication object with credentials and configurations.
    """

    # Load the the configuration from the yaml file
    with open('./marketing_generator/config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    # Create an authentication object using the loaded configuration
    authenticator = Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    return authenticator



def authenticate_and_login(authenticator):
    """
    Handle user login using the provided authenticator.
    
    Function renders a login module and checks the authentication status to provide feedback to the user.
    """
   
    # Render login modul (default location: main body of the page)
    name, authentication_status, username = authenticator.login('Log in', 'main')

    # Check the current authentication status in the session state
    if not st.session_state.get("authentication_status"):
        # If status is false the credentials were wrong
        if st.session_state.get("authentication_status") is False:
            st.error('Username and/or password are incorrect')
        else:
            # If not status is set -> Ask user to insert credentials
            st.warning('Please enter your username and password')
        
        return None, None, None

    return name, authentication_status, username



def user_logout(authenticator):
    """
    Handle user logout using the provided authenticator.
    
    Function renders a logout module so the user can end the session
    """

    # Render logout modul (default location: main body of the page)
    logout_option = authenticator.logout('Log out', 'main')

    return logout_option