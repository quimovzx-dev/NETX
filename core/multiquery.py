def expand_query(query):
    base=query.strip()
    if not base:return []
    return list(dict.fromkeys([base,base+" latest",base+" official",base+" specifications",base+" research"]))
