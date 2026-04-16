import sys
from pathlib import Path
import streamlit as st

# Add backend folder to import path
BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
sys.path.append(str(BACKEND_DIR))

from search import search_web
from scraper import scrape
from features import build_features
from predictor import predict

st.set_page_config(
    page_title="AI Fake Matrimonial Profile Detector",
    page_icon="🔍",
    layout="centered"
)

st.title("🔍 AI Fake Matrimonial Profile Detector")
st.write("Enter matrimonial profile details to check whether the profile is genuine, suspicious, or fake.")

name = st.text_input("Name")
company = st.text_input("Company / Organization")
job = st.text_input("Occupation / Job Title")
text = st.text_area("Profile Description")

if st.button("Verify Profile"):
    try:
        with st.spinner("Verifying matrimonial profile..."):
            if not name.strip():
                st.error("Name is required.")
                st.stop()

            strict_query = f'"{name}" "{company}" "{job}" matrimonial profile linkedin facebook instagram'
            links = search_web(strict_query)

            if len(links) < 3:
                fallback_query = f'{name} {job} {company} profile india linkedin facebook instagram'
                links = search_web(fallback_query)

            allowed_domains = ["linkedin.com", "facebook.com", "instagram.com"]
            filtered_links = [
                link for link in links
                if any(domain in link.lower() for domain in allowed_domains)
            ]
            if filtered_links:
                links = filtered_links

            web_text = scrape(links)
            text_lower = web_text.lower() if web_text else ""

            data = {
                "name": name,
                "company": company,
                "job": job,
                "text": text
            }

            features = build_features(data, web_text, links)
            prediction, confidence = predict(features)

            name_clean = name.lower().strip()
            company_clean = company.lower().strip()
            job_clean = job.lower().strip()

            name_found = any(
                part in link.lower()
                for link in links
                for part in name_clean.split()
            ) or any(
                part in text_lower
                for part in name_clean.split()
            )

            company_found = (
                any(company_clean in link.lower() for link in links)
                or (company_clean in text_lower if company_clean else False)
            )

            job_found = (
                any(job_clean in link.lower() for link in links)
                or (job_clean in text_lower if job_clean else False)
            )

            full_identity = f"{name_clean} {company_clean}".strip()
            full_identity_match = full_identity in text_lower if full_identity else False

            linkedin_found = any("linkedin.com" in l.lower() for l in links)
            facebook_found = any("facebook.com" in l.lower() for l in links)
            instagram_found = any("instagram.com" in l.lower() for l in links)

            suspicious_keywords = [
                "urgent marriage",
                "send money",
                "looking for bride urgently",
                "investment",
                "crypto",
                "army officer",
                "widowed",
                "settled abroad",
                "rich family",
                "visa",
                "loan",
                "financial help",
                "transfer money"
            ]
            suspicious_claim_found = any(
                keyword in (text.lower() + " " + text_lower)
                for keyword in suspicious_keywords
            )

            analysis = {
                "name_match": name_found,
                "company_match": company_found,
                "job_match": job_found,
                "full_identity_match": full_identity_match,
                "linkedin_found": linkedin_found,
                "facebook_found": facebook_found,
                "instagram_found": instagram_found,
                "web_text_found": len(text_lower) > 100,
                "suspicious_claim_found": suspicious_claim_found
            }

            score = 0.0
            if name_found:
                score += 0.40
            if company_found:
                score += 0.20
            if job_found:
                score += 0.20
            if linkedin_found:
                score += 0.30
            if facebook_found:
                score += 0.05
            if instagram_found:
                score += 0.05
            if suspicious_claim_found:
                score -= 0.40
            if len(text) > 80:
                score += 0.05

            confidence = min(max(score, 0.0), 1.0)

            if confidence >= 0.60:
                prediction = 0
            elif confidence >= 0.30:
                prediction = 1
            else:
                prediction = 2

        st.subheader("Verification Result")
        st.progress(confidence)

        if prediction == 2:
            st.error(f"🚨 Fake Profile (Confidence: {confidence:.2f})")
        elif prediction == 1:
            st.warning(f"⚠️ Suspicious Profile (Confidence: {confidence:.2f})")
        else:
            st.success(f"✅ Genuine Profile (Confidence: {confidence:.2f})")

        if confidence > 0.8:
            st.info("Confidence Level: High")
        elif confidence > 0.5:
            st.info("Confidence Level: Moderate")
        else:
            st.info("Confidence Level: Low")

        st.subheader("Top Websites Found")
        if links:
            for link in links[:5]:
                st.write(link)
        else:
            st.write("No websites found.")

        st.subheader("Analysis")
        for key, value in analysis.items():
            label = key.replace("_", " ").title()
            if value:
                st.success(f"{label}: ✔ Verified")
            else:
                st.warning(f"{label}: ❌ Not Verified")

    except Exception as e:
        st.error("An error occurred.")
        st.write(str(e))
