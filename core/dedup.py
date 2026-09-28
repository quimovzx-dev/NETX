import hashlib

def fingerprint(text):
    normalized = " ".join(text.lower().split())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

def deduplicate(results):
    seen_urls = set()
    seen_content = set()
    output = []

    for item in results:
        url = item.get("url", "")
        content = item.get("content", "")
        content_hash = fingerprint(content) if content else ""
        if url in seen_urls or (content_hash and content_hash in seen_content):
            continue
        seen_urls.add(url)
        if content_hash:
            seen_content.add(content_hash)
        output.append(item)
    return output
