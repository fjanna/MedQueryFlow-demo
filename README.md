# 🧠 MedQueryFlow-demo · Offline Medical RAG with Tiny LLM

A **prompt-orchestrated medical QA pipeline** that runs **fully offline** with compact open-source models.  
It demonstrates an end-to-end flow:

**Intent → Query Rewrites → Local RAG Retrieval → Answer Synthesis → Safety Highlight**

> Built for quick review of my NLP technical skills; mirrors the production ideas I use at work (intent routing, promptable rewrites, lightweight RAG, and safety gates).

---

## ✨ Features

- **Dual Intent Classifier**: rule-based baseline + LLM scoring (Qwen2-0.5B-Instruct)
- **Prompt-driven Query Rewriter**: swap prompts via `prompts/*.txt`
- **Local RAG**: semantic search over a small MedQuAD subset using **paraphrase-MiniLM-L3-v2**
- **Answer Generator + Safety Layer**: merges `config.yaml.safety` with `data/emergency_terms.json`; triggers ⚠️ highlights on urgent terms
- **Streamlit UI**: one-click demo, export full JSON payload
- **Config-first**: everything toggled via `config.yaml`

---

## 🖼 Demo (Screenshots)

Place screenshots in the `assets/` directory — recommended 2–3 images:

1. `assets/ui-home.png` — Homepage and sample input  
2. `assets/ui-run.png` — Results: Intent / Rewrite / Retrieval / Answer / Safety  
3. `assets/ui-config.png` — Configuration and model download script (optional)

```text
repo/
├─ assets/
│  ├─ ui-home.png
│  ├─ ui-run.png
│  └─ ui-config.png
```

![](assets/ui-home.png)
![](assets/ui-run.png)

---

## 🚀 Quickstart

### 1️⃣ Create environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt
# Recommended (verified) versions:
#   torch==2.3.*
#   transformers==4.44.*
#   sentence-transformers==2.6.*
#   numpy>=1.24
#   pyyaml>=6.0
#   streamlit>=1.36
#   ddgs>=1.0.7   # Only needed if enabling web retrieval
```

---

### 2️⃣ Download models (offline)

```bash
# Qwen2-0.5B-Instruct -> models/qwen2-0.5b-instruct
python scripts/download_model.py

# Sentence-BERT -> models/paraphrase-MiniLM-L3-v2
python scripts/download_sbert.py
```

> You may also manually place Hugging Face model folders under `models/` with the same names.

---

### 3️⃣ (Optional) Prepare MedQuAD subset

A small subset is already included; to regenerate:

```bash
python scripts/convert_medquad_xml_to_json.py
# Output: data/medquad_subset.json
```

---

### 4️⃣ Run the app

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`, input a medical question, and click **Run**.

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
  web_top_k: 5

generation:
  max_new_tokens: 256
  allow_sampling: false

safety:
  urgent_keywords: ["chest pain", "shortness of breath", "syncope", "stroke"]
  urgent_highlight: "⚠️ These symptoms may indicate an emergency. Seek immediate medical care."
  caution_highlight: "⚠️ Concerning features present. Please consult a clinician soon."

prompts:
  intent_prompt:  prompts/intent_prompt.txt
  rewrite_prompt: prompts/rewrite_prompt.txt
  answer_prompt:  prompts/answer_prompt.txt

intent:
  use_llm: true   # true: use LLM scoring; false: rule-based
```

- **Custom emergency terms**: extend `data/emergency_terms.json` — entries will merge automatically.  
- **Prompt hot-swap**: simply replace files in `prompts/` for A/B testing.

---

## 🧩 How It Works

1. **Intent**  
   - Rule-based (`modules/intent_classifier.py`) or LLM-based (`modules/intent_llm_classifier.py`)  
   - Note: `rules` return `"diagnostic"`, `LLM` returns `"diagnosis_request"`. The pipeline maps these internally.

2. **Rewrites**  
   - Uses `prompts/rewrite_prompt.txt` to generate 2–3 search-oriented rewrites.  
   - If prompt missing, falls back to simple expansions.

3. **RAG Retrieval**  
   - Embeds `data/medquad_subset.json` using **paraphrase-MiniLM-L3-v2** for cosine-similarity search.  
   - Missing dependencies fallback to keyword-based top-k (see console log).

4. **Answer + Safety**  
   - Generates an answer using `prompts/answer_prompt.txt`.  
   - Matches against `safety` keywords and `emergency_terms.json`.  
   - UI highlights ⚠️ urgent cases with standardized messages.  
   - Supports one-click **Export JSON** (intent, rewrites, retrieval, final answer, safety triggers).

---

## 🖥️ Performance Tips

- The demo is intentionally optimized for **simplicity and portability** — all components run on CPU by default.
- For faster inference, you may run on GPU with smaller precision:
  ```python
  model = AutoModelForCausalLM.from_pretrained(path, torch_dtype=torch.float16).to("cuda")
  ```
- Typical improvement: 5–10× faster generation, 50% less memory use.

---

### ⚙️ Device & Precision Note

> 💡 **Note:**  
> The current demo runs on CPU by default for simplicity and portability.  
> On systems with GPU, users can manually add `.to(device)` and specify `torch_dtype=torch.float16`  
> when loading the model for faster inference and lower memory usage.  
> This optimization is intentionally left out in the default version to ensure that  
> reviewers can run the demo smoothly on any machine without setup issues.

---

## 🧪 Repository Layout

```
core/            # LLM client & pipeline
modules/         # intent / rewrite / retrieval / answer
prompts/         # prompt templates (hot-swappable)
data/            # medquad subset + emergency_terms.json
models/          # local Hugging Face models (ignored by git)
scripts/         # model download & data conversion
app.py           # Streamlit UI
config.yaml      # all knobs here
```

---

## 📄 Data & License

- **MedQuAD subset**: derived for demo only.  
  Original dataset: [MedQuAD – CC BY 4.0](https://catalog.data.gov/dataset/medquad-dataset-of-medical-question-answer-pairs)  
  (note: several MedlinePlus subsets were later removed upstream).  
  Please use this subset **only for academic demonstration and non-commercial research**.

- **Code License:** MIT (see `LICENSE`)

> ⚠️ *Medical Disclaimer:* This demo does not provide medical advice.  
> For emergencies, contact local emergency services immediately.

---

## ❓FAQ

**Q:** Can it run fully offline?  
**A:** Yes — by default, `use_web=false`. Models and data are local.

**Q:** Easiest way for professors to test?  
**A:**  
`pip install -r requirements.txt` → run the two download scripts → `streamlit run app.py`.

**Q:** Why does it sometimes show “please seek medical attention”?  
**A:** Triggered by `safety.urgent_keywords` or entries in `data/emergency_terms.json`.

**Q:** How to use my own knowledge base?  
**A:** Replace `data/medquad_subset.json` with your own JSON (fields: `id`, `title`, `text`, `url`).

---

## 🙌 Acknowledgements

- Qwen2 (Alibaba Cloud)
- sentence-transformers
- MedQuAD dataset authors and maintainers

---

## 🧾 Citation

If this demo is referenced or used in presentations:

```
Feng, Jie. "MedQueryFlow-demo: Prompt-Orchestrated Offline Medical QA with Tiny LLMs." 2025.
```
