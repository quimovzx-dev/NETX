import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from config import MAX_RESULTS, REQUEST_TIMEOUT, USER_AGENT

SEARCH_URL = "https://html.duckduckgo.com/html/"

def search(query):
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(
        SEARCH_URL,
        params={"q": query},
        headers=headers,
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    for item in soup.select(".result")[:MAX_RESULTS]:
        title = item.select_one(".result__title")
        link = item.select_one(".result__a")
        snippet = item.select_one(".result__snippet")
        if not title or not link:
            continue
        results.append({
            "title": title.get_text(" ", strip=True),
            "url": link.get("href", ""),
            "snippet": snippet.get_text(" ", strip=True) if snippet else "",
        })
    return results
