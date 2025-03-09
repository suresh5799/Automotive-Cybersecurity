import streamlit as st
import login
import search
import upload_file
import delete_file
import list_of_files
#import old
 

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0

if "lockout_time" not in st.session_state:
    st.session_state.lockout_time = None    

if "page" not in st.session_state:
    st.session_state.page = "login"
 
# Page Navigation Logic
#if st.session_state.page == "login":
if  st.session_state.page=="login":
    login.show_login()
elif st.session_state.page == "search" :
    search.show_search()
elif st.session_state.page == "upload_file":
    upload_file.show_upload_file()
#elif st.session_state.page == "old" :
    #old.show_old()
elif st.session_state.page == "delete_file" and st.session_state.role=="Architect":
    delete_file.show_delete_file()
#elif st.session_state.page == "list_of_files" and st.session_state.role=="Admin":
elif st.session_state.page == "list_of_files":   
    list_of_files.show_list_of_files()


else:
    st.session_state.page = "login"
    st.rerun()
