import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO
import requests

# Skill to category mapping (you can expand this as needed)
skill_to_category = {
    "python": "Programming",
    "excel": "Programming",
    "java": "Programming",
    "soft skills": "Soft Skills",
    "communication": "Soft Skills",
    "leadership": "Soft Skills",
    "data analysis": "Data Science",
    "machine learning": "Data Science",
    "marketing": "Marketing",
    "sales": "Sales"
    # Add more skill-category mappings here...
}

st.set_page_config(page_title="Trainer Recommender", layout="wide")
st.title("🔍 Trainer Recommender")

# Load data from Google Sheet (public CSV URL)
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT-Ar35mOmUWVi7sxlukLJLKtJ3WhtSx_dgEeB4GbNbOUAeTNKO0roiwUreM3sXFTnhlbRGM14yMqEP/pub?output=csv"
try:
    df = pd.read_csv(CSV_URL)
except Exception as e:
    st.error(f"Error loading trainer data: {e}")
    st.stop()

# Preprocess the data (Skills taught)
df["Skills Taught"] = df["Skills Taught"].fillna("").apply(lambda x: [s.strip().lower() for s in x.split(",")])

# User input
skills_input = st.text_input("🧠 Enter skills you're looking for (comma-separated):")
location_input = st.text_input("📍 Enter your location:")

if st.button("Find Trainers"):
    user_skills = [skill.strip().lower() for skill in skills_input.split(",") if skill.strip()]
    user_location = location_input.strip().lower()

    if not user_skills:
        st.warning("Please enter at least one skill.")
    else:
        # Match logic
        # Get trainers who match any of the user skills
        matches = df[df["Skills Taught"].apply(lambda skills: any(skill in skills for skill in user_skills))]

        # If a location is provided, filter trainers by city
        if user_location:
            matches = matches[matches["City"].str.contains(user_location)]

        if not matches.empty:
            st.success(f"✅ Found {len(matches)} matching trainer(s):")
            for _, row in matches.iterrows():
                # Layout in two columns
