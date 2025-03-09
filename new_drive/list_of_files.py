import streamlit as st
import os
from streamlit_option_menu import option_menu
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
 
#upload = "Client_folder"
#os.makedirs(upload, exist_ok=True)

#upload1 ="Poc_folder"
#os.makedirs(upload1, exist_ok=True)

#upload2 ="CS_Goals_folder"

SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = "service_account.json"
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

def list_pdfs(PARENT_FOLDER,drive_service):
    #drive_service = authenticate()
    results = drive_service.files().list(q=f"'{PARENT_FOLDER}' in parents and mimeType='application/pdf'",fields="files(id, name)").execute()
    return results.get("files", [])
 
def show_list_of_files():
    #st.title("List of Uploaded Files")
 
    col1, col2 = st.columns([14,2])
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
    st.write("### Select Directory")

    

    selected=option_menu(menu_title=None,options=["CS Goals Folder","CLIENT FOLDER","POC FOLDER"],icons=["","bi bi-folder","bi bi-folder"],orientation="horizontal",)
    l=["admin"]
    try:
        if selected == "CLIENT FOLDER":
            drive_service = authenticate()
            pdf_files = list_pdfs(PARENT_FOLDER_ID,drive_service)
            if pdf_files:
                st.write("### Available files:")
                for file in pdf_files:
                    st.write(file["name"])

            else:
                #st.error("The folder does not exist yet. Please upload a file using Fileuploader Page")
                st.warning("No files uploaded yet. Please upload a file using Fileuploader Page")
        
        elif selected == "POC FOLDER":
            #st.write("## Files in the Upload Folder")
            drive_service = authenticate()
            pdf_files = list_pdfs(PARENT_FOLDER_ID1,drive_service)
            if pdf_files:
                st.write("### Available files:")
                for file in pdf_files:
                    st.write(file["name"])

            else:
                #st.error("The folder does not exist yet. Please upload a file using Fileuploader Page")
                st.warning("No files uploaded yet. Please upload a file using Fileuploader Page")

        elif selected == "CS Goals Folder":
            #st.write("## Files in the Upload Folder")
            drive_service = authenticate()
            pdf_files = list_pdfs(PARENT_FOLDER_ID2,drive_service)
            if pdf_files:
                st.write("### Available files:")
                
                for file in pdf_files:
                    st.write(file["name"])

            else:
                #st.error("The folder does not exist yet. Please upload a file using Fileuploader Page")
                st.warning("No files uploaded yet. Please upload a file using Fileuploader Page")

        else:
            st.error("Unauthorized User")
        

    except Exception as e:
            pass

