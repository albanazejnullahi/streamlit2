import streamlit as st
import pandas as pd
import os

def feedback_page():
    st.title('Feedback Records')
    feedback_file = 'feedback.csv'
    feedback_password = "London123"  

    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'show_confirm' not in st.session_state:
        st.session_state.show_confirm = False

    if not st.session_state.authenticated:
        password = st.text_input("Enter password to view feedback records", type="password")
        if password == feedback_password:
            st.session_state.authenticated = True
            st.experimental_rerun()  # Ensure the rerun only happens here, if needed
        elif password:
            st.error("Incorrect password.")
    else:
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.experimental_rerun()  # Ensure the rerun only happens here, if needed

        if os.path.exists(feedback_file):
            feedback_df = pd.read_csv(feedback_file)
            st.dataframe(feedback_df)

            if st.button("Delete all feedback records"):
                st.session_state.show_confirm = True

            if st.session_state.show_confirm:
                st.warning("Are you sure you want to delete all feedback records?")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Yes"):
                        os.remove(feedback_file)
                        st.success("All feedback records have been deleted.")
                        st.session_state.show_confirm = False
                        # Refresh the page to update the state
                        st.experimental_rerun()
                with col2:
                    if st.button("No"):
                        st.session_state.show_confirm = False
                        # Refresh the page to update the state
                        st.experimental_rerun()

        else:
            st.info("No feedback records found.")

if __name__ == "__main__":
    feedback_page()
