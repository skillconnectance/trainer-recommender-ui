import streamlit as st
import pandas as pd

st.title("Trainer Recommender")

# Load data from Google Sheet (public CSV URL)
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT-Ar35mOmUWVi7sxlukLJLKtJ3WhtSx_dgEeB4GbNbOUAeTNKO0roiwUreM3sXFTnhlbRGM14yMqEP/pub?output=csv"
try:
    df = pd.read_csv(CSV_URL)
except Exception as e:
    st.error(f"Error loading trainer data: {e}")
    st.stop()

# Preprocess skill column
df["Skills Taught"] = df["Skills Taught"].fillna("").apply(lambda x: [s.strip().lower() for s in x.split(",")])
df["City"] = df["City"].fillna("").str.lower()

# User input
skills_input = st.text_input("Enter skills you're looking for (comma-separated):")
location_input = st.text_input("Enter your location:")

if st.button("Find Trainers"):
    user_skills = [skill.strip().lower() for skill in skills_input.split(",") if skill.strip()]
    user_location = location_input.strip().lower()

    if not user_skills:
        st.warning("Please enter at least one skill.")
    else:
        # Match logic
        matches = df[df["Skills Taught"].apply(lambda skills: any(skill in skills for skill in user_skills))]
        if user_location:
            matches = matches[matches["City"].str.contains(user_location)]

        if not matches.empty:
            st.success(f"Found {len(matches)} matching trainer(s).")
            for _, row in matches.iterrows():
                st.subheader(f"{row['First Name']} {row['Last Name']}")
                st.text(f"City: {row['City']}")
                st.text(f"Skills: {', '.join(row['Skills Taught'])}")
                st.text(f"Experience: {row['Years of Experience']} years")
                st.text(f"Membership: {row['Membership Type']}")
                st.markdown(f"[LinkedIn]({row['LinkedIn Profile URL']})")
                st.text(f"Bio: {row['Short Bio']}")
                if isinstance(row['Profile Picture Upload'], str) and row['Profile Picture Upload'].startswith("http"):
                    st.image(row['Profile Picture Upload'], width=100)
                st.markdown("---")
        else:
            st.warning("No matching trainers found.")
