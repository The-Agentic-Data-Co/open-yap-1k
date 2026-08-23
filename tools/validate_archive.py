"""Check a delivered Open Yap 1K archive against the published schemas.

Run this on a corpus you have received, before you build a pipeline on it. It
validates every JSON file against `data/schema/`, checks the folder layout, and
reports what is missing rather than stopping at the first problem.

It does NOT open the audio. Nothing here needs the recordings.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = REPO_ROOT / "data" / "schema"

# Which schema governs which filename. Two-speaker deliveries only, which is
# every Open Yap 1K archive. The role-named `agent_*` / `caller_*` files that
# scripted deliveries ship carry a different meta shape, and the schemas here
# would reject every one of them; they are reported as uncovered instead.
SPEAKER_STEMS = ("speaker_a", "speaker_b")


def load(name: str) -> dict:
    return json.loads((SCHEMA_DIR / name).read_text())


def schema_for(path: Path) -> tuple[str, dict] | None:
    name = path.name
    if name == "manifest.json":
        return "manifest", load("manifest.schema.json")
    if name == "meta.json":
        return "conversation", load("conversation.schema.json")
    for stem in SPEAKER_STEMS:
        if name == f"{stem}_meta.json":
            return "speaker", load("speaker.schema.json")
        if name == f"{stem}_transcript.json":
            return "transcript", load("transcript.schema.json")
        if name == f"{stem}_dnsmos.json":
            return "dnsmos", load("dnsmos.schema.json")
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path, help="an extracted archive directory")
    args = parser.parse_args()

    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        print("jsonschema is missing. Run: pip install -r tools/requirements.txt")
        return 1

    root = args.archive
    if not root.is_dir():
        print(f"{root} is not a directory")
        return 1

    conversations = root / "conversations"
    if not conversations.is_dir():
        print(f"expected {conversations} — is this the extracted archive root?")
        return 1

    problems: list[str] = []
    checked = 0

    for path in sorted(conversations.rglob("*.json")):
        match = schema_for(path)
        if match is None:
            problems.append(f"{path.relative_to(root)}: no schema covers this filename")
            continue
        _, schema = match
        try:
            document = json.loads(path.read_text())
        except json.JSONDecodeError as err:
            problems.append(f"{path.relative_to(root)}: not valid JSON ({err})")
            continue
        for error in Draft202012Validator(schema).iter_errors(document):
            where = ".".join(str(p) for p in error.absolute_path) or "(root)"
            problems.append(f"{path.relative_to(root)}: {where}: {error.message}")
        checked += 1

    # A dnsmos file is ABSENT when a track was not scored, which is valid. A
    # missing meta or transcript is not.
    required = (
        "meta.json",
        *(f"{stem}_meta.json" for stem in SPEAKER_STEMS),
        *(f"{stem}_transcript.json" for stem in SPEAKER_STEMS),
    )
    for folder in sorted(p for p in conversations.iterdir() if p.is_dir()):
        for name in required:
            if not (folder / name).exists():
                problems.append(f"{folder.relative_to(root)}: missing {name}")

    print(f"checked {checked} JSON files in {root}")
    if not problems:
        print("no problems found")
        return 0

    print(f"\n{len(problems)} problems:\n")
    for problem in problems:
        print(f"  {problem}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
