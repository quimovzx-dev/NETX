from core.search import search
from core.fetcher import fetch
from core.parser import parse
from core.dedup import deduplicate
from core.ranking import rank_results
from database.db import save_results
from exporters.json_export import export as export_json
from exporters.html_export import export as export_html

def run(query):
    print("\n[1/7] Searching web...")
    results = search(query)

    print(f"[2/7] Found {len(results)} sources")
    enriched = []
    for i, item in enumerate(results, 1):
        print(f"[3/7] Fetching {i}/{len(results)}: {item['title'][:70]}")
        try:
            parsed = parse(fetch(item["url"]))
            item.update({
                "content": parsed["content"],
                "page_title": parsed["title"],
                "description": parsed["description"],
            })
        except Exception as exc:
            item["content"] = ""
            item["error"] = str(exc)
        enriched.append(item)

    print("[4/7] Removing duplicates...")
    cleaned = deduplicate(enriched)
    print("[5/7] Ranking sources...")
    ranked = rank_results(cleaned)
    print("[6/7] Saving to SQLite...")
    save_results(query, ranked)
    print("[7/7] Exporting reports...")
    json_path = export_json(ranked, query)
    html_path = export_html(ranked, query)
    return ranked, json_path, html_path
