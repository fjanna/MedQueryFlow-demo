# MedQueryFlow · Final Proper (RAG + Qwen2, Offline)

This package matches the reviewed design:
- LLM-based Intent (with confidence) / Query Rewrite / Answer generation
- Emergency terms in `data/emergency_terms.json` (merged with config fallback)
- 5-tab Streamlit UI with safety hits, intent confidence, raw prompts, and Export JSON
- MedQuAD subset: place your `data/medquad_subset.json` (this repo ships a placeholder `[]`)

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Configure
- `config.yaml` for model paths and toggles (intent.use_llm)
- `prompts/*.txt` for behavior control
- `data/emergency_terms.json` to maintain safety keywords
- `data/medquad_subset.json` as RAG corpus (fallback stub if missing)
