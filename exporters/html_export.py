import html
import os
from config import HTML_REPORT

def export(results, query):
    os.makedirs(os.path.dirname(HTML_REPORT), exist_ok=True)
    cards = []
    for item in results:
        title = html.escape(item.get("title", "Untitled"))
        url = html.escape(item.get("url", ""), quote=True)
        snippet = html.escape(item.get("snippet", ""))
        score = item.get("score", 0)
        cards.append(f"""<article class="card"><h2>{title}</h2><a href="{url}" target="_blank">{url}</a><p>{snippet}</p><small>NETX score: {score}</small></article>""")

    page = f"""<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>NETX Report</title>
<style>body{{background:#0b0f14;color:#e8edf2;font-family:system-ui;max-width:1000px;margin:40px auto;padding:20px}}h1{{font-size:42px}}.muted{{color:#8d99a6}}.card{{background:#121922;border:1px solid #263241;border-radius:16px;padding:20px;margin:16px 0}}a{{color:#7cc7ff;word-break:break-all}}small{{color:#9aa8b6}}</style></head>
<body><h1>NETX</h1><p class="muted">Research report for: <b>{html.escape(query)}</b></p>{''.join(cards)}</body></html>"""

    with open(HTML_REPORT, "w", encoding="utf-8") as f:
        f.write(page)
    return HTML_REPORT
