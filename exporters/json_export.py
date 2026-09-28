import json,os
from datetime import datetime,timezone
from config import JSON_REPORT,VERSION
def export(results,query,graph=None,comparison=None,topics=None):
 os.makedirs(os.path.dirname(JSON_REPORT),exist_ok=True)
 payload={"engine":"NETX","version":VERSION,"generated_at":datetime.now(timezone.utc).isoformat(),"query":query,"result_count":len(results),"results":results,"knowledge_graph":graph or {"nodes":[],"edges":[]},"comparison":comparison or {},"topics":topics or []}
 with open(JSON_REPORT,"w",encoding="utf-8") as f:json.dump(payload,f,indent=2,ensure_ascii=False)
 return JSON_REPORT
