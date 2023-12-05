
import streamlit_authenticator as stauth

# Function to hash passwords for each user - the hashed passwords then need to be copied to the config.yaml file.
# 'abc' and 'def' are just examples and should be replaced. It can also be just one password.

# Important: After generating the hashed password, the plaintext ones must be deleted.

# To run the code in a terminal on a mac: python3 password_generator/password_generator.py
# To run the code in a terminal on a windows: python password_generator/password_generator.py

hashed_passwords = stauth.Hasher(['abc', 'def']).generate()
print(hashed_passwords)