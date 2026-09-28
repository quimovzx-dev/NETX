import re
def _words(text): return set(re.findall(r"[a-zA-Z0-9]{4,}",text.lower()))
def compare(results):
    docs=[_words(x.get("content","")) for x in results if x.get("content")]
    common=set.intersection(*docs) if docs else set()
    return {"shared_terms":sorted(common)[:80],"sources":[{"title":x.get("title","Untitled"),"url":x.get("url",""),"summary":x.get("summary",""),"unique_terms":sorted(_words(x.get("content",""))-common)[:40]} for x in results]}
