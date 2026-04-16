import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def scrape(links: list[str]) -> str:
    combined_text = ""

    for link in links[:5]:
        try:
            response = requests.get(link, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            for tag in soup(["script", "style", "noscript"]):
                tag.decompose()

            text = soup.get_text(separator=" ", strip=True)
            combined_text += " " + text[:3000]

        except Exception:
            continue

    return combined_text