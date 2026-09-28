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
from core.multiquery import expand_query
from core.clustering import cluster
from database.db import save_results,cached
from exporters.json_export import export as export_json
from exporters.html_export import export as export_html
from config import MAX_WORKERS,MIN_CONTENT_LENGTH
def _enrich(item):
 c=cached(item.get("url",""))
 if c and len(c.get("content",""))>=MIN_CONTENT_LENGTH:
  c["snippet"]=item.get("snippet",c.get("snippet",""));c["title"]=item.get("title",c.get("title",""));c["cached"]=True;c["entities"]=extract_entities(c.get("content",""));return c
 try:
  p=parse(fetch(item["url"]));content=p["content"];item.update({"content":content,"page_title":p["title"],"description":p["description"],"summary":summarize(content),"entities":extract_entities(content),"cached":False})
 except Exception as e:item.update({"content":"","summary":"","entities":[],"error":str(e)})
 return item
def run(query):
 print("\n[1/10] Expanding research query...")
 variants=expand_query(query); print("    "+ " | ".join(variants))
 results=[]
 for variant in variants:
  try: results.extend(search(variant))
  except Exception as e: print(f"    Search warning: {e}")
 print(f"[2/10] Found {len(results)} raw sources")
 enriched=[];print(f"[3/10] Fetching pages with {MAX_WORKERS} workers...")
 with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
  jobs={pool.submit(_enrich,x):x for x in results}
  for n,f in enumerate(as_completed(jobs),1):
   x=f.result();print(f"    [{n}/{len(results)}] {'cached' if x.get('cached') else 'fetched'}: {x.get('title','')[:65]}");enriched.append(x)
 print("[4/10] Removing duplicates...");cleaned=deduplicate(enriched)
 print("[5/10] Ranking sources...");ranked=rank_results(cleaned,query)
 print("[6/10] Building entity knowledge graph...");graph=build_graph(ranked)
 print("[7/10] Comparing sources + clustering topics...");comparison=compare(ranked);topics=cluster(ranked)
 print("[8/10] Saving to SQLite...");save_results(query,ranked)
 print("[9/10] Exporting reports...");jp=export_json(ranked,query,graph,comparison,topics);hp=export_html(ranked,query,graph,comparison,topics)
 print("[10/10] Research complete.")
 return ranked,jp,hp,graph,comparison,topics
