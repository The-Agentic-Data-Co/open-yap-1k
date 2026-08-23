"""Download the Open Yap 1K sample from the Hugging Face Hub.

The repository is gated: the dataset page is public, but the files need an
authenticated account that has accepted the terms once. A bare 401 from the
shop window's own tool is worse than no tool, so this checks for a token first
and says exactly what to do.

The full corpus is not here and is not downloadable. Request it at the landing
page printed below.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def release() -> dict:
    return json.loads((REPO_ROOT / "data" / "release.json").read_text())


def main() -> int:
    info = release()
    repo = info["sampleLicense"]["huggingFaceRepo"]

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="open-yap-1k-sample", help="where to put the files")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="resolve the repository and exit without downloading",
    )
    args = parser.parse_args()

    try:
        from huggingface_hub import snapshot_download
        from huggingface_hub.utils import GatedRepoError, HfHubHTTPError
    except ImportError:
        print("huggingface_hub is missing. Run: pip install -r tools/requirements.txt")
        return 1

    if args.dry_run:
        print(f"would download {repo} to {args.out}")
        return 0

    try:
        path = snapshot_download(repo_id=repo, repo_type="dataset", local_dir=args.out)
    except GatedRepoError:
        print(f"{repo} is gated. Two one-time steps:\n")
        print(f"  1. Open https://huggingface.co/datasets/{repo} and accept the terms.")
        print("  2. Run: hf auth login\n")
        print("Then run this again.")
        return 1
    except HfHubHTTPError as err:
        print(f"the Hub refused the request: {err}")
        return 1

    print(f"\ndownloaded the sample to {path}")
    print(f"licence: {info['sampleLicense']['name']}, see LICENSE-SAMPLE.txt")
    print(f"\nthe full corpus is by request at {info['landingUrl']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
