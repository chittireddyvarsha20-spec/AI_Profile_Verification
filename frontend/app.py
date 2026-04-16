import streamlit as st
import requests

# Backend API URL (Render)
API_URL = "https://ai-profile-backend.onrender.com/verify"

# Page config
st.set_page_config(
    page_title="AI Fake Matrimonial Profile Detector",
    page_icon="🔍",
    layout="centered"
)

# Title
st.title("🔍 AI Fake Matrimonial Profile Detector")
st.write("Enter matrimonial profile details to check whether the profile is genuine, suspicious, or fake.")

# Input fields
name = st.text_input("Name")
company = st.text_input("Company / Organization")
job = st.text_input("Occupation / Job Title")
description = st.text_area("Profile Description")

# Button
if st.button("Verify Profile"):
    try:
        if not name.strip():
            st.error("Name is required.")
            st.stop()

        with st.spinner("Analyzing profile..."):

            # Prepare data for backend
            payload = {
                "name": name,
                "company": company,
                "job_title": job,
                "description": description
            }

            # Send request to backend
            response = requests.post(API_URL, json=payload)

            # Check response
            if response.status_code != 200:
                st.error(f"Error: {response.status_code}")
                st.write(response.text)
                st.stop()

            result = response.json()

            prediction = result.get("prediction")
            confidence = result.get("confidence")
            sources = result.get("sources", [])

        # Display results
        st.subheader("Verification Result")

        if confidence is not None:
            st.progress(float(confidence))

        # Show prediction
        if prediction == 2 or prediction == "Fake":
            st.error(f"🚨 Fake Profile (Confidence: {confidence:.2f})")
        elif prediction == 1 or prediction == "Suspicious":
            st.warning(f"⚠️ Suspicious Profile (Confidence: {confidence:.2f})")
        else:
            st.success(f"✅ Genuine Profile (Confidence: {confidence:.2f})")

        # Confidence level
        if confidence is not None:
            if confidence > 0.8:
                st.info("Confidence Level: High")
            elif confidence > 0.5:
                st.info("Confidence Level: Moderate")
            else:
                st.info("Confidence Level: Low")

        # Show sources
        st.subheader("Top Websites Found")
        if sources:
            for link in sources[:5]:
                st.write(link)
        else:
            st.write("No websites found.")

    except Exception as e:
        st.error("An error occurred.")
        st.write(str(e))

