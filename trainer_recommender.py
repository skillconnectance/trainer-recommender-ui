import streamlit as st
import pandas as pd
from pytrends.request import TrendReq
from PIL import Image
import time
import random

# --- Config ---
st.set_page_config(page_title="SkillConnectance", layout="wide")
st.title("SkillConnectance: 💡 Learn Smarter")

# GCC Countries list for location restriction
GCC_COUNTRIES = [
    "Bahrain", "Kuwait", "Oman", "Qatar", "Saudi Arabia", "United Arab Emirates"
]

# Default trending skills
TRENDING_SKILLS = ["AI", "Python", "Marketing", "Data Science", "Machine Learning", "Blockchain", "Digital Marketing"]

# --- Load trainer data from Google Sheets ---
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT-Ar35mOmUWVi7sxlukLJLKtJ3WhtSx_dgEeB4GbNbOUAeTNKO0roiwUreM3sXFTnhlbRGM14yMqEP/pub?output=csv"
try:
    df = pd.read_csv(CSV_URL)
    df["Skills Taught"] = df["Skills Taught"].fillna("").apply(lambda x: [s.strip().lower() for s in x.split(",")])
    df["City"] = df["City"].fillna("").str.lower()
except Exception as e:
    st.error(f"Error loading trainer data: {e}")
    st.stop()

# --- Caching for Google Trends ---
@st.cache_data(show_spinner=False, ttl=3600)  # Cache for 1 hour
def fetch_trend_data(skill, region, timeframe):
    pytrends = TrendReq()
    retries = 3
    for i in range(retries):
        try:
            pytrends.build_payload([skill], timeframe=timeframe, geo=region.upper() if region else '')
            trend_data = pytrends.interest_over_time()
            return trend_data
        except Exception as e:
            if "429" in str(e):  # Handling rate limit errors
                wait_time = random.randint(30, 60)  # Random backoff time between 30-60 seconds
                st.warning(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise e  # Raise the exception if it's not a rate limit issue
    st.error("Unable to fetch trends after multiple attempts. Please try again later.")
    return pd.DataFrame()

# --- User Input for Skills and Location ---
skills_input = st.text_input("🧠 Enter skills you're looking for (comma-separated):", key="skills_input")
location_input = st.selectbox("📍 Select your location:", options=GCC_COUNTRIES, index=0)

# Timeframe toggle (last 12 months or last 30 days)
timeframe_option = st.radio("📅 Select trend period:", options=["Last 12 months", "Last 30 days"], index=0)

# --- Recommender and Radar Display ---
if st.button("Find Trainers & View Skill Trends"):
    user_skills = [skill.strip().lower() for skill in skills_input.split(",") if skill.strip()]
    user_location = location_input.strip().lower()

    if not user_skills:
        st.warning("Please enter at least one skill.")
    else:
        # --- Trainer Recommender ---
        matches = df[df["Skills Taught"].apply(lambda skills: any(skill in skills for skill in user_skills))]
        if user_location:
            matches = matches[matches["City"].str.contains(user_location)]

        if not matches.empty:
            st.success(f"✅ Found {len(matches)} matching trainer(s):")
            for _, row in matches.iterrows():
                col1, col2 = st.columns([1, 3])
                with col1:
                    img = row['Profile Picture Upload'] if isinstance(row['Profile Picture Upload'], str) and row['Profile Picture Upload'].startswith("http") else "https://via.placeholder.com/120"
                    st.image(img, width=120)
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

        # --- Skill Demand Radar ---
        radar_skill = st.selectbox("📈 Select a trending skill for demand radar:", options=TRENDING_SKILLS)
        
        # Map timeframe to Google Trends format
        timeframe = 'today 12-m' if timeframe_option == "Last 12 months" else 'today 30-d'

        with st.spinner("Fetching Google Trends data..."):
            trend_df = fetch_trend_data(radar_skill, user_location, timeframe)
            if not trend_df.empty:
                st.success(f"Showing trends for **{radar_skill}** in {user_location.capitalize()}")
                st.line_chart(trend_df[radar_skill])
                st.caption(f"📅 Data from {timeframe_option} via Google Trends")
            else:
                st.info("No trend data found for this skill.")
