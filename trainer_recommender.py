import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# Authenticate Google Sheets API using credentials.json
def authenticate_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    return client

# Fetch the latest data from Google Sheets
def get_sheet_data():
    client = authenticate_google_sheets()
    sheet = client.open("Trainer Sign Ups").sheet1  # Open the specific Google Sheet by name
    data = sheet.get_all_records()  # Gets all records as a list of dictionaries
    df = pd.DataFrame(data)
    return df

# Streamlit UI to take user input and find matching trainers
st.title("Trainer Recommender")

skills_input = st.text_input("Enter skills you're looking for (comma-separated):")
location_input = st.text_input("Enter your location:")

if st.button("Find Trainers"):
    # Get data from Google Sheets
    df = get_sheet_data()

    # Process user input
    user_skills = [skill.strip().lower() for skill in skills_input.split(",") if skill.strip()]
    user_location = location_input.strip().lower()

    if user_skills:
        # Filter trainers based on skills and location
        filtered_df = df[df['City'].str.lower() == user_location]
        filtered_df['Skills'] = filtered_df['Skills Taught'].apply(lambda x: [skill.strip().lower() for skill in x.split(",")])
        
        # Find trainers whose skills match the user's input
        matches = filtered_df[filtered_df['Skills'].apply(lambda x: any(skill in x for skill in user_skills))]

        if not matches.empty:
            st.success(f"Found {len(matches)} matching trainers!")
            for _, trainer in matches.iterrows():
                st.subheader(trainer["First Name"] + " " + trainer["Last Name"])
                st.text(f"City: {trainer['City']}")
                st.text(f"Skills: {trainer['Skills Taught']}")
                st.text(f"Membership: {trainer['Membership Type']}")
                st.markdown(f"[LinkedIn]({trainer['LinkedIn Profile URL']})")
                st.text(trainer["Short Bio"])
                if trainer["Profile Picture Upload"]:
                    st.image(trainer["Profile Picture Upload"], width=100)
                st.markdown("---")
        else:
            st.warning("No matching trainers found.")
    else:
        st.warning("Please enter at least one skill.")
