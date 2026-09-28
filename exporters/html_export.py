import html,os
from datetime import datetime,timezone
from config import HTML_REPORT,VERSION
def export(results,query,graph=None,comparison=None):
 os.makedirs(os.path.dirname(HTML_REPORT),exist_ok=True);cards=[]
 for i,x in enumerate(results,1):
  cards.append(f'<article class="card"><div class="meta">#{i} · {html.escape(x.get("source_type","web"))} · score {x.get("score",0)}</div><h2>{html.escape(x.get("title","Untitled"))}</h2><a href="{html.escape(x.get("url",""),quote=True)}" target="_blank">{html.escape(x.get("url",""))}</a><p>{html.escape(x.get("summary",""))}</p><details><summary>Entities</summary><p>{html.escape(", ".join(e["name"] for e in x.get("entities",[])))}</p></details></article>')
 page=f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>NETX v{VERSION}</title><style>body{{background:#080c12;color:#e8edf2;font-family:system-ui;max-width:1050px;margin:30px auto;padding:20px}}.card{{background:#111923;border:1px solid #263241;border-radius:16px;padding:20px;margin:16px 0}}a{{color:#7cc7ff;word-break:break-all}}.meta,.muted{{color:#8d99a6}}</style></head><body><h1>NETX</h1><p class="muted">v{VERSION} · {html.escape(query)} · {datetime.now(timezone.utc).isoformat()}</p>{"".join(cards)}<details><summary>Knowledge graph data</summary><pre>{html.escape(str(graph or {}))}</pre></details></body></html>'
 with open(HTML_REPORT,"w",encoding="utf-8") as f:f.write(page)
 return HTML_REPORT
