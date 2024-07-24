import streamlit as st
import pandas as pd
import os

def feedback_page():
    st.title('Feedback Records')
    feedback_file = 'feedback.csv'
    feedback_password = "London123"  # Replace with your desired password

    password = st.text_input("Enter password to view feedback records", type="password")
    if password == feedback_password:
        if os.path.exists(feedback_file):
            feedback_df = pd.read_csv(feedback_file)
            st.dataframe(feedback_df)
            
            # Add a button to delete the feedback records
            if st.button("Delete all feedback records"):
                os.remove(feedback_file)
                st.success("All feedback records have been deleted.")
                st.experimental_rerun()
        else:
            st.info("No feedback records found.")
    elif password:
        st.error("Incorrect password.")

if __name__ == "__main__":
    feedback_page()
