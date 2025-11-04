"""Download SBERT 'paraphrase-MiniLM-L3-v2' locally for offline inference."""
from __future__ import annotations
import argparse
from pathlib import Path
from huggingface_hub import snapshot_download

def download_model(target_dir: str, repo_id: str = "sentence-transformers/paraphrase-MiniLM-L3-v2") -> None:
    path = Path(target_dir)
    path.mkdir(parents=True, exist_ok=True)
    snapshot_download(repo_id=repo_id, local_dir=path, local_dir_use_symlinks=False)
    print(f"Model downloaded to {path}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Download paraphrase-MiniLM-L3-v2 model")
    parser.add_argument("--target", default="models/paraphrase-MiniLM-L3-v2", help="Target directory")
    parser.add_argument("--repo", default="sentence-transformers/paraphrase-MiniLM-L3-v2", help="Hugging Face repo id")
    args = parser.parse_args()
    download_model(args.target, args.repo)

if __name__ == "__main__":
    main()
