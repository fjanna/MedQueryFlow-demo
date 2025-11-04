# 🧠 `models/` Folder Guide

This folder stores all local models used by the project.

---

## 🩺 1. Language Model — Qwen2-0.5B-Instruct

We use **[Qwen2-0.5B-Instruct](https://huggingface.co/Qwen/Qwen2-0.5B-Instruct)**, a compact instruction-tuned large language model designed for reasoning, classification, and medical question answering tasks.

### Model Highlights
- Architecture: Qwen2 (0.5B parameters)
- Purpose: intent classification, query rewrite, and answer generation
- Source: Hugging Face — [Qwen/Qwen2-0.5B-Instruct](https://huggingface.co/Qwen/Qwen2-0.5B-Instruct)
- Notes: lightweight and suitable for CPU or small GPU setups

To download this model automatically, run:

```bash
python scripts/download_model.py --name Qwen2-0.5B-Instruct
```

This will create a folder:
```
models/Qwen2-0.5B-Instruct/
│
├─ config.json
├─ model.safetensors
├─ tokenizer.json
└─ special_tokens_map.json
```

---

## 💬 2. Sentence Embedding Model — paraphrase-MiniLM-L3-v2

We use **[`paraphrase-MiniLM-L3-v2`](https://huggingface.co/sentence-transformers/paraphrase-MiniLM-L3-v2)** from the Sentence-Transformers library, a lightweight model for semantic similarity and retrieval tasks.

### Model Highlights
- Architecture: MiniLM (3 layers)
- Embedding Dimension: 384
- Purpose: semantic similarity, query rewrite evaluation, and retrieval embedding
- Size: ~22 MB

To download this model automatically, run:

```bash
python scripts/download_sbert.py --target models/paraphrase-MiniLM-L3-v2
```

This will create a folder:
```
models/paraphrase-MiniLM-L3-v2/
│
├─ config.json
├─ model.safetensors
├─ tokenizer.json
└─ sentence_bert_config.json
```

---

## 📦 3. Notes

- Both models will be loaded locally in offline environments.
- If the folders already exist, re-running the scripts will **skip re-downloading**.
- It is recommended to add the `models/` folder to `.gitignore` if your repository is public.
