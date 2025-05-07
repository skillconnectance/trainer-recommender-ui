import streamlit as st
import requests

st.title("Trainer Recommender")

# Input from user
skills_input = st.text_input("Enter skills you're looking for (comma-separated):")
location_input = st.text_input("Enter your location:")

if st.button("Find Trainers"):
    # Process user input
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
                    st.success(f"Found {len(matches)} matching trainers!")
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
                st.error(f"Error: response status is {response.status_code}")
        except Exception as e:
            st.error(f"Error contacting recommendation engine: {e}")
    else:
        st.warning("Please enter at least one skill.")
