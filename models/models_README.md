# 🧠 `models/` Folder Guide

This folder stores all local models used by the project.

---

## 🩺 1. Sentence Embedding Model

We use **[`paraphrase-MiniLM-L3-v2`](https://huggingface.co/sentence-transformers/paraphrase-MiniLM-L3-v2)** from the Sentence-Transformers library.

### Model Highlights
- Architecture: MiniLM (3-layer)
- Embedding Dimension: 384
- Purpose: semantic similarity, query rewrite evaluation, and retrieval embedding
- Size: ~22 MB (very lightweight)

---

## ⚙️ 2. Downloading the Model

You can download it automatically with one of the provided scripts:

```bash
# Option 1: Recommended – download via Hugging Face API
python scripts/download_sbert.py --target models/paraphrase-MiniLM-L3-v2

# Option 2: Generic downloader
python scripts/download_model.py --name paraphrase-MiniLM-L3-v2
```

Both scripts will automatically create the folder:

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

- The model will be loaded from this folder in offline environments.
- If the folder already exists, re-running the script will **skip re-downloading**.
- Make sure to keep this folder under `.gitignore` if the repo is public, since model weights are large.
