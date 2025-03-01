import streamlit as st
import google.generativeai as genai 
#VERIFICATION CODE STARTS
import hmac

def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False


if not check_password():
    st.stop()
#VERIFICATION CODE ENDS

st.title('Vacation planner using Gen AI')


genai.configure(api_key=st.secrets['API_KEY']['api_key']) #API KEY
model = genai.GenerativeModel("gemini-2.0-flash") #MODEL NAME AND VERSION

budget_data = st.text_input('Enter budget in dollars')
dest_data = st.text_input('Enter destination city')
days_data = st.text_input('Enter number of days')
group_data = st.text_input('Enter group size')
contraints_data = st.text_input('Enter special contraints (food, young or old, hotel type, room type)')

response = model.generate_content(f"""Create a vacation plan based on budget = {budget_data},
                                   destination is {dest_data} for number of days {days_data}
                                  group size {group_data} and consider contraints
                                  {contraints_data}""")
st.write(response.text)