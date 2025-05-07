import streamlit as st
import requests

st.set_page_config(page_title="Trainer Recommender", layout="wide")

st.title("🔍 Trainer Recommender")
st.markdown("Enter your **desired skills** and **location** to find top trainers.")

# Input form
with st.form("recommendation_form"):
    skills_input = st.text_input("Skills you're looking to learn (comma-separated)", "")
    location_input = st.text_input("Preferred City (optional)", "")
    submitted = st.form_submit_button("Find Trainers")

if submitted:
    with st.spinner("Finding best trainers..."):
        api_url = "https://trainer-matcher.onrender.com/match_trainers"  # Replace with your live Render URL
        payload = {
            "skills": [s.strip() for s in skills_input.split(",") if s.strip()],
            "location": location_input.strip()
        }

        try:
            res = requests.post(api_url, json=payload)
            if res.status_code == 200:
                results = res.json()["matches"]
                if results:
                    st.success(f"Found {len(results)} matching trainers")
                    for trainer in results:
                        with st.container():
                            col1, col2 = st.columns([1, 3])
                            with col1:
                                if trainer["pic"]:
                                    st.image(trainer["pic"], width=100)
                            with col2:
                                st.subheader(trainer["name"])
                                st.markdown(f"**City:** {trainer['city']}")
                                st.markdown(f"**Skills:** {trainer['skills']}")
                                st.markdown(f"**Membership:** {trainer['membership']}")
                                st.markdown(f"**Bio:** {trainer['bio']}")
                                if trainer["linkedin"]:
                                    st.markdown(f"[LinkedIn Profile]({trainer['linkedin']})")
                            st.markdown("---")
                else:
                    st.warning("No matching trainers found. Try other skills or locations.")
            else:
                st.error("Error contacting recommendation engine.")
        except Exception as e:
            st.error(f"Something went wrong: {e}")
