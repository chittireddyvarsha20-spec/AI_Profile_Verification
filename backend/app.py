from fastapi import FastAPI
from predictor import predict
from features import build_features
from search import search_web
from scraper import scrape

app = FastAPI()


@app.get("/")
def home():
    return {"message": "AI Fake Matrimonial Profile Detector API Running"}


@app.post("/verify")
def verify(data: dict):
    try:
        name = data.get("name", "").strip()
        company = data.get("company", "").strip()
        job = data.get("job", "").strip()
        profile_text = data.get("text", "").strip()

        if not name:
            return {"error": "Name is required"}

        # 1. Search query
        strict_query = f'"{name}" "{company}" "{job}" matrimonial profile linkedin facebook instagram'
        links = search_web(strict_query)

        # 2. Fallback search
        if len(links) < 3:
            fallback_query = f'{name} {job} {company} profile india linkedin facebook instagram'
            links = search_web(fallback_query)

        # 3. Keep only useful social/profile links
        allowed_domains = ["linkedin.com", "facebook.com", "instagram.com"]
        filtered_links = [
            link for link in links
            if any(domain in link.lower() for domain in allowed_domains)
        ]
        if filtered_links:
            links = filtered_links

        # 4. Scrape text
        web_text = scrape(links)
        text_lower = web_text.lower() if web_text else ""

        # 5. Build ML features
        features = build_features(data, web_text, links)

        # 6. ML prediction (kept, but overridden by final logic)
        prediction, confidence = predict(features)

        # 7. Normalized values
        name_clean = name.lower().strip()
        company_clean = company.lower().strip()
        job_clean = job.lower().strip()

        # 8. Relaxed matching logic
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

        # 9. Social presence
        linkedin_found = any("linkedin.com" in l.lower() for l in links)
        facebook_found = any("facebook.com" in l.lower() for l in links)
        instagram_found = any("instagram.com" in l.lower() for l in links)

        # 10. Suspicious matrimonial keywords
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
            keyword in (profile_text.lower() + " " + text_lower)
            for keyword in suspicious_keywords
        )

        # 11. Analysis
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

        # 12. Improved scoring
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

        # Bonus for strong description
        if len(profile_text) > 80:
            score += 0.05

        confidence = min(max(score, 0.0), 1.0)

        # 13. Final decision
        if confidence >= 0.60:
            prediction = 0   # Genuine
        elif confidence >= 0.30:
            prediction = 1   # Suspicious
        else:
            prediction = 2   # Fake

        return {
            "prediction": int(prediction),
            "confidence": float(round(confidence, 2)),
            "sources": links[:5],
            "analysis": analysis
}
    except Exception as e:
        return {"error": str(e)}
