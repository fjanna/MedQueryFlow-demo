# MedQueryFlow Demo

This is a lightweight, locally runnable demo built with minimal model dependencies.

## Key Components

- **Intent Classification**  
  evaluating the conditional log-likelihood of each candidate label given a query, tokenizing and concatenating the prompt–label pairs, runs inference under torch.no_grad(), accumulates per-token log-probabilities using F.log_softmax, and applies a final softmax normalization to produce interpretable intent probabilities.

- **Query Rewriting**  
  prompt-driven, with structured text cleaning and defensive fallback strategies to ensure reliable output under various runtime conditions.

- **Safety Controls**  
  Detects urgent or critical symptoms and inserts emergency reminders automatically.

## Quick Start：
See `data/data_readme.md` for the local knowledge base setup, and `models/models_readme.md` for the model setup.
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Notes

This project is for demonstration only.  
