import streamlit as st
import pandas as pd
import requests

# Load data from Google Sheets (published as CSV)
@st.cache_data(ttl=600)
def load_trainer_data():
    sheet_url = st.secrets["google_sheets"]["sheet_url"]
    df = pd.read_csv(sheet_url)
    df.fillna("", inplace=True)
    return df

def find_matches(df, skills, location):
    matched_trainers = []
    for _, row in df.iterrows():
        trainer_skills = [s.strip().lower() for s in row["Skills Taught"].split(",")]
        trainer_location = row["City"].strip().lower()
        if any(skill in trainer_skills for skill in skills) and location in trainer_location:
            matched_trainers.append({
                "name": f"{row['First Name']} {row['Last Name']}",
                "city": row["City"],
                "skills": row["Skills Taught"],
                "membership": row.get("Membership Type", ""),
                "linkedin": row.get("LinkedIn Profile URL", ""),
                "bio": row.get("Short Bio", ""),
                "pic": row.get("Profile Picture Upload", "")
            })
    return matched_trainers

# UI
st.set_page_config(page_title="Trainer Recommender", layout="centered")
st.title("🎯 Trainer Recommender")

skills_input = st.text_input("Enter skills you're looking for (comma-separated):")
location_input = st.text_input("Enter your location:")

if st.button("Find Trainers"):
    user_skills = [s.strip().lower() for s in skills_input.split(",") if s.strip()]
    user_location = location_input.strip().lower()
    if user_skills and user_location:
        with st.spinner("Matching trainers..."):
            df = load_trainer_data()
            matches = find_matches(df, user_skills, user_location)

        if matches:
            st.success(f"Found {len(matches)} matching trainer(s).")
            for trainer in matches:
                st.subheader(trainer["name"])
                st.text(f"City: {trainer['city']}")
                st.text(f"Skills: {trainer['skills']}")
                st.text(f"Membership: {trainer['membership']}")
                st.markdown(f"[LinkedIn]({trainer['linkedin']})")
                st.text(trainer["bio"])
                if trainer["pic"]:
                    st.image(trainer["pic"], width=100)
                st.markdown("---")
        else:
            st.warning("No matching trainers found.")
    else:
        st.warning("Please enter both skills and location.")
