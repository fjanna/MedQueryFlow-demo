from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, List

def _merge_safety(cfg: Dict[str, Any]) -> Dict[str, Any]:
    base = (cfg or {}).get("safety", {}) or {}
    custom = {}
    p = Path("data/emergency_terms.json")
    if p.exists():
        try:
            custom = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"⚠️ Failed to parse emergency_terms.json: {e}")
    merged = {
        "urgent_keywords": [t.lower() for t in custom.get("urgent_keywords", base.get("urgent_keywords", []))],
        "urgent_highlight": custom.get("urgent_highlight", base.get("urgent_highlight", "")),
        "caution_highlight": custom.get("caution_highlight", base.get("caution_highlight", "")),
    }
    return merged

class SafetyGate:
    def __init__(self, cfg: Dict[str, Any]):
        s = _merge_safety(cfg)
        self.urgent_terms = s.get("urgent_keywords", [])
        self.urgent_msg = s.get("urgent_highlight", "")

    def check(self, text: str) -> Dict[str, Any]:
        s = (text or "").lower()
        hit = [t for t in self.urgent_terms if t and t in s]
        return {"urgent": bool(hit), "terms": hit, "message": self.urgent_msg if hit else ""}

class AnswerGenerator:
    def __init__(self, llm, cfg: Dict[str, Any]):
        self.llm = llm
        self.cfg = cfg or {}
        self.safety = SafetyGate(self.cfg)
        p = Path(self.cfg.get("prompts", {}).get("answer_prompt", "prompts/answer_prompt.txt"))
        try:
            self.template = p.read_text(encoding="utf-8")
            self.prompt_error = None
        except Exception as e:
            self.template = ("Answer the medical query with a short, factual, and safe response.\n"
                             "Query: {{query}}\nContext:\n{{context}}\nAnswer:")
            self.prompt_error = f"answer_prompt missing or unreadable: {e}"

    def _build_context(self, retrieved: Dict[str, Any]) -> str:
        lines: List[str] = []
        for p in retrieved.get("local", [])[:5]:
            lines.append(f"[LOCAL] {p.get('text','')[:280]}")
        for w in retrieved.get("web", [])[:3]:
            title = w.get('title','')
            body = w.get('body','')
            lines.append(f"[WEB] {title}: {body[:200]}")
        return "\n".join(lines)

    def generate(self, query: str, retrieved: Dict[str, Any]) -> Dict[str, Any]:
        context = self._build_context(retrieved)
        prompt = self.template.replace("{{query}}", (query or "").strip()).replace("{{context}}", context)
        out = self.llm.generate(prompt, max_new_tokens=self.cfg.get("generation",{}).get("max_new_tokens",256))
        gate = self.safety.check(f"{query} {context}")
        if gate.get("urgent") and gate.get("message"):
            out = f"{gate['message']}\n\n{out}"
        return {
            "text": out,
            "safety_triggered": bool(gate.get("urgent")),
            "safety_terms": gate.get("terms", []),
            "raw_prompt": prompt,
            "answer_prompt_error": self.prompt_error,
        }
