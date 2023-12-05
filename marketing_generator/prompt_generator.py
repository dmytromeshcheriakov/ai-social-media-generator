import streamlit as st
from langchain.prompts import PromptTemplate


def generate_prompts():
    """
    Generate prompts for creating social media content.
    
    Function provides a interface for selecting type of content, tonality, and the option for AI generated pictures.
    Based on the selection, the respective template is used for text or (if choosen) AI image generation
    """

    # User selects the type of content (e.g.: "Neue Öffnungszeiten")
    subject = st.radio(
            "What type of post would you like to generate?",
            ('Service Offer', 'Employee Spotlight', 'Event', 'Announcement'),
            horizontal=True
    )

    # User selects the tonality of the content (e.g.: "Informativ")
    tonality = st.radio(
        "How should the post be written?",
        ('Business informational', 'Catchy question', 'Tech deep dive', 'Engaging insights'),
        # ('Informativ', 'Begeisternd'), # 'Tech deep dive' , 'Interessant'
        horizontal=True
    )



    # Use the respective templates based on the selected tonality
    if tonality == 'Business informational':
        title_template = PromptTemplate(
        input_variables = ['topic', 'webpage_data', 'subject'],
        template= """Act as a professional and experienced consultant with 20 years of experience
        in social media copywriting. Avoid exaggerated and to euphoric tone, don’t try to sell 
        a solution. Compose a title for {subject} on the topic: {topic}. The goal is to grab the readers’ attention. It must
        not create the impression of a click bait. The audience we are addressing has a 
        business background and no in-depth technical knowledge.  
        This is the content from website: {webpage_data}"""
        )

        linkedin_template = PromptTemplate(
        input_variables = ['topic', 'webpage_data', 'subject', 'default_url', 'default_name'],
        template = """
        Act as a professional and experienced consultant with 20 years of experience in social media copywriting.

        - **Post Type**: Informational for {subject}.
        - **Tone**: Professional and neutral. Avoid exaggeration and overly enthusiastic language, don’t try to sell 
        a solution
        - **Topic**: Write a text for {subject} about: {topic}.
        - **Length**: The post should not exceed 255 characters.
        - **Call-to-Action**: Always include a direct call to action to '{default_url}'.
        - **Brackets**: Never use any brackets, always include the name '{default_name}' or the '{default_url}'.
        - **Emojis**: Write only plain text. Do not use any emojis, icons, or symbols.
        - **Goal**: The post should capture readers' attention, encouraging them to get more information.
        - **Audience**: The audience we are addressing has a business background and no in-depth technical knowledge.
        - **Context**: If relevant, incorporate the following content: {webpage_data}.
        """
    )
    elif tonality == 'Catchy question':
        title_template = PromptTemplate(
        input_variables = ['topic', 'webpage_data', 'subject'],
        template="""Develop an engaging title for the subject: {subject}, informed by insights on the topic: {topic}. 
        The objective is to capture the interest of potential clients through social media, ensuring authenticity and avoiding clickbait. 
        Tailor this to the audience interested in our corporate services, incorporating context from: {webpage_data}."""
        )

        linkedin_template = PromptTemplate(
        input_variables = ['topic', 'webpage_data', 'subject', 'default_url', 'default_name'],
        template = """
        Act as a professional and experienced consultant with 20 years of experience in social media copywriting. 

        - **Post Type**: Catchy question for {subject}.
        - **Tone**: Catchy and engaging.
        - **Topic**: Formulate a general question for {subject} about {topic} that the text is giving an answer to without mentioning the 
        concrete details such as the name of the client or the involved Reply company.
        - **Length**: The post should not exceed 255 characters.
        - **Call-to-Action**: Always include a direct call to action to '{default_url}'.
        - **Brackets**: Never use any brackets, always include the name '{default_name}' or the '{default_url}'.
        - **Emojis**: Write only plain text. Do not use any emojis, icons, or symbols.
        - **Goal**: The post should capture readers' attention, encouraging them to get more information.
        - **Audience**: The audience we are addressing has a business background and no in-depth technical knowledge.
        - **Context**: If relevant, incorporate the following content: {webpage_data}.
        """
    )
    elif tonality == 'Tech deep dive':
        title_template = PromptTemplate(
        input_variables = ['topic', 'webpage_data', 'subject'],
        template="""Act as a professional and experienced consultant with 20 years of experience
        in social media copywriting. Avoid exaggerated and to euphoric tone, don’t try to sell 
        a solution. Compose a title for {subject} on the topic: {topic}. The goal is to grab the readers’ attention. It must
        not create the impression of a click bait. The audience we are addressing has a business
        background and some in-depth technical knowledge.
        This is the content from website: {webpage_data}"""
        )
        
        linkedin_template = PromptTemplate(
        input_variables = ['topic', 'webpage_data', 'subject', 'default_url', 'default_name'],
        template = """
        Act as a professional and experienced consultant with 20 years of experience in social media copywriting. 

        - **Post Type**: Tech deep dive {subject}.
        - **Tone**: Engaging and insightful. Write the Text in a way it is relatable for representant from the same or
        similar industry.
        - **Topic**: The Text should address a generalized pain point of the {topic} that the solution or project or 
        informational material is addressing.
        - **Length**: The post should not exceed 255 characters.
        - **Call-to-Action**: Always include a direct call to action to '{default_url}'.
        - **Brackets**: Never use any brackets, always include the name '{default_name}' or the '{default_url}' of the restaurant.
        - **Emojis/Symbols**: Write only plain text. Do not use any emojis, icons, or symbols.
        - **Goal**: The copy should grab the readers’ attention and make them click on the call-to-action link, without appearing as clickbait.
        - **Audience**: The audience we are addressing has a business background and some in-depth technical knowledge.
        - **Context**: If relevant, incorporate the following content: {webpage_data}.
        """
        )
        
    elif tonality == 'Engaging insights':
        title_template = PromptTemplate(
        input_variables = ['topic', 'webpage_data', 'subject'],
        template="""Act as a professional and experienced consultant with 20 years of experience
        in social media copywriting. Avoid exaggerated and to euphoric tone, don’t try to sell 
        a solution. Compose a title for {subject} on the topic: {topic}. The goal is to grab the readers’ attention. It must
        not create the impression of a click bait. The audience we are addressing has a business
        background and no in-depth technical knowledge.
        This is the content from website: {webpage_data}"""
        )
        
        linkedin_template = PromptTemplate(
        input_variables = ['topic', 'webpage_data', 'subject', 'default_url', 'default_name'],
        template = """
        Act as a professional and experienced consultant with 20 years of experience in social media copywriting. 

        - **Post Type**: Engaging insights for {subject}.
        - **Tone**: Engaging and insightful.
        - **Topic**: The first paragraph should contain already the most important information and motivates to read on. Emphasize information for {subject} on the topic: {topic}.
        - **Length**: Format the text so that the first paragraph is not longer than 240 characters and leave an empty line after the first paragraph.
        - **Call-to-Action**: Always include a direct call to action to '{default_url}'.
        - **Brackets**: Never use any brackets, always include the name '{default_name}' or the '{default_url}' of the restaurant.
        - **Emojis/Symbols**: Write only plain text. Do not use any emojis, icons, or symbols.
        - **Goal**: The copy should grab the readers’ attention and make them click on the call-to-action link, without appearing as clickbait.
        - **Audience**: The audience we are addressing has a business background and no in-depth technical knowledge.
        - **Context**: If relevant, incorporate the following content: {webpage_data}.
        """
    )

    # Use the image template, if 'generatepicture' checkbox was choosen
    imgdescription_template = PromptTemplate(
        input_variables=['linkedin'],
        template=
        """        
        **Task**: Craft a 100-character DALL-E prompt.
        **Prompt**: Write the prompt for a photorealistic high quality image displaying {linkedin}.
        **Style**: simple and elegant photorealistic image, best quality, official art, accurate proportions and minimal clutter, no text, no watermark, no signature, no names.
        **Note**: Always consider the "Style" in the 100-character DALL-E prompt
        """


        # Add drawing as a specific command
    )
    
    return tonality, subject, title_template, linkedin_template, imgdescription_template