import streamlit as st
import os
from streamlit_option_menu import option_menu
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

##################################################################

#upload = "Client_folder"
#upload1 ="Poc_folder"
#upload2 ="CS_Goals_folder"

#def file_exists(filename):
   # return os.path.exists(os.path.join(upload, filename))
#def file_exists1(filename):
   # return os.path.exists(os.path.join(upload1, filename))
#def file_exists2(filename):
   # return os.path.exists(os.path.join(upload2, filename))

# Google Drive API Setup
SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = "service_account.json"  # Your JSON file
PARENT_FOLDER_ID = "1N36EC-B3dN7wx3wUYC732os1S6RzjwHh"
PARENT_FOLDER_ID1 ="1N4GgBTduwK0JsB9ERGD8DYyPHmTyBRpQ"
PARENT_FOLDER_ID2 ="1N5uQq9XJH_M9Tsee8Z6bgRy3eNhGncal"

 
def authenticate():
    """Authenticate with Google Drive API."""
    service_account_json = st.secrets["GOOGLE_SERVICE_ACCOUNT"]
    service_account_info = json.loads(service_account_json)
    creds = service_account.Credentials.from_service_account_info(service_account_info)
    #creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build("drive", "v3", credentials=creds)
 
def file_exists(file_name,drive_service,PARENT_FOLDER):
    """Check if a file already exists in Google Drive folder."""
    
    query = f"name='{file_name}' and '{PARENT_FOLDER}' in parents"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    return len(results.get("files", [])) > 0  # Return True if file exists

def upload_file(file,drive_service,PARENT_FOLDER):
    """Upload file to Google Drive if it does not already exist."""
    #drive_service = authenticate()
    file_name=file.name
    if file_exists(file.name,drive_service,PARENT_FOLDER):
        return False, f"⚠️ File '{file.name}' already exists. Please rename and try again."
    
    temp_file_path=os.path.join("client_temp",file_name)
    os.makedirs("client_temp",exist_ok=True)
    # Upload the file
    file_metadata = {"name": file.name, "parents": [PARENT_FOLDER]}
    # Save the file temporarily
    #temp_path = f"./{file.name}"
    with open(temp_file_path, "wb") as f:
        f.write(file.getbuffer())
 

    media = MediaFileUpload(temp_file_path, mimetype="application/pdf")
    uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    
    #os.remove(temp_file_path)  # Delete temporary file after upload
    return True, f"File '{file.name}' uploaded successfully!"    # (ID: {uploaded_file.get('id')})"



def show_upload_file():
    #st.title("Upload File Page")
 
    col1, col2 = st.columns([14, 2])
    with col1:
        if st.button("🏠 Home"):
            st.session_state.page = "search"
            st.rerun()
    with col2:
        if st.button(":blue[Logout]"):
            st.session_state.logged_in = False
            st.session_state.page = "login"
            st.rerun()
    

        
    hide="""
        <style>
        #MainManu {visibility:hidden;}
        footer {visibility:hidden;}
        header {visibility:hidden;}
        </style>
    """
    st.markdown(hide,unsafe_allow_html=True)
    st.header("Select Directory")
    

    selected=option_menu(menu_title=None,options=["CS Goals Folder","CLIENT FOLDER","POC FOLDER"],icons=["","bi bi-folder","bi bi-folder"],orientation="horizontal",)

    l=["admin"]
    try:
        if selected == "CLIENT FOLDER" and st.session_state.username in l:
            #File uploaded into uploaded_file folder
            #st.header("Upload Files to Google Drive")
            drive_service = authenticate()
            uploaded_file = st.file_uploader("Choose a file",accept_multiple_files=True, type=["pdf"])  
 
            if uploaded_file:
                for file in uploaded_file:
                    success, message = upload_file(file,drive_service,PARENT_FOLDER_ID)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
            
            '''
            uploaded_file = st.file_uploader("Upload PDF", type='pdf')
            if uploaded_file:
                file_path = os.path.join(upload, uploaded_file.name)
                    # Check if the file already exists
                if file_exists(uploaded_file.name):
                    st.error(f"A file with the name '{uploaded_file.name}' already exists. Please rename the file before uploading.")
                else:
                    # Save the file
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                            #st.session_state["uploaded_file"]=uploaded_file
                    st.success(f"File uploaded successfully: {uploaded_file.name}")
            
                '''  

        elif selected == "POC FOLDER":
            drive_service = authenticate()
            uploaded_file = st.file_uploader("Choose a file",accept_multiple_files=True, type=["pdf"])  
 
            if uploaded_file:
                for file in uploaded_file:
                    success, message = upload_file(file,drive_service,PARENT_FOLDER_ID1)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
            
            #File uploaded into uploaded_file folder
            ''' uploaded_file = st.file_uploader("Upload PDF", type='pdf')
            if uploaded_file:
                file_path = os.path.join(upload1, uploaded_file.name)
                    # Check if the file already exists
                if file_exists1(uploaded_file.name):
                    st.error(f"A file with the name '{uploaded_file.name}' already exists. Please rename the file before uploading.")
                else:
                    # Save the file
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                            #st.session_state["uploaded_file"]=uploaded_file
                    st.success(f"File uploaded successfully: {uploaded_file.name}")
            '''

        elif selected == "CS Goals Folder":
            drive_service = authenticate()
            uploaded_file = st.file_uploader("Choose a file",accept_multiple_files=True, type=["pdf"])  
 
            if uploaded_file:
                for file in uploaded_file:
                    success, message = upload_file(file,drive_service,PARENT_FOLDER_ID2)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
            #File uploaded into uploaded_file folder
            '''uploaded_file = st.file_uploader("Upload PDF", type='pdf')
            if uploaded_file:
                file_path = os.path.join(upload2, uploaded_file.name)
                    # Check if the file already exists
                if file_exists2(uploaded_file.name):
                    st.error(f"A file with the name '{uploaded_file.name}' already exists. Please rename the file before uploading.")
                else:
                    # Save the file
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                            #st.session_state["uploaded_file"]=uploaded_file
                    st.success(f"File uploaded successfully: {uploaded_file.name}")
            '''

        else:
            st.error("Unauthorized User")
        
    except Exception as e:
        st.error(f" Error! Select an Folder: {e}")





    
   