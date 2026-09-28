from concurrent.futures import ThreadPoolExecutor, as_completed
from core.search import search
from core.fetcher import fetch
from core.parser import parse
from core.dedup import deduplicate
from core.ranking import rank_results
from core.summarizer import summarize
from database.db import save_results, cached
from exporters.json_export import export as export_json
from exporters.html_export import export as export_html
from config import MAX_WORKERS, MIN_CONTENT_LENGTH

def _enrich(item):
    cached_item = cached(item.get("url", ""))
    if cached_item and len(cached_item.get("content", "")) >= MIN_CONTENT_LENGTH:
        cached_item["snippet"] = item.get("snippet", cached_item.get("snippet", ""))
        cached_item["title"] = item.get("title", cached_item.get("title", ""))
        cached_item["cached"] = True
        return cached_item
    try:
        parsed = parse(fetch(item["url"]))
        content = parsed["content"]
        item.update({
            "content": content,
            "page_title": parsed["title"],
            "description": parsed["description"],
            "summary": summarize(content),
            "cached": False
        })
    except Exception as exc:
        item.update({"content": "", "summary": "", "error": str(exc)})
    return item

def run(query):
    print("\n[1/7] Searching web...")
    results = search(query)
    print(f"[2/7] Found {len(results)} sources")
    enriched = []
    print(f"[3/7] Fetching pages with {MAX_WORKERS} workers...")
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        jobs = {pool.submit(_enrich, item): item for item in results}
        for completed, future in enumerate(as_completed(jobs), 1):
            item = future.result()
            status = "cached" if item.get("cached") else "fetched"
            print(f"    [{completed}/{len(results)}] {status}: {item.get('title', '')[:65]}")
            enriched.append(item)
    print("[4/7] Removing duplicates...")
    cleaned = deduplicate(enriched)
    print("[5/7] Ranking + summarizing sources...")
    ranked = rank_results(cleaned, query)
    print("[6/7] Saving to SQLite...")
    save_results(query, ranked)
    print("[7/7] Exporting reports...")
    return ranked, export_json(ranked, query), export_html(ranked, query)
