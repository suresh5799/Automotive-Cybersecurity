import streamlit as st
import os
from streamlit_option_menu import option_menu
import streamlit as st
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
import time

 

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

# Get list of files in the upload folder
def list_pdfs(drive_service,PARENT_FOLDER):
    #drive_service = authenticate()
    results = drive_service.files().list(q=f"'{PARENT_FOLDER}' in parents and mimeType='application/pdf'",fields="files(id, name)").execute()
    return results.get("files", [])

def delete_pdf(file_id,drive_service):
    #drive_service = authenticate()
    drive_service.files().delete(fileId=file_id).execute()
    return True



def show_delete_file():
    #st.title("Delete a File")
 
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
    st.write("### Select Directory")

    

    selected=option_menu(menu_title=None,options=["CS Goals Folder","CLIENT FOLDER","POC FOLDER"],icons=["","bi bi-folder","bi bi-folder"],orientation="horizontal",)

    try:
        if selected == "CLIENT FOLDER":
          
            drive_service = authenticate()
            pdf_files = list_pdfs(drive_service,PARENT_FOLDER_ID)
            if pdf_files:
                pdf_names = [file["name"] for file in pdf_files]
                pdf_names.insert(0,"Select a file")
                selected_pdf = st.selectbox("", pdf_names,key="present_files")

                if st.button("Delete File"):
                    file_id = next(file["id"] for file in pdf_files if file["name"] == selected_pdf)
                    result=delete_pdf(file_id,drive_service)
                    if result:
                        st.success(f"File '{selected_pdf}' has been deleted.")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"File '{selected_pdf}' not found.")

            else:
                st.warning("No files uploaded yet. Please upload a file using Upload File Page")
        
        elif selected == "POC FOLDER":
            #st.write("### Available files")
            drive_service = authenticate()
            pdf_files = list_pdfs(drive_service,PARENT_FOLDER_ID1)
            if pdf_files:
                pdf_names = [file["name"] for file in pdf_files]
                pdf_names.insert(0,"Select a file")
                selected_pdf = st.selectbox("", pdf_names,key="present_files")

                if st.button("Delete File"):
                    file_id = next(file["id"] for file in pdf_files if file["name"] == selected_pdf)
                    result=delete_pdf(file_id,drive_service)
                    if result:
                        st.success(f"File '{selected_pdf}' has been deleted.")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"File '{selected_pdf}' not found.")

            else:
                st.warning("No files uploaded yet. Please upload a file using Upload File Page")

        elif selected == "CS Goals Folder":
            #st.write("### Available files")
            drive_service = authenticate()
            pdf_files = list_pdfs(drive_service,PARENT_FOLDER_ID2)
            if pdf_files:
                pdf_names = [file["name"] for file in pdf_files]
                pdf_names.insert(0,"Select a file")
                selected_pdf = st.selectbox("", pdf_names,key="present_files")

                if st.button("Delete File"):
                    file_id = next(file["id"] for file in pdf_files if file["name"] == selected_pdf)
                    result=delete_pdf(file_id,drive_service)
                    if result:
                        st.success(f"File '{selected_pdf}' has been deleted.")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"File '{selected_pdf}' not found.")
            else:
                st.warning("No files uploaded yet. Please upload a file using Upload File Page")

        else:
            st.error("Select Directory")


    except Exception as e:
            pass
######################################################