import re
from collections import Counter
STOP={"this","that","with","from","about","which","their","there","have","will","into","than","also","where","what","when","your","more","used","using","were","been","they","them","these","those","some","such"}
def extract_entities(text,limit=30):
    text=" ".join(text.split())
    phrases=re.findall(r"\b[A-Z][A-Za-z0-9&.-]*(?:\s+[A-Z][A-Za-z0-9&.-]*){0,3}",text)
    counts=Counter(p.strip(".,:;!?()[]") for p in phrases)
    result=[]
    for name,count in counts.most_common():
        if len(name)>=3 and name.lower() not in STOP:
            result.append({"name":name,"mentions":count})
        if len(result)>=limit: break
    return result
