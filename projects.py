import json,os
from datetime import datetime,timezone
PROJECT_FILE=os.path.join("data","projects.json")
def _load():
 os.makedirs("data",exist_ok=True)
 if not os.path.exists(PROJECT_FILE): return {}
 try:
  with open(PROJECT_FILE,encoding="utf-8") as f:return json.load(f)
 except:return {}
def _save(x):
 with open(PROJECT_FILE,"w",encoding="utf-8") as f:json.dump(x,f,indent=2,ensure_ascii=False)
def create(name):
 x=_load(); x[name]={"name":name,"created_at":datetime.now(timezone.utc).isoformat(),"queries":[]};_save(x);return x[name]
def add_query(name,query):
 x=_load()
 if name not in x:create(name);x=_load()
 if query not in x[name]["queries"]:x[name]["queries"].append(query)
 _save(x)
def list_projects():return list(_load().values())
def get(name):return _load().get(name)
