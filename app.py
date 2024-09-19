import streamlit as st
import os
from pathlib import Path

# Directory for storing containers (each user's data folder)
BASE_DIR = "user_containers"
Path(BASE_DIR).mkdir(parents=True, exist_ok=True)

# Function to get or create a container (directory) for a user based on the key
def get_user_container(user_key):
    user_container_path = os.path.join(BASE_DIR, user_key)
    Path(user_container_path).mkdir(parents=True, exist_ok=True)
    return user_container_path

# Function to validate user key
def validate_user_key(user_key):
    return os.path.exists(os.path.join(BASE_DIR, user_key))

# App title
st.title("Secure File Upload and Text Storage")

# User key input to create or access a container
user_key = st.text_input("Enter your secret key to access your container:", type="password")

if user_key:
    if validate_user_key(user_key):
        st.success("Access granted to your container.")
    else:
        st.warning("This is a new container. It will be created for you.")
        
    # Get or create the user's container
    user_container = get_user_container(user_key)
    
    # File upload section
    uploaded_file = st.file_uploader("Upload a file")
    if uploaded_file:
        file_path = os.path.join(user_container, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")
    
    # Text input area to store text
    st.write("### Store some text in your container")
    user_text = st.text_area("Enter your text here:")
    
    if st.button("Save Text"):
        text_file_path = os.path.join(user_container, "user_text.txt")
        with open(text_file_path, "w") as f:
            f.write(user_text)
        st.success("Your text has been saved successfully!")

    # Display stored files and text
    st.write("### Your uploaded files and saved text:")
    
    # List available files
    files = os.listdir(user_container)
    if files:
        for file in files:
            file_path = os.path.join(user_container, file)
            if file.endswith(".txt"):
                with open(file_path, "r") as f:
                    st.write(f"**{file}**: {f.read()}")
            else:
                with open(file_path, "rb") as f:
                    st.download_button(
                        label=f"Download {file}",
                        data=f,
                        file_name=file
                    )
    else:
        st.write("No files or text saved yet.")
else:
    st.info("Please enter your secret key to access or create your container.")
