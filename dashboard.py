from http.server import BaseHTTPRequestHandler,HTTPServer
from urllib.parse import urlparse,parse_qs
from database.db import create_tables,stats
from core.local_search import search_local
from projects import list_projects
import json,os
PAGE='''<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>NETX v0.5</title><style>body{margin:0;background:#070b10;color:#eef3f7;font-family:system-ui;padding:18px}main{max-width:900px;margin:auto}input,button{padding:12px;border-radius:10px;border:1px solid #33404d;background:#101822;color:white;margin:3px}.box,.result{background:#111923;border:1px solid #273442;border-radius:14px;padding:16px;margin:12px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px}a{color:#78c8ff}.muted{color:#8e9aa6}</style></head><body><main><h1>NETX ⚡</h1><p class="muted">Internet Intelligence Platform v0.5</p><div class="grid"><div class="box"><b id="sources">—</b><br>Sources</div><div class="box"><b id="queries">—</b><br>Queries</div><div class="box"><b id="hosts">—</b><br>Hosts</div></div><form id="f"><input id="q" placeholder="Search saved research..." style="width:65%"><button>Search</button></form><section id="results"></section><h2>Projects</h2><div id="projects"></div><p><a href="/graph">Open live knowledge graph</a></p></main><script>async function load(){let s=await fetch('/stats').then(r=>r.json());sources.textContent=s.sources;queries.textContent=s.queries;hosts.textContent=s.hosts;let p=await fetch('/projects').then(r=>r.json());projects.innerHTML=p.map(x=>'<div class="box"><b>'+x.name+'</b><br><span class="muted">'+x.queries.length+' queries</span></div>').join('')}load();f.onsubmit=async e=>{e.preventDefault();let q=document.getElementById('q').value;let d=await fetch('/search?q='+encodeURIComponent(q)).then(r=>r.json());results.innerHTML=d.results.map(x=>'<article class="result"><b>'+x.title+'</b><p class="muted">'+(x.summary||'')+'</p><a href="'+x.url+'" target="_blank">'+x.url+'</a></article>').join('')}</script></body></html>'''
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
  if p.path=="/projects":return self.send(json.dumps(list_projects(),ensure_ascii=False))
  if p.path=="/graph":
   js="reports/graph_data.js"
   if not os.path.exists(js):return self.send("No graph yet. Run a research query first.","text/plain",404)
   g=open(js,encoding="utf-8").read()
   page=open("graph_view.html",encoding="utf-8").read().replace("const data=window.NETX_GRAPH||{\"nodes\":[],\"edges\":[]}","const data=window.NETX_GRAPH||{\"nodes\":[],\"edges\":[]}") 
   return self.send(g+"\n"+page,"text/html")
  self.send(json.dumps({"error":"not found"}),status=404)
def start_dashboard(host="127.0.0.1",port=8080):
 create_tables();print(f"Dashboard: http://{host}:{port}");HTTPServer((host,port),Handler).serve_forever()
