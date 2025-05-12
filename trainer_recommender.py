import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO
import requests

st.set_page_config(page_title="Trainer Recommender", layout="wide")
st.title("🔍 Trainer Recommender")

# Load data from Google Sheet (public CSV URL)
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT-Ar35mOmUWVi7sxlukLJLKtJ3WhtSx_dgEeB4GbNbOUAeTNKO0roiwUreM3sXFTnhlbRGM14yMqEP/pub?output=csv"
try:
    df = pd.read_csv(CSV_URL)
except Exception as e:
    st.error(f"Error loading trainer data: {e}")
    st.stop()

# Preprocess skill columns and add categories
df["Skills Taught"] = df["Skills Taught"].fillna("").apply(lambda x: [s.strip().lower() for s in x.split(",")])
df["Skill Categories"] = df["Skill Categories"].fillna("").apply(lambda x: [s.strip().lower() for s in x.split(",")])
df["City"] = df["City"].fillna("").str.lower()

# User input for skills and categories
skills_input = st.text_input("🧠 Enter skills you're looking for (comma-separated):")
categories_input = st.text_input("🔖 Enter categories you're interested in (comma-separated):")
location_input = st.text_input("📍 Enter your location:")

if st.button("Find Trainers"):
    user_skills = [skill.strip().lower() for skill in skills_input.split(",") if skill.strip()]
    user_categories = [category.strip().lower() for category in categories_input.split(",") if category.strip()]
    user_location = location_input.strip().lower()

    if not user_skills and not user_categories:
        st.warning("Please enter at least one skill or category.")
    else:
        # Match logic: Skills + Categories
        matches = df[df["Skills Taught"].apply(lambda skills: any(skill in skills for skill in user_skills)) | df["Skill Categories"].apply(lambda categories: any(category in categories for category in user_categories))]
        
        if user_location:
            matches = matches[matches["City"].str.contains(user_location)]

        if not matches.empty:
            st.success(f"✅ Found {len(matches)} matching trainer(s):")
            for _, row in matches.iterrows():
                # Layout in two columns
                col1, col2 = st.columns([1, 3])

                with col1:
                    if isinstance(row['Profile Picture Upload'], str) and row['Profile Picture Upload'].startswith("http"):
                        st.image(row['Profile Picture Upload'], width=120)
                    else:
                        st.image("https://via.placeholder.com/120", width=120)

                with col2:
                    st.markdown(f"### {row['First Name']} {row['Last Name']}")
                    st.markdown(f"📍 **City:** {row['City'].capitalize()}")
                    st.markdown(f"🛠️ **Skills:** {', '.join(row['Skills Taught'])}")
                    st.markdown(f"📅 **Experience:** {row['Years of Experience']} years")
                    st.markdown(f"📝 **Bio:** {row['Short Bio']}")
                    if pd.notna(row['LinkedIn Profile URL']):
                        st.markdown(f"[🔗 Connect on LinkedIn]({row['LinkedIn Profile URL']})", unsafe_allow_html=True)

                st.markdown("---")
        else:
            st.warning("⚠️ No matching trainers found.")
