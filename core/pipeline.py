from __future__ import annotations
from typing import Dict, Any
import os

from core.llm_client import LLMClient
from modules.intent_classifier import classify_intent
from modules.intent_llm_classifier import IntentLLMClassifier
from modules.query_rewriter import QueryRewriter
# 修正命名：RAGRetriever 替代 MedicalRAGRetriever
from modules.rag_retriever import RAGRetriever as MedicalRAGRetriever
from modules.answer_generator import AnswerGenerator


class MedQueryFlowPipeline:
    _llm_singleton = None
    _intent_llm = None

    def __init__(self, config: Dict[str, Any]):
        self.config = config or {}
        if self.config.get("models", {}).get("offline", False):
            os.environ["TRANSFORMERS_OFFLINE"] = "1"

        if MedQueryFlowPipeline._llm_singleton is None:
            MedQueryFlowPipeline._llm_singleton = LLMClient(self.config)
        self.llm = MedQueryFlowPipeline._llm_singleton
        self.tokenizer = self.llm.tokenizer  # 新增：保存 tokenizer 引用

        # 修正参数：IntentLLMClassifier 需要 (model, tokenizer, cfg)
        if self.config.get("intent", {}).get("use_llm", False):
            MedQueryFlowPipeline._intent_llm = IntentLLMClassifier(self.llm, self.tokenizer, self.config)
            self.intent_mode = "llm"
        else:
            self.intent_mode = "rule"

        self.retriever = MedicalRAGRetriever(self.config)
        self.rewriter = QueryRewriter(self.llm, self.config)
        self.generator = AnswerGenerator(self.llm, self.config)

    def run(self, user_query: str) -> Dict[str, Any]:
        intent = None
        intent_probs = None
        raw_intent_prompt = None

        if self.intent_mode == "llm":
            # 确保 classify_with_conf 存在；如新版只有 predict()，可替换
            if hasattr(MedQueryFlowPipeline._intent_llm, "classify_with_conf"):
                intent, intent_probs, raw_intent_prompt = MedQueryFlowPipeline._intent_llm.classify_with_conf(user_query)
            else:
                result = MedQueryFlowPipeline._intent_llm.predict(user_query)
                intent = result["label"]
                intent_probs = result.get("probs")
        else:
            intent = classify_intent(user_query)

        rewrites, rewrite_err = self.rewriter.rewrite(user_query)

        retrieved = {"local": [], "web": []}
        if intent in ("fact", "diagnostic", "advisory", "unknown"):
            collected = []
            for q in rewrites:
                collected.extend(self.retriever.retrieve_local(q))
            seen, uniq = set(), []
            for it in collected:
                key = it.get("id") or it.get("text")
                if key not in seen:
                    uniq.append(it)
                    seen.add(key)
            retrieved["local"] = uniq[: self.config.get("retrieval", {}).get("local_top_k", 5)]

        if self.config.get("retrieval", {}).get("use_web", False) and intent != "emotion":
            for q in rewrites[:2]:
                retrieved["web"].extend(self.retriever.retrieve_web(q))

        answer = self.generator.generate(user_query, retrieved)

        return {
            "intent": intent,
            "intent_probs": intent_probs,
            "intent_raw_prompt": raw_intent_prompt,
            "rewrites": rewrites,
            "rewrite_prompt_error": rewrite_err,
            "retrieved": retrieved,
            "answer": answer,
            "corpus_ok": getattr(self.retriever, "corpus_ok", True)
        }

