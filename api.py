from http.server import BaseHTTPRequestHandler,HTTPServer
import json
from urllib.parse import urlparse,parse_qs
from database.db import create_tables,history,stats
from core.local_search import search_local
class Handler(BaseHTTPRequestHandler):
 def _send(self,data,status=200):
  raw=json.dumps(data,ensure_ascii=False).encode();self.send_response(status);self.send_header("Content-Type","application/json; charset=utf-8");self.send_header("Content-Length",str(len(raw)));self.end_headers();self.wfile.write(raw)
 def do_GET(self):
  p=urlparse(self.path)
  if p.path=="/health": return self._send({"ok":True,"engine":"NETX"})
  if p.path=="/stats": return self._send(stats())
  if p.path=="/history": return self._send([{"query":q,"sources":n,"created_at":t} for q,n,t in history(20)])
  if p.path=="/search":
   q=parse_qs(p.query).get("q",[""])[0].strip()
   return self._send({"query":q,"results":search_local(q)} if q else {"error":"missing q"},200 if q else 400)
  return self._send({"error":"not found"},404)
def start_api(host="127.0.0.1",port=8080):
 create_tables();print(f"NETX API listening on http://{host}:{port}");HTTPServer((host,port),Handler).serve_forever()
if __name__=="__main__": start_api()
