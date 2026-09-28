import re
from config import SUMMARY_SENTENCES

def summarize(text, max_sentences=SUMMARY_SENTENCES):
    clean = " ".join(text.split())
    if not clean:
        return ""
    sentences = re.split(r"(?<=[.!?])\s+", clean)
    sentences = [s.strip() for s in sentences if len(s.strip()) >= 45]
    if not sentences:
        return clean[:500]
    scored = []
    for index, sentence in enumerate(sentences):
        words = re.findall(r"[A-Za-z0-9]{4,}", sentence.lower())
        score = min(len(words), 35) / 10
        if any(x in sentence.lower() for x in ("according", "because", "announced", "research", "study", "report")):
            score += 1
        scored.append((score, index, sentence))
    selected = sorted(scored, reverse=True)[:max_sentences]
    selected.sort(key=lambda x: x[1])
    return " ".join(x[2] for x in selected)
