from __future__ import annotations
from typing import Any, Dict, List, Tuple
import torch
import torch.nn.functional as F

LABELS = ["fact","diagnosis_request","advice","emotion"]

class IntentLLMClassifier:
    def __init__(self, model, tokenizer, cfg: Dict[str, Any]):
        self.model = model
        self.tok = tokenizer
        self.cfg = cfg or {}
        # Minimal prompt; projects may replace via config-prompts
        self.template = (
            "Classify the user's medical query into one of: fact, diagnosis_request, advice, emotion.\n"
            "Query: {query}\nLabel:"
        )

    def score_label(self, query: str, label: str) -> float:
        # Next-token scoring over label tokens
        text = self.template.format(query=query)
        in_ids = self.tok(text, return_tensors="pt").input_ids
        lab_ids = self.tok(label, return_tensors="pt").input_ids
        full = torch.cat([in_ids, lab_ids], dim=1)


        model = getattr(self.model, "model", self.model)
        with torch.no_grad():
            out = model(full)
            logits = out.logits  # [1, T, V]

        logprob = 0.0
        for i in range(lab_ids.shape[1]):
            pos = in_ids.shape[1] + i
            step = logits[0, pos - 1, :]  # distribution to generate token at pos
            logprob += float(F.log_softmax(step, dim=-1)[lab_ids[0, i]])
        return logprob

    def predict(self, query: str) -> Dict[str, Any]:
        scores = [self.score_label(query, y) for y in LABELS]
        # softmax for user-friendly probs
        ts = torch.tensor(scores)
        probs = torch.softmax(ts, dim=0).tolist()
        best_idx = int(ts.argmax().item())
        return {
            "label": LABELS[best_idx],
            "scores": {LABELS[i]: float(scores[i]) for i in range(len(LABELS))},
            "probs": {LABELS[i]: float(probs[i]) for i in range(len(LABELS))},
        }
