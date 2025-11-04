
This folder stores all local models used by the project.

---

## 1. Sentence Embedding Model

We use **[`paraphrase-MiniLM-L3-v2`](https://huggingface.co/sentence-transformers/paraphrase-MiniLM-L3-v2)** from the Sentence-Transformers library.

### Model Highlights
- Architecture: MiniLM (3-layer)
- Embedding Dimension: 384
- Purpose: semantic similarity, query rewrite evaluation, and retrieval embedding
- Size: ~22 MB (very lightweight)

---

## 2. Downloading the Model

You can download it automatically with the provided scripts:

```bash

python scripts/download_sbert.py --target models/paraphrase-MiniLM-L3-v2
python scripts/download_model.py

```

---

## 3. Notes

- The model will be loaded from this folder in offline environments.
