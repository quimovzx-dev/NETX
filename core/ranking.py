from urllib.parse import urlparse
import re

TRUSTED = {
    "wikipedia.org": 10,
    "github.com": 10,
    "microsoft.com": 9,
    "apple.com": 9,
    "google.com": 9,
    "samsung.com": 9,
    "sony.com": 8,
    "oneplus.com": 8,
    "qualcomm.com": 9,
    "intel.com": 9,
    "amd.com": 9,
    "nasa.gov": 10,
    "who.int": 10,
    "gov": 10,
    "edu": 8,
}

def _host(url):
    host = urlparse(url).netloc.lower().split(":")[0]
    return host.removeprefix("www.")

def source_type(url):
    host = _host(url)
    if host.endswith(".gov") or ".gov." in host:
        return "government"
    if host.endswith(".edu") or ".edu." in host:
        return "education"
    if any(host == d or host.endswith("." + d) for d in TRUSTED):
        return "official/reference"
    if "github.com" in host:
        return "code"
    return "web"

def _trusted_score(host):
    best = 0
    for domain, points in TRUSTED.items():
        if domain in {"gov", "edu"}:
            continue
        if host == domain or host.endswith("." + domain):
            best = max(best, points)
    if host.endswith(".gov") or ".gov." in host:
        best = max(best, 10)
    if host.endswith(".edu") or ".edu." in host:
        best = max(best, 8)
    return best

def _terms(query):
    return [x.lower() for x in re.findall(r"[a-zA-Z0-9]{3,}", query)]

def rank(item, query=""):
    host = _host(item.get("url", ""))
    score = _trusted_score(host)

    text = " ".join([
        item.get("title", ""),
        item.get("snippet", ""),
        item.get("content", ""),
    ]).lower()
    terms = _terms(query)
    if terms:
        hits = sum(text.count(term) for term in terms)
        score += min(hits * 0.35 / max(len(terms), 1), 4)

    length = len(item.get("content", ""))
    score += min(length / 5000, 5)

    if item.get("summary"):
        score += 0.5
    if item.get("error"):
        score -= 3

    return round(score, 2)

def rank_results(results, query=""):
    for item in results:
        item["source_type"] = source_type(item.get("url", ""))
        item["score"] = rank(item, query)
    return sorted(results, key=lambda x: x["score"], reverse=True)
