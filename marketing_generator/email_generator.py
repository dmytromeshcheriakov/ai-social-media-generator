# import pickle
# import os
# import base64 
# import json

# from io import BytesIO
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.image import MIMEImage
# from googleapiclient.errors import HttpError
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from google.auth.exceptions import RefreshError
# from googleapiclient.discovery import build


# def gmail_authenticate():
#     """Load / refresh Gmail API credentials."""
    
#     SCOPES = ['https://mail.google.com/']
#     creds = None

#     # if token.pickle is available load credentials
#     if os.path.exists("token.pickle"):
#         with open("token.pickle", "rb") as token:
#             creds = pickle.load(token)

#     try:
#         # if credentials are not valid
#         if not creds or not creds.valid:
#             # Refresh request
#             if creds and creds.expired and creds.refresh_token:
#                 creds.refresh(Request())
#             # Request new credentials
#             else:
#                 flow = InstalledAppFlow.from_client_secrets_file('./marketing_generator/credentials.json', SCOPES)
#                 creds = flow.run_local_server(port=0)
#                 with open("token.pickle", "wb") as token:
#                     pickle.dump(creds, token)
#     except RefreshError:
#         # Handle refresh error (e.g. token revoked or expired without possibility of refresh)
#         os.remove("token.pickle")  # remove the invalid token
#         return gmail_authenticate()  # recursive call to re-authenticate
    
#     return build('gmail', 'v1', credentials=creds)



# def create_image_attachment(image_data, filename='image.jpg'):
#     """Image for email attachment."""

#     img = MIMEImage(image_data)
#     img.add_header('Content-Disposition', 'attachment', filename=filename)
    
#     return img


# def load_customize():
#     with open('./marketing_generator/customize.json', 'r') as f:
#         return json.load(f)


# def send_email_with_attachment(service, name, title, linkedin, upload_image=None, generated_image_data=None, camera_picture=None):
#     """Send Email with an attachment containing an image"""

#     # Load the dictionary from the JSON file
#     login_customize_dict = load_customize()
#     # Accessing email based on the name
#     default_email = login_customize_dict.get(name, {}).get("Restaurant_Email", "")

#     message = MIMEMultipart()
#     message['To'] = 'm.pricken@reply.de, {}'.format(default_email) # m.afflerbach@reply.de, d.meshcheriakov@reply.de, d.hammer@reply.de'
#     message['From'] = 'mpricken.reply@gmail.com'
#     message['Subject'] = 'Beitrag HD Content Creator'

#     body_part = MIMEText(f"Name des Restaurant: \n {name} \n\n Titel des Beitrags: \n {title} \n\n Inhalt des Beitrag: \n {linkedin}", 'plain')
#     message.attach(body_part)

#     if upload_image:
#         byte_arr = BytesIO()
#         format_to_extension = {
#             'JPEG': 'jpg',
#             'PNG': 'png'
#         }
#         image_format = upload_image.format
#         filename = f'image.{format_to_extension.get(image_format, "jpg")}'
#         upload_image.save(byte_arr, format=image_format)
#         image_data = byte_arr.getvalue()

#         image_attachment = create_image_attachment(image_data, filename)
#         message.attach(image_attachment)

#     if camera_picture:
#         byte_arr = BytesIO()
#         camera_picture.save(byte_arr, format=camera_picture.format)
#         image_data = byte_arr.getvalue()

#         image_attachment = create_image_attachment(image_data, 'camera_image.jpg')
#         message.attach(image_attachment)

#     if generated_image_data:
#         image_attachment = create_image_attachment(generated_image_data, 'generated_image.jpg')
#         message.attach(image_attachment)

#     encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

#     create_message_body = {
#         'raw': encoded_message
#     }

#     try:
#         sent_message = (service.users().messages().send(userId="me", body=create_message_body).execute())
#         print(F'Message Id: {sent_message["id"]}')

#         return sent_message
    
#     except HttpError as error:
#         print(F'An error occurred: {error}')

#         return None