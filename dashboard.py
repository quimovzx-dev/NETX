from http.server import BaseHTTPRequestHandler,HTTPServer
from urllib.parse import urlparse,parse_qs
from database.db import create_tables,stats
from core.local_search import search_local
import json
PAGE='''<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>NETX Dashboard</title><style>body{margin:0;background:#070b10;color:#eef3f7;font-family:system-ui;padding:18px}main{max-width:900px;margin:auto}input,button{padding:13px;border-radius:10px;border:1px solid #33404d;background:#101822;color:white}button{cursor:pointer}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}.box,.result{background:#111923;border:1px solid #273442;border-radius:14px;padding:16px;margin:12px 0}.muted{color:#8e9aa6}a{color:#78c8ff}#results{margin-top:15px}</style></head><body><main><h1>NETX ⚡</h1><p class="muted">Internet Intelligence Dashboard</p><div class="grid"><div class="box"><b id="sources">—</b><br>Sources</div><div class="box"><b id="queries">—</b><br>Queries</div><div class="box"><b id="hosts">—</b><br>Hosts</div></div><form id="f"><input id="q" placeholder="Search saved research..." style="width:65%"><button>Search</button></form><section id="results"></section></main><script>async function load(){let s=await fetch('/stats').then(r=>r.json());sources.textContent=s.sources;queries.textContent=s.queries;hosts.textContent=s.hosts}load();f.onsubmit=async e=>{e.preventDefault();let q=document.getElementById('q').value;let d=await fetch('/search?q='+encodeURIComponent(q)).then(r=>r.json());results.innerHTML=d.results.map(x=>'<article class="result"><b>'+x.title+'</b><p class="muted">'+(x.summary||'')+'</p><a href="'+x.url+'" target="_blank">'+x.url+'</a></article>').join('')}</script></body></html>'''
class Handler(BaseHTTPRequestHandler):
 def send(self,data,ctype="application/json",status=200):
  raw=data if isinstance(data,bytes) else data.encode();self.send_response(status);self.send_header("Content-Type",ctype);self.send_header("Content-Length",str(len(raw)));self.end_headers();self.wfile.write(raw)
 def do_GET(self):
  p=urlparse(self.path)
  if p.path=="/":return self.send(PAGE,"text/html")
  if p.path=="/stats":
   s=stats();return self.send(json.dumps({"sources":s["sources"],"queries":s["queries"],"hosts":s["unique_hosts"]}))
  if p.path=="/search":
   q=parse_qs(p.query).get("q",[""])[0];return self.send(json.dumps({"results":search_local(q)}))
  self.send(json.dumps({"error":"not found"}),status=404)
def start_dashboard(host="127.0.0.1",port=8080):
 create_tables();print(f"Dashboard: http://{host}:{port}");HTTPServer((host,port),Handler).serve_forever()
