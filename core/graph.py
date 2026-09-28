import json,os
from collections import defaultdict
def build_graph(results):
 nodes={};edges=defaultdict(set)
 for item in results:
  source=item.get("url","") or item.get("title","");nodes[source]={"id":source,"label":item.get("title","Untitled"),"type":"source","score":item.get("score",0)}
  for entity in item.get("entities",[]):
   eid="entity:"+entity["name"].lower();nodes[eid]={"id":eid,"label":entity["name"],"type":"entity","mentions":entity["mentions"]};edges[source].add(eid)
 return {"nodes":list(nodes.values()),"edges":[{"from":a,"to":b} for a,bs in edges.items() for b in bs]}
def export_graph(graph,path="reports/graph_data.js"):
 os.makedirs(os.path.dirname(path),exist_ok=True)
 with open(path,"w",encoding="utf-8") as f:f.write("window.NETX_GRAPH="+json.dumps(graph,ensure_ascii=False)+";")
 return path
