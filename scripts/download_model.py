"""Download Qwen2-0.5B-Instruct locally for offline inference."""

from __future__ import annotations

import argparse
from pathlib import Path

from huggingface_hub import snapshot_download


def download_model(target_dir: str, repo_id: str = "Qwen/Qwen2-0.5B-Instruct") -> None:
    path = Path(target_dir)
    path.mkdir(parents=True, exist_ok=True)
    snapshot_download(repo_id=repo_id, local_dir=path, local_dir_use_symlinks=False)
    print(f"Model downloaded to {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Download Qwen2-0.5B-Instruct model")
    parser.add_argument("--target", default="models/qwen2-0.5b-instruct", help="Target directory")
    parser.add_argument("--repo", default="Qwen/Qwen2-0.5B-Instruct", help="Hugging Face repo id")
    args = parser.parse_args()
    download_model(args.target, args.repo)


if __name__ == "__main__":
    main()
