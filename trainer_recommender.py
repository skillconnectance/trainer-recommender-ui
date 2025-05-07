import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.title("🔍 Trainer Recommender")

# Input section
skills_input = st.text_input("Enter skills you're looking for (comma-separated):")
location_input = st.text_input("Enter your location:")

if st.button("Find Trainers"):
    user_skills = [skill.strip().lower() for skill in skills_input.split(",") if skill.strip()]
    user_location = location_input.strip().lower()

    if user_skills:
        try:
            response = requests.post(
                "https://trainer-matcher.onrender.com/match_trainers",
                json={"skills": user_skills, "location": user_location},
                timeout=10
            )

            if response.status_code == 200:
                matches = response.json().get("matches", [])
                if matches:
                    st.success(f"Found {len(matches)} matching trainer(s)!")
                    for trainer in matches:
                        with st.container():
                            cols = st.columns([1, 3])
                            
                            # Profile Picture
                            with cols[0]:
                                if trainer["pic"]:
                                    st.image(trainer["pic"], width=100)
                                else:
                                    st.image("https://via.placeholder.com/100", width=100)

                            # Trainer Details
                            with cols[1]:
                                st.markdown(f"### 👤 {trainer['name']}")
                                st.markdown(f"🏙️ **City:** {trainer['city'].title()}")
                                st.markdown(f"🧠 **Skills:** `{trainer['skills']}`")
                                st.markdown(f"🎓 **Experience:** {trainer.get('experience', 'N/A')} years")
                                if trainer["linkedin"]:
                                    st.markdown(f"[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-blue?logo=linkedin)]({trainer['linkedin']})", unsafe_allow_html=True)
                                
                                st.markdown("📝 **Bio:**")
                                st.markdown(f"{trainer['bio'][:300]}..." if len(trainer["bio"]) > 300 else trainer["bio"])

                                # Connect Button (redirect to profile)
                                if "profile_url" in trainer:
                                    st.markdown(f"[🔗 Connect to Profile]({trainer['profile_url']})", unsafe_allow_html=True)

                                st.markdown("---")
                else:
                    st.warning("No matching trainers found.")
            else:
                st.error(f"Error: response status is {response.status_code}")
        except Exception as e:
            st.error(f"Error contacting recommendation engine: {e}")
    else:
        st.warning("Please enter at least one skill.")
