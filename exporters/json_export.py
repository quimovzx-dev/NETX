import json
import os
from config import JSON_REPORT

def export(results, query):
    os.makedirs(os.path.dirname(JSON_REPORT), exist_ok=True)
    payload = {
        "engine": "NETX",
        "version": "0.1.0",
        "query": query,
        "results": results,
    }
    with open(JSON_REPORT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    return JSON_REPORT
