
This folder stores all local models used by the project.

---

## 1. Language Model — Qwen2-0.5B-Instruct

We use **[Qwen2-0.5B-Instruct](https://huggingface.co/Qwen/Qwen2-0.5B-Instruct)** for reasoning, classification, and medical question answering tasks.

To download this model automatically, run:

```bash
python scripts/download_model.py
```

---

## 2. Sentence Embedding Model — paraphrase-MiniLM-L3-v2

We use **[`paraphrase-MiniLM-L3-v2`](https://huggingface.co/sentence-transformers/paraphrase-MiniLM-L3-v2)** from the Sentence-Transformers library, a lightweight model for semantic similarity and retrieval tasks.


To download this model automatically, run:

```bash
python scripts/download_sbert.py --target models/paraphrase-MiniLM-L3-v2
```


---

## 3. Notes

- Both models will be loaded locally in offline environments.
