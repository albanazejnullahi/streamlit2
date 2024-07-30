import streamlit as st
import pandas as pd
import re
import os

def main():
    st.title('AI Narratives')

    file_path = 'processed_properties.xlsx'
    feedback_file = 'feedback.csv'
    
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return
    
    # Ensure all columns are stripped of leading/trailing spaces
    df.columns = df.columns.str.strip()
    
    # Convert all relevant columns to string type
    df['Property Name'] = df['Property Name'].astype(str)
    df['Subject Data'] = df['Subject Data'].astype(str)
    df['Comps Data'] = df['Comps Data'].astype(str)
    df['Assessment'] = df['Assessment'].astype(str)
    
    unique_property_names = df['Property Name'].unique().tolist() if 'Property Name' in df.columns else []
    unique_property_names.insert(0, 'Select Property Name')

    with st.sidebar:
        st.subheader('Filters')
        selected_property_name = st.selectbox("Select Property Name", unique_property_names, key='property_dropdown', help="Select the Property Name")

    if selected_property_name != 'Select Property Name':
        # Filter by Property Name
        filtered_df = df[df['Property Name'] == selected_property_name]
        # Further filter to include only rows where Assessment is not empty
        filtered_df = filtered_df[filtered_df['Assessment'].str.strip().astype(bool)]

        # Limit to top 10 properties
        filtered_df = filtered_df.head(10)

        st.header("Filtered Data")

        if filtered_df.empty:
            st.warning("No data found with the selected criteria.")
        else:
            for index, row in filtered_df.iterrows():
                st.markdown(f"### Property Name: {row['Property Name']}")
                
                st.markdown("---")

                # Display Subject Data and Comps Data side by side
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"### Subject Data")
                    formatted_subject_data = format_text(row['Subject Data'], add_space=False)
                    st.markdown(formatted_subject_data, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"### Comps Data")
                    formatted_comps_data = format_text(row['Comps Data'], add_space=False)
                    st.markdown(formatted_comps_data, unsafe_allow_html=True)

                st.markdown("---")

                # Display Assessment
                st.markdown(f"### Assessment")
                formatted_assessment = format_text(row['Assessment'], add_space=True)
                st.markdown(formatted_assessment, unsafe_allow_html=True)

                st.markdown("---")
                
                # Feedback Form
                st.markdown("### Feedback")
                name = st.text_input("Your Name")
                info = f"Property Name: {row['Property Name']}"
                st.text_input("Info", value=info, disabled=True)
                feedback = st.text_area("Your Feedback")
                if st.button("Submit"):
                    save_feedback(name, info, feedback, feedback_file)
                    st.success(f"Thank you for your feedback, {name}!")

    else:
        st.info("Please select a Property Name to see filtered data.")

def format_text(text, add_space):
    text = re.sub(r'(^o )', r'* ', text, flags=re.MULTILINE)

    if add_space:
        # Add white space between paragraphs
        formatted_text = text.replace("\n", "<br><br>")
    else:
        formatted_text = text.replace("\n", "<br>")
    
    formatted_text = re.sub(r'\b(\w+italic\w+)\b', r'<i>\1</i>', formatted_text, flags=re.IGNORECASE)
    
    formatted_text = formatted_text.replace("$", "\$")
    
    return formatted_text

def save_feedback(name, info, feedback, feedback_file):
    # Create a DataFrame for the feedback
    feedback_data = pd.DataFrame({
        'Name': [name],
        'Info': [info],
        'Feedback': [feedback]
    })
    
    # Append feedback to the CSV file
    if not os.path.isfile(feedback_file):
        feedback_data.to_csv(feedback_file, index=False)
    else:
        feedback_data.to_csv(feedback_file, mode='a', header=False, index=False)

if __name__ == "__main__":
    main()
