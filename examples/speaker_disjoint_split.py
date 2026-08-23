"""Split the corpus by speaker, not by conversation.

The trap this avoids: a speaker appears in more than one conversation. Split at
random and the same voice lands in both train and test, so your model is scored
on voices it has already heard and every number comes out optimistic.

Speakers, not conversations, are the independent unit. Run this against an
extracted archive.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def bucket(speaker_id: str, buckets: int = 100) -> int:
    """Stable across runs and machines: a hash, not `random`. Re-splitting the
    same corpus twice must give the same answer or a held-out set is not held
    out."""
    digest = hashlib.sha256(speaker_id.encode()).hexdigest()
    return int(digest[:8], 16) % buckets


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    # Named for what it holds out. 10% of SPEAKERS is far fewer conversations:
    # a conversation reaches the test set only when BOTH its speakers do.
    parser.add_argument("--test-speaker-percent", type=int, default=10)
    args = parser.parse_args()

    conversations = args.archive / "conversations"
    metas = [
        json.loads(p.read_text())
        for p in sorted(conversations.glob("conv_*/meta.json"))
    ]

    # A conversation has two speakers. If EITHER is held out, the whole
    # conversation is held out — otherwise the test voice appears in training
    # through its partner's file.
    train, test, straddling = [], [], 0
    for meta in metas:
        sides = [meta["speaker_a_id"], meta["speaker_b_id"]]
        held = [s for s in sides if bucket(s) < args.test_speaker_percent]
        if len(held) == len(sides):
            test.append(meta["conversation_id"])
        elif held:
            straddling += 1
        else:
            train.append(meta["conversation_id"])

    share = len(test) / len(metas) if metas else 0.0
    print(f"train {len(train)}  test {len(test)} ({share:.1%} of conversations)  dropped {straddling}")
    print("\nDropped conversations have one speaker on each side. Keeping them")
    print("in either split would leak a voice across the boundary.")

    Path("train.txt").write_text("\n".join(train) + "\n")
    Path("test.txt").write_text("\n".join(test) + "\n")


if __name__ == "__main__":
    main()
