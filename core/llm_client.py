import os
from typing import Any, Dict
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class LLMClient:
    """Local Qwen2 client (single-init expected via pipeline singleton)."""
    def __init__(self, config: Dict[str, Any]):
        self.config = config or {}
        model_path = self.config.get("models", {}).get("qwen_path", "models/qwen2-0.5b-instruct")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"❌ Qwen2 model not found at: {model_path}. Edit config.yaml -> models.qwen_path")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
        self.model = AutoModelForCausalLM.from_pretrained(model_path, local_files_only=True)
        self.model.eval()

    def generate(self, prompt: str, max_new_tokens: int = 256, **kwargs) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
