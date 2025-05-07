import streamlit as st
import pandas as pd

st.set_page_config(page_title="Trainer Recommender", layout="wide")
st.title("🔍 Trainer Recommender")

# Load data from Google Sheets
@st.cache_data
def load_data():
    sheet_url = st.secrets["google_sheets"]["sheet_url"]
    return pd.read_csv(sheet_url)

df = load_data()

# Get user input
skills_input = st.text_input("Enter skills you're looking for (comma-separated):")
location_input = st.text_input("Enter your location:")

if st.button("Find Trainers"):
    user_skills = [s.strip().lower() for s in skills_input.split(",") if s.strip()]
    user_location = location_input.strip().lower()

    if not user_skills:
        st.warning("Please enter at least one skill.")
    else:
        # Filter logic
        matches = df[df["City"].str.lower().str.contains(user_location, na=False)]

        def has_skill(row):
            trainer_skills = str(row["Skills Taught"]).lower().split(",")
            return any(skill in [ts.strip() for ts in trainer_skills] for skill in user_skills)

        matches = matches[matches.apply(has_skill, axis=1)]

        if matches.empty:
            st.warning("No matching trainers found.")
        else:
            st.success(f"Found {len(matches)} matching trainer(s):")
            for _, row in matches.iterrows():
                st.subheader(f"{row['First Name']} {row['Last Name']}")
                st.text(f"City: {row['City']}")
                st.text(f"Skills: {row['Skills Taught']}")
                st.text(f"Experience: {row['Years of Experience']} years")
                st.text(f"Membership: {row.get('Membership Type', 'N/A')}")
                st.markdown(f"[LinkedIn Profile]({row.get('LinkedIn Profile URL', '#')})")
                st.text_area("Bio", row.get("Short Bio", "N/A"), height=100)
                if pd.notna(row.get("Profile Picture Upload", None)):
                    st.image(row["Profile Picture Upload"], width=100)
                st.markdown("---")
