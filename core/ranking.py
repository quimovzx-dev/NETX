from urllib.parse import urlparse

TRUSTED = {
    "wikipedia.org": 10,
    "github.com": 10,
    "microsoft.com": 9,
    "apple.com": 9,
    "google.com": 9,
    "samsung.com": 9,
    "sony.com": 8,
    "oneplus.com": 8,
}

def rank(item):
    host = urlparse(item.get("url", "")).netloc.lower()
    host = host.removeprefix("www.")
    score = 0
    for domain, points in TRUSTED.items():
        if host == domain or host.endswith("." + domain):
            score = points
            break
    length = len(item.get("content", ""))
    score += min(length / 5000, 5)
    return round(score, 2)

def rank_results(results):
    for item in results:
        item["score"] = rank(item)
    return sorted(results, key=lambda x: x["score"], reverse=True)
