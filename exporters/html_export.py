import html
import os
from datetime import datetime, timezone
from config import HTML_REPORT, VERSION

def export(results, query):
    os.makedirs(os.path.dirname(HTML_REPORT), exist_ok=True)
    cards = []
    for index, item in enumerate(results, 1):
        title = html.escape(item.get("title", "Untitled"))
        url = html.escape(item.get("url", ""), quote=True)
        snippet = html.escape(item.get("snippet", ""))
        summary = html.escape(item.get("summary", ""))
        score = item.get("score", 0)
        source_type = html.escape(item.get("source_type", "web"))
        cards.append(f'''<article class="card"><div class="meta">#{index} · {source_type} · score {score}</div><h2>{title}</h2><a href="{url}" target="_blank" rel="noopener">{url}</a><p>{snippet}</p><details><summary>NETX summary</summary><p>{summary}</p></details></article>''')
    page = f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>NETX Research Report</title><style>body{{background:#080c12;color:#e8edf2;font-family:system-ui;max-width:1050px;margin:30px auto;padding:20px}}h1{{font-size:42px;margin-bottom:4px}}.muted,.meta{{color:#8d99a6}}.card{{background:#111923;border:1px solid #263241;border-radius:16px;padding:20px;margin:16px 0}}a{{color:#7cc7ff;word-break:break-all}}summary{{cursor:pointer;color:#a9d8ff}}</style></head><body><h1>NETX</h1><p class="muted">v{VERSION} · {html.escape(query)} · {datetime.now(timezone.utc).isoformat()}</p>{''.join(cards)}</body></html>'''
    with open(HTML_REPORT, "w", encoding="utf-8") as f:
        f.write(page)
    return HTML_REPORT
