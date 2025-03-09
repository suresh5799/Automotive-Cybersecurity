import streamlit as st
import base64
import time


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.failed_attempts = 0
    st.session_state.lockout_time = None


lock_out_time = 10  # Lockout duration in seconds
 
# Check if the user is in lockout period
def is_locked_out():
    if st.session_state.lockout_time:
        elapsed_time = time.time() - st.session_state.lockout_time
        remaining_time = lock_out_time - int(elapsed_time)
 
        if remaining_time > 0:
            return True, remaining_time  # User is still locked out
        else:
            # Reset lockout after time is over
            st.session_state.lockout_time = None
            st.session_state.failed_attempts = 0
            return False, 0  # Allow login again
    return False, 0

if "username" not in st.session_state:
    st.session_state.username=""

# Simulated login credentials
# Predefined credentials   
#st.select_slider.ENGINEERS=ENGINEERS

ENGINEERS = {"40037840":"40037840","40037842":"40037842","40037797":"40037797","40035022":"40035022","admin":"admin"}
ADMINS = {"admin": "admin"}


# Function to set background image from local folder
def set_background():
    image_path = "new_drive/images/auti1.jpg"
    with open(image_path, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()
    page_bg = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_string}");
        background-size: cover;
        #background-position: center;
        #background-attachment: fixed;
        #background-repeat:no-repeat;
        
    }}
    .login-container{{
        display:flex;
        justify-content:center;
        align-items:center;
        height:100vh;
        text-align:center;

    }}
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)


def show_login():
    
    set_background()
    st.header("🔐 :blue[Login Page]")
    locked, remaining_time = is_locked_out()
    if locked:
        st.warning(f"**Too many failed attempts! Please try again in {remaining_time} seconds.**")
        time.sleep(1)  # Wait 1 second before re-running the app
        st.rerun()  # Refresh the app to update countdown
        return  # Stop execution of login form

    #st.markdown('<div class="login-container">', unsafe_allow_html=True)
 
    #st.markdown("<h1 style='text-align: center;'>Login Page</h1>", unsafe_allow_html=True)
 
    username = st.text_input("",placeholder="Username ")
    password = st.text_input("",placeholder="Password", type="password")
    role=st.selectbox("",["Select Role","Engineer","Architect"])
    input_style="""
    <style>
    input[type="text"]{
        background-color:transparent;
        color:#a19eae;

    }
    div[data-baseweb="base-input"]{
        background-color:transparent !important;
    }
    div[data-testid="stAppViewContainer"]{
        background-color:transparent !important;
    }
    </style>
    """
    if st.button("Login",type="primary"):
            c=0
            if role == "Engineer" and username in ENGINEERS and ENGINEERS[username] == password:
                st.session_state.logged_in = True
                st.session_state.role = "Engineer"
                st.session_state.username = username
                
                st.session_state.failed_attempts = 0  # Reset failed attempts on success
                
                st.success("Login Successful! Redirecting...")
                st.session_state.page = "search"
                st.rerun()
            elif role == "Architect" and username in ADMINS and ADMINS[username] == password:
                st.session_state.logged_in = True
                st.session_state.role = "Architect"
                st.session_state.page = "search"
                st.session_state.username = username
                
                st.session_state.failed_attempts = 0  # Reset failed attempts on success
                st.success("Login Successful! Redirecting...")
                st.rerun()
            else:
                st.session_state.failed_attempts += 1
                st.warning(f"**Invalid username, password, or role selection! Attempt {st.session_state.failed_attempts}/3**")
 
                if st.session_state.failed_attempts >= 3:
                    st.session_state.lockout_time = time.time()  # Store lockout start time
                    #st.warning("**Too many failed attempts! Login disabled for 10 seconds.**")
                    st.rerun()
               
    
    st.markdown('</div>', unsafe_allow_html=True)






'''
 
    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.session_state.role = role
            st.session_state.page = "search"
            st.rerun()  # Refresh to switch pages
        else:
            st.error("Enter valid credentials")
'''
