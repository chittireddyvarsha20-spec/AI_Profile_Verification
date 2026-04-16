from difflib import SequenceMatcher


def similarity(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def clean_text(text: str) -> str:
    return (
        text.lower()
        .replace(".", "")
        .replace(" ", "")
        .replace("-", "")
        .replace("_", "")
        .replace("/", "")
    )


def exact_match(value: str, text: str) -> float:
    if not value or not text:
        return 0.0
    return 1.0 if clean_text(value) in clean_text(text) else 0.0


def keyword_presence(keyword: str, text: str) -> float:
    if not keyword or not text:
        return 0.0
    return 1.0 if keyword.lower() in text.lower() else 0.0


def social_trust_score(links: list[str]) -> float:
    trusted_domains = ["linkedin.com", "facebook.com", "instagram.com"]
    if not links:
        return 0.0

    score = 0.0
    for link in links:
        if any(domain in link.lower() for domain in trusted_domains):
            score += 0.25

    return min(score, 1.0)


def build_features(data: dict, web_text: str, links: list[str]) -> list[float]:
    name = data.get("name", "")
    company = data.get("company", "")
    job = data.get("job", "")
    profile_text = data.get("text", "")

    text = web_text.lower() if web_text else ""

    name_score = max(
        similarity(name, text),
        exact_match(name, text),
        keyword_presence(name, text)
    )

    job_score = max(
        similarity(job, text),
        keyword_presence(job, text)
    )

    company_score = max(
        similarity(company, text),
        keyword_presence(company, text)
    )

    presence_score = min(len(text) / 4000, 1.0)

    description_score = 0.0
    if profile_text:
        description_score = max(
            similarity(name, profile_text),
            similarity(company, profile_text),
            similarity(job, profile_text)
        )

    trust_score = social_trust_score(links)

    combined_presence = min(
        (presence_score * 0.6) +
        (trust_score * 0.3) +
        (description_score * 0.1),
        1.0
    )

    return [
        name_score,
        job_score,
        company_score,
        combined_presence
    ]
