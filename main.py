from config import APP_NAME,VERSION
from database.db import create_tables,history,stats
from core.engine import run
from core.local_search import search_local
from api import start_api
def banner():
 print(r'''\n╔══════════════════════════════════════════╗
║        NETX — INTERNET INTELLIGENCE     ║
║                 ENGINE                   ║
╚══════════════════════════════════════════╝''');print(f"{APP_NAME} v{VERSION}");print("Commands: /history /stats /local <term> /api /help /exit\n")
def main():
 create_tables();banner()
 while True:
  q=input("NETX > ").strip()
  if q.lower() in {"/exit","exit","quit","q"}:print("NETX shutting down.");break
  if q.lower()=="/help":print("\n/history  recent research\n/stats    database stats\n/local X  search saved research\n/api      start local REST API\n/exit     quit\n");continue
  if q.lower()=="/history":
   for x in history():print(f"  • {x[0]} ({x[1]} sources) — {x[2]}")
   print();continue
  if q.lower()=="/stats":
   s=stats();print(f"\nSources: {s['sources']}\nQueries: {s['queries']}\nHosts: {s['unique_hosts']}\n");continue
  if q.lower().startswith("/local "):
   for x in search_local(q[7:]):print(f"\n{x['title']}\n{x['source_type']} · {x['score']}\n{x['url']}\n{x['summary']}")
   print();continue
  if q.lower()=="/api":start_api();continue
  if not q:continue
  try:
   results,jp,hp,graph,comparison=run(q)
   print("\n========== TOP RESULTS ==========")
   for i,x in enumerate(results,1):print(f"\n{i}. {x.get('title','Untitled')}\n   Type: {x.get('source_type')}\n   Score: {x.get('score')}\n   Summary: {x.get('summary','')[:300]}\n   Entities: {', '.join(e['name'] for e in x.get('entities',[])[:8])}\n   URL: {x.get('url','')}")
   print(f"\nGraph: {len(graph['nodes'])} nodes / {len(graph['edges'])} edges");print(f"Reports: {jp} | {hp}\n")
  except Exception as e:print(f"\n[ERROR] {e}\n")
if __name__=="__main__":main()
