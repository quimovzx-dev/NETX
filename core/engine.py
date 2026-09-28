from concurrent.futures import ThreadPoolExecutor,as_completed
from core.search import search
from core.fetcher import fetch
from core.parser import parse
from core.dedup import deduplicate
from core.ranking import rank_results
from core.summarizer import summarize
from core.entities import extract_entities
from core.graph import build_graph
from core.compare import compare
from database.db import save_results,cached
from exporters.json_export import export as export_json
from exporters.html_export import export as export_html
from config import MAX_WORKERS,MIN_CONTENT_LENGTH
def _enrich(item):
    c=cached(item.get("url",""))
    if c and len(c.get("content",""))>=MIN_CONTENT_LENGTH:
        c["snippet"]=item.get("snippet",c.get("snippet",""));c["title"]=item.get("title",c.get("title",""));c["cached"]=True;c["entities"]=extract_entities(c.get("content",""));return c
    try:
        p=parse(fetch(item["url"]));content=p["content"]
        item.update({"content":content,"page_title":p["title"],"description":p["description"],"summary":summarize(content),"entities":extract_entities(content),"cached":False})
    except Exception as e:item.update({"content":"","summary":"","entities":[],"error":str(e)})
    return item
def run(query):
    print("\n[1/9] Searching web...");results=search(query);print(f"[2/9] Found {len(results)} sources");enriched=[]
    print(f"[3/9] Fetching pages with {MAX_WORKERS} workers...")
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        jobs={pool.submit(_enrich,x):x for x in results}
        for n,f in enumerate(as_completed(jobs),1):
            x=f.result();print(f"    [{n}/{len(results)}] {'cached' if x.get('cached') else 'fetched'}: {x.get('title','')[:65]}");enriched.append(x)
    print("[4/9] Removing duplicates...");cleaned=deduplicate(enriched)
    print("[5/9] Ranking sources...");ranked=rank_results(cleaned,query)
    print("[6/9] Building entity knowledge graph...");graph=build_graph(ranked)
    print("[7/9] Comparing sources...");comparison=compare(ranked)
    print("[8/9] Saving to SQLite...");save_results(query,ranked)
    print("[9/9] Exporting reports...");jp=export_json(ranked,query,graph,comparison);hp=export_html(ranked,query,graph,comparison)
    return ranked,jp,hp,graph,comparison
