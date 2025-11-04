# MedQueryFlow Demo

This is a lightweight, locally runnable demo built with minimal model dependencies.

## Key Components

- **Intent Classification**  
  Categorizes queries into `fact`, `diagnostic`, `advisory`, or `emotion`.  
  Each label routes the query to a suitable retrieval path (e.g., professional medical knowledge base vs. in-platform posts).

- **Query Rewriting**  
  Decomposes biased or ill-formed queries into neutral *sub-queries* to expand recall and reduce misleading assumptions.  
  Example:  
  > “Cervical spondylosis makes me dizzy and vomit” →  
  > “Symptoms of cervical spondylosis” + “Causes of dizziness and vomiting”

- **Safety Controls**  
  Detects urgent or critical symptoms and inserts emergency reminders automatically.

See `data/data_readme.md` for the local knowledge base setup, and `models/models_readme.md` for the model setup.

## Notes

This project is for demonstration only.  
