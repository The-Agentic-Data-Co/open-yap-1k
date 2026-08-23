"""Stream the Open Yap 1K sample and print what one conversation contains.

Streaming, so nothing is downloaded up front. Swap `streaming=False` if you want
the files on disk.
"""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    from datasets import load_dataset

    info = json.loads((REPO_ROOT / "data" / "release.json").read_text())
    repo = info["sampleLicense"]["huggingFaceRepo"]

    dataset = load_dataset(repo, split="train", streaming=True)
    row = next(iter(dataset))

    print(f"repository: {repo}")
    print(f"keys:       {sorted(row)}")

    # Two speakers, two files, one timeline. There is no mixed track: the
    # separation is the product, and re-mixing them throws it away.
    for key in sorted(k for k in row if k.endswith(("flac", "wav"))):
        audio = row[key]
        seconds = len(audio["array"]) / audio["sampling_rate"]
        print(f"  {key}: {seconds:.1f}s at {audio['sampling_rate']} Hz")


if __name__ == "__main__":
    main()
