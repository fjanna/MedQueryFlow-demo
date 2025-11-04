# 🧠 MedQueryFlow — Multi-Stage Medical Q&A Pipeline (Offline RAG)

MedQueryFlow is a **prompt-orchestrated medical Q&A system** integrating local models, retrieval, and structured safety control.  
It supports **offline execution** via compact open-source models — [`Qwen2-0.5B-Instruct`](https://huggingface.co/Qwen/Qwen2-0.5B-Instruct) for reasoning and [`paraphrase-MiniLM-L3-v2`](https://huggingface.co/sentence-transformers/paraphrase-MiniLM-L3-v2) for semantic retrieval.

---

## 🚀 Features

| Module | Description |
|--------|--------------|
| 🧩 **Intent Classification** | Determines query intent (medical fact, diagnosis, advice, or emotion) via LLM or rule-based fallback. |
| 🪄 **Query Rewriting** | Reformulates user queries into canonical, knowledge-searchable forms. |
| 🔍 **Retrieval (RAG)** | Retrieves similar QA pairs from the local MedQuAD dataset using SBERT embeddings. |
| 💬 **Answer Generation** | Synthesizes context-aware, medically compliant answers via Qwen2-0.5B-Instruct. |
| 🛡 **Safety & Urgency Detection** | Scans for emergency symptoms (e.g., chest pain, syncope, stroke) and injects triage highlights. |
| 🌐 **Offline-First Design** | Works fully offline with optional web retrieval (DuckDuckGo API toggle). |
| 📊 **Streamlit UI (5 Tabs)** | Displays detected intent, rewritten query, safety hits, raw prompts, and exportable JSON results. |

---

## 🧱 Directory Structure

```
MedQueryFlow/
│
├─ app.py                  # Streamlit interface entry point
├─ core/
│   └─ pipeline.py         # Main pipeline orchestration logic
├─ modules/
│   ├─ llm_client.py       # Qwen2 + SBERT model interface
│   └─ web_search.py       # (optional) DuckDuckGo retriever
│
├─ config.yaml             # Central configuration file
├─ prompts/
│   ├─ intent_prompt.txt
│   ├─ rewrite_prompt.txt
│   └─ answer_prompt.txt
│
├─ data/
│   ├─ MedQuAD/            # Original XML dataset (manually downloaded)
│   ├─ medquad_subset.json # Generated QA corpus after conversion
│   └─ emergency_terms.json
│
├─ models/
│   ├─ paraphrase-MiniLM-L3-v2/
│   └─ qwen2-0.5b-instruct/
│
├─ scripts/
│   ├─ download_model.py   # Auto-download Qwen2-0.5B-Instruct
│   ├─ download_sbert.py   # Auto-download paraphrase-MiniLM-L3-v2
│   └─ convert_medquad.py  # Convert MedQuAD XML → JSON
│
└─ requirements.txt
```

---

## ⚙️ Configuration (`config.yaml`)

```yaml
models:
  sbert_path: models/paraphrase-MiniLM-L3-v2
  qwen_path: models/qwen2-0.5b-instruct
  offline: true

retrieval:
  local_top_k: 5
  use_web: false

generation:
  max_new_tokens: 256
  allow_sampling: false

safety:
  source_file: data/emergency_terms.json  # 👈 dynamically loaded

prompts:
  intent_prompt: prompts/intent_prompt.txt
  rewrite_prompt: prompts/rewrite_prompt.txt
  answer_prompt: prompts/answer_prompt.txt

intent:
  use_llm: true

logging:
  level: INFO
```

- **Models** — local paths to Qwen2 (LLM) and SBERT (retriever)  
- **Retrieval** — top-K candidates and online/offline switch  
- **Safety** — urgent keyword detection for triage prompts (auto loaded from JSON)  
- **Prompts** — define templates for intent, rewrite, and answer generation  

---

## 🧩 Model Setup

### 1️⃣ Qwen2-0.5B-Instruct
> LLM used for intent detection, rewriting, and answer generation.

```bash
python scripts/download_model.py --name Qwen2-0.5B-Instruct
```
➡️ Creates:  
`models/qwen2-0.5b-instruct/`

Model page: [https://huggingface.co/Qwen/Qwen2-0.5B-Instruct](https://huggingface.co/Qwen/Qwen2-0.5B-Instruct)

---

### 2️⃣ paraphrase-MiniLM-L3-v2
> SBERT model used for embedding and semantic retrieval.

```bash
python scripts/download_sbert.py --target models/paraphrase-MiniLM-L3-v2
```
➡️ Creates:  
`models/paraphrase-MiniLM-L3-v2/`

Model page: [https://huggingface.co/sentence-transformers/paraphrase-MiniLM-L3-v2](https://huggingface.co/sentence-transformers/paraphrase-MiniLM-L3-v2)

---

## 📚 Dataset Preparation

1️⃣ Download **MedQuAD XML** dataset manually:  
👉 [https://github.com/abachaa/MedQuAD](https://github.com/abachaa/MedQuAD)

2️⃣ Place it under:
```
data/MedQuAD/
```

3️⃣ Convert XML → JSON:
```bash
python scripts/convert_medquad.py
```

Generates:
```
data/medquad_subset.json
```

---

## 🧠 Run the App

### Install dependencies
```bash
pip install -r requirements.txt
```

### Launch Streamlit UI
```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🩹 Safety & Compliance Layer

- Emergency terms are defined in `data/emergency_terms.json`.
- Each user query is scanned for urgent/caution keywords.
- If detected, the model automatically prepends a triage warning message.

Example:
```
User: I have sudden chest pain and dizziness.
→ ⚠️ These symptoms may indicate an emergency. Seek immediate medical care.
```

---

## 🧪 Local Debug & Logs

Log level is set in `config.yaml`:

```yaml
logging:
  level: INFO
```

To enable debug output:
```yaml
logging:
  level: DEBUG
```

---

## 🧰 Offline-First Design

When `models.offline: true`:
- All retrievals and generations run locally.
- No external API calls are made.
- Web search (DuckDuckGo) can be re-enabled via `retrieval.use_web: true`.

---

## 📦 Notes

- Models and datasets are stored locally for reproducibility.
- Large model folders should be added to `.gitignore`.
- Compatible with CPU or GPU (CUDA/ROCm supported).
- Recommended Python ≥ 3.9, tested on 3.13 (Anaconda env `medquery`).

---

## 🧾 Citation (optional)

If you use this framework in academic work, please cite:

> **MedQueryFlow: A Prompt-Orchestrated Medical QA Pipeline.**  
> Inspired by the MedQuAD dataset and Sentence-Transformers embedding models.
