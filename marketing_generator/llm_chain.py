import streamlit as st
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import WebBaseLoader
from langchain.memory import ConversationBufferMemory
from marketing_generator.image_generator import sd_generate_image
# from marketing_generator.email_generator import send_email_with_attachment, gmail_authenticate


def run_llm_chain(name, title_template, linkedin_template, imgdescription_template, prompt, webpage, subject, generatepicture, default_url, default_name):
    """
    Run the LLM chain to generate content and (if choosen) AI image.

    Function takes user inputs and generates social media content using a language model (LLM) chain. It can also generate images.
    """

    # Memory buffers for storing conversation history
    title_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
    linkedin_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
    imgdescription_memory = ConversationBufferMemory(input_key='linkedin', memory_key='chat_history')

    # !!! IMPORTANT: model_name needs to be changed back to GPT-4.0 !!!
    # Create OpenAI model instance
    llm = ChatOpenAI(model_name="gpt-4", temperature=0.9) # !!! Uncomment if App goes live !!!
    # llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.9) # !!! Only use for testing !!!

    # Create LLM chains for generating title, text and image descriptions
    title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, output_key='title', memory=title_memory)
    linkedin_chain = LLMChain(llm=llm, prompt=linkedin_template, verbose=True, output_key='script', memory=linkedin_memory)
    imgdescription_chain = LLMChain(llm=llm, prompt=imgdescription_template, verbose=True, output_key='imgdescription', memory=imgdescription_memory)
    
    # Chaining the components and displaying outputs
    if st.button("Generate Post"):
    # if st.button("Beitrag generieren"): 
        # Display loading element while generating the post 
        with st.spinner('Post is generated...'):
        # with st.spinner('Beitrag wird generiert...'):

            # Load website data
            loader = WebBaseLoader(webpage)
            webpage_data  = loader.load()

            # Generate title and text
            title = title_chain.run(topic=prompt, webpage_data=webpage_data, subject=subject, default_name=default_name)
            linkedin = linkedin_chain.run(topic=prompt, webpage_data=webpage_data, subject=subject, default_url=default_url, default_name=default_name)

            # Store content in session state -> Relevant if user deceides to generate a new title + text on the results overview page
            # 'st.session_state' allows for persisting and managing user data across reruns in a Streamlit (Documentation: https://docs.streamlit.io/library/api-reference/session-state)
            st.session_state.title_text = title
            st.session_state.linkedin_text = linkedin

            # If the checkbox to generate AI image was choosen (from promp_generator.py) -> call sd_generate_image function to generate the AI image
            if generatepicture:
                imgdescription = imgdescription_chain.run(linkedin=linkedin)
                generated_image_data = sd_generate_image(imgdescription)
            else:
                generated_image_data = None

            return name, title, linkedin, imgdescription_chain, generated_image_data, title_chain, linkedin_chain, prompt, webpage_data
    
    else: 
        None
    

# def email_attachments(upload_image, camera_picture, generated_image_data, linkedin, title, name):
#     """
#     Logic for preparing email attachments.
    
#     Function handles sending E-Mails with or without attachments.
#     """

#     # If the checkbox to generate an image was choosen, an image was uploaded or picture was taken -> attach a file
#     if generated_image_data or upload_image or camera_picture:
#         # If AI image was generated attach it to the email
#         if generated_image_data:
#             send_email(name, title, linkedin, generated_image_data=generated_image_data)

#         # If camera picture was taken attach it to the email
#         if camera_picture:
#             send_email(name, title, linkedin, camera_picture=camera_picture)
            
#         # If image was uploaded attach it to the email
#         if upload_image:
#             send_email(name, title, linkedin, upload_image=upload_image)

#     # Otherwise send just the text without an image as an attachment
#     else:
#         send_email(name, title, linkedin)


# def send_email(name, title, linkedin, generated_image_data=None, upload_image=None, camera_picture=None):
#     """
#     Authenticate and send the email with attachments or plain text.

#     Function handles gmail authentication and sends E-Mauls with or without attachments.
#     """
    
#     # Call gmail_authenticate and send_email_with_attachment functions
#     service = gmail_authenticate()
#     send_email_with_attachment(service, name, title, linkedin, generated_image_data=generated_image_data, upload_image=upload_image, camera_picture=camera_picture)