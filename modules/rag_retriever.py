from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, List
import math

try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
except Exception:
    SentenceTransformer = None
    np = None

class RAGRetriever:
    def __init__(self, cfg: Dict[str, Any]):
        self.cfg = cfg or {}
        self.sbert_path = (self.cfg.get("models", {}) or {}).get("sbert_path", "models/paraphrase-MiniLM-L3-v2")
        self.local_top_k = (self.cfg.get("retrieval", {}) or {}).get("local_top_k", 5)
        self.model = None
        if SentenceTransformer is not None:
            try:
                self.model = SentenceTransformer(self.sbert_path, device="cpu")
            except Exception as e:
                print(f"⚠️ SBERT load failed ({self.sbert_path}): {e}")

        self.corpus = []
        p = Path("data/medquad_subset.json")
        if p.exists():
            try:
                self.corpus = json.loads(p.read_text(encoding="utf-8"))
            except Exception as e:
                print(f"⚠️ Failed to parse medquad_subset.json: {e}")
        else:
            self.corpus = []

        self.embeddings = None
        if self.model is not None and np is not None and self.corpus:
            try:
                texts = [c.get("text","") for c in self.corpus]
                self.embeddings = self.model.encode(texts, show_progress_bar=False, convert_to_numpy=True, normalize_embeddings=True)
            except Exception as e:
                print(f"⚠️ SBERT encoding failed: {e}")

    def retrieve_local(self, query: str) -> List[Dict[str, Any]]:
        if self.model is None or self.embeddings is None or not self.corpus:
            return []
        vq = self.model.encode([query], show_progress_bar=False, convert_to_numpy=True, normalize_embeddings=True)[0]
        sims = self.embeddings @ vq
        idx = sims.argsort()[::-1][: self.local_top_k]
        results: List[Dict[str, Any]] = []
        for i in idx:
            item = dict(self.corpus[i])
            item["score"] = float(sims[i])
            results.append(item)
        return results

    def retrieve_web(self, query: str) -> List[Dict[str, Any]]:
        # web disabled in offline bundle; keep stub for API compatibility
        use_web = (self.cfg.get("retrieval", {}) or {}).get("use_web", False)
        if not use_web:
            return []
        try:
            from ddgs import DDGS
        except Exception:
            return []
        region = (self.cfg.get("retrieval", {}) or {}).get("ddg_region", "us-en")
        safe = (self.cfg.get("retrieval", {}) or {}).get("ddg_safe_search", "Moderate")
        timeout = (self.cfg.get("retrieval", {}) or {}).get("ddg_timeout_sec", 8)
        topk = (self.cfg.get("retrieval", {}) or {}).get("web_top_k", 5)
        out = []
        try:
            with DDGS(timeout=timeout) as ddgs:
                for r in ddgs.text(query, region=region, safesearch=safe, max_results=topk):
                    out.append({
                        "title": r.get("title",""),
                        "href": r.get("href",""),
                        "body": r.get("body",""),
                    })
        except Exception as e:
            print(f"⚠️ DDGS search failed: {e}")
        return out

MedicalRAGRetriever = RAGRetriever

