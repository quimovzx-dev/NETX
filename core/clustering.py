import re
from collections import Counter
def cluster(results,limit=6):
    groups={}
    for item in results:
        words=re.findall(r"[a-zA-Z]{5,}",(item.get("title","")+" "+item.get("summary","")).lower())
        words=[w for w in words if w not in {"about","which","their","there","these","those","using","between","through"}]
        key=Counter(words).most_common(1); label=key[0][0] if key else "other"
        groups.setdefault(label,[]).append(item.get("title","Untitled"))
    return [{"topic":k,"sources":v,"count":len(v)} for k,v in sorted(groups.items(),key=lambda x:len(x[1]),reverse=True)[:limit]]
