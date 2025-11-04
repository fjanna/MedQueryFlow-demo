from __future__ import annotations
import re
from typing import Literal

Intent = Literal["fact","diagnostic","advisory","emotion","unknown"]

SYMPTOM_HINTS = [
    r"chest (pain|tight(ness)?)", r"short(ness)? of breath|dyspno(e|a)",
    r"syncope|faint", r"headache", r"fever", r"abdominal pain"
]
ADVISORY_HINTS = [r"can i|is it ok|should i|能.*吗|可以.*吗"]
EMOTION_HINTS  = [r"i feel (anxious|sad|worried)|情绪|焦虑|评价|偏方|民间"]

def classify_intent(text: str) -> Intent:
    s = (text or "").lower().strip()
    if not s:
        return "unknown"
    if re.search(r"\b(what|why|how)\b.*(disease|symptom|drug|dose|risk|原因|病|症状)", s):
        return "fact"
    if any(re.search(p, s) for p in SYMPTOM_HINTS):
        return "diagnostic"
    if any(re.search(p, s) for p in ADVISORY_HINTS):
        return "advisory"
    if any(re.search(p, s) for p in EMOTION_HINTS):
        return "emotion"
    return "unknown"
