import requests
import os
import os
SERP_API_KEY = os.getenv("SERPAPI_API_KEY")
def search_web(query: str) -> list[str]:
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": SERP_API_KEY,
        "engine": "google",
        "num": 10
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()
    data = response.json()

    links = []
    for result in data.get("organic_results", [])[:10]:
        link = result.get("link")
        if link:
            links.append(link)

    return links