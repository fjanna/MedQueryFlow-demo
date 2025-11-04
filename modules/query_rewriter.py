from __future__ import annotations
from typing import List, Tuple
from pathlib import Path

class QueryRewriter:
    def __init__(self, llm, cfg):
        self.llm = llm
        self.cfg = cfg or {}
        p = Path(self.cfg.get("prompts", {}).get("rewrite_prompt", "prompts/rewrite_prompt.txt"))
        self.template = None
        self.prompt_error = None
        try:
            self.template = p.read_text(encoding="utf-8")
        except Exception as e:
            self.prompt_error = f"rewrite_prompt missing or unreadable: {e}"

    def rewrite(self, user_query: str) -> Tuple[List[str], str]:
        q = (user_query or "").strip()
        if not q:
            return [], self.prompt_error

        if self.template is None:
            # Fallback rewrites if prompt file is missing
            rewrites = [q, f"{q} causes and red flags", f"{q} related symptoms"]
            return rewrites, self.prompt_error

        prompt = self.template.replace("{{query}}", q)
        text = self.llm.generate(prompt, max_new_tokens=200)
        lines = [ln.strip() for ln in text.splitlines()]
        out = []
        for ln in lines:
            if not ln:
                continue
            ln = ln.lstrip("-•*0123456789. ").strip()
            if len(ln) > 2 and ln.lower() not in {x.lower() for x in out}:
                out.append(ln)
        if not out:
            out = [q, f"{q} causes and red flags", f"{q} related symptoms"]
        return out[:5], None
