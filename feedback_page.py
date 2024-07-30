import streamlit as st
import pandas as pd
import os

def feedback_page():
    st.title('Feedback Records')
    feedback_file = 'feedback.csv'
    feedback_password = "London123"

    # Initialize session state variables if they do not exist
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'show_confirm' not in st.session_state:
        st.session_state.show_confirm = False

    # Authentication logic using form
    if not st.session_state.authenticated:
        with st.form("login_form"):
            password = st.text_input("Enter password to view feedback records", type="password")
            login_button = st.form_submit_button("Login")
            
            if login_button:
                if password == feedback_password:
                    st.session_state.authenticated = True
                    st.session_state.show_confirm = False  # Reset any confirmation state
                    st.success("Logged in successfully.")
                else:
                    st.error("Incorrect password.")
    else:
        st.button("Logout", on_click=lambda: logout())

        # Display feedback records if authenticated and file exists
        if os.path.exists(feedback_file):
            feedback_df = pd.read_csv(feedback_file)
            st.dataframe(feedback_df)

            # Button to delete records
            if st.button("Delete all feedback records"):
                st.session_state.show_confirm = True

            # Show confirmation dialog if deletion is requested
            if st.session_state.show_confirm:
                st.warning("Are you sure you want to delete all feedback records?")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Yes"):
                        delete_records(feedback_file)
                with col2:
                    if st.button("No"):
                        st.session_state.show_confirm = False
        else:
            st.info("No feedback records found.")

def logout():
    st.session_state.authenticated = False
    st.info("Logged out successfully.")

def delete_records(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        st.success("All feedback records have been deleted.")
        st.session_state.show_confirm = False
        st.session_state.authenticated = False  # Optional: Logout after deletion

if __name__ == "__main__":
    feedback_page()
