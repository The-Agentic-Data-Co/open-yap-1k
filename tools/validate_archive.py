"""Check a delivered Open Yap 1K archive against the published schemas.

Run this on a corpus you have received, before you build a pipeline on it. It
validates every JSON file against `data/schema/`, checks the folder layout, and
reports what is missing rather than stopping at the first problem.

Version 4 archives also require matching SHA-256 hashes for every delivered file.
This checks file identity, not the accuracy of the audio measurements.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
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
        if name == f"{stem}_signal_metrics.json":
            return "signal metrics", load("signal-metrics.schema.json")
    return None


def signal_metrics_problems(document: object) -> list[str]:
    if not isinstance(document, dict):
        return []
    count = document.get("measurement_count")
    if not isinstance(count, int) or isinstance(count, bool):
        return []

    problems = []
    for field in ("snr_db", "noise_floor_dbfs", "clipping_pct"):
        values = document.get(field)
        if isinstance(values, list) and len(values) != count:
            problems.append(
                f"measurement_count is {count} but {field} has {len(values)} entries"
            )

    duration = document.get("duration_seconds")
    step = document.get("step_seconds")
    numbers = (int, float)
    if (
        isinstance(duration, numbers)
        and not isinstance(duration, bool)
        and isinstance(step, numbers)
        and not isinstance(step, bool)
        and math.isfinite(duration)
        and math.isfinite(step)
        and duration > 0
        and step > 0
    ):
        expected = math.ceil(duration / step)
        if count != expected:
            problems.append(
                f"measurement_count is {count} but duration_seconds requires {expected} entries"
            )
    return problems


def verification_problems(root: Path) -> list[str]:
    record = root / "conversations" / "verification.json"
    dataset = json.loads((root / "conversations" / "manifest.json").read_text())
    if not isinstance(dataset, dict):
        return ["dataset manifest is not an object"]
    measurement_version = dataset.get("measurement_schema_version", 0)
    if not isinstance(measurement_version, int) or isinstance(measurement_version, bool) or measurement_version < 0:
        return ["invalid measurement_schema_version in dataset manifest"]
    if not record.exists():
        needs_proof = dataset.get("dataset_version") == "2.0" or measurement_version >= 4
        return ["missing conversations/verification.json"] if needs_proof else []
    proof = json.loads(record.read_text())
    if not isinstance(proof, dict):
        return ["verification record is not an object"]
    if proof.get("version") != 1 or proof.get("measurement_schema_version") != dataset.get("measurement_schema_version"):
        return ["verification version differs from the dataset manifest"]
    files = proof.get("files")
    if not isinstance(files, dict) or not files:
        return ["verification record has no files"]
    problems = []
    for name, expected in files.items():
        if not isinstance(expected, dict):
            problems.append(f"invalid verification entry: {name}")
            continue
        sha256 = expected.get("sha256")
        byte_length = expected.get("byteLength")
        if (
            not isinstance(sha256, str)
            or not re.fullmatch(r"[0-9a-f]{64}", sha256)
            or not isinstance(byte_length, int)
            or isinstance(byte_length, bool)
            or byte_length < 0
        ):
            problems.append(f"invalid verification entry: {name}")
            continue
        relative = Path(name)
        filename = root / relative
        if relative.is_absolute() or ".." in relative.parts or not filename.resolve().is_relative_to(root.resolve()):
            problems.append(f"invalid verification path: {name}")
            continue
        if not filename.is_file() or filename.is_symlink():
            problems.append(f"missing or linked file: {name}")
            continue
        digest = hashlib.sha256()
        length = 0
        with filename.open("rb") as source:
            while block := source.read(1024 * 1024):
                digest.update(block)
                length += len(block)
        if digest.hexdigest() != sha256 or length != byte_length:
            problems.append(f"changed file: {name}")
    for filename in (root / "conversations").rglob("*"):
        if filename.is_file() and filename != record and filename.relative_to(root).as_posix() not in files:
            problems.append(f"unverified file: {filename.relative_to(root)}")
    return problems


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

    try:
        problems.extend(verification_problems(root))
    except (OSError, ValueError, TypeError) as error:
        problems.append(f"invalid verification record: {error}")

    for path in sorted(conversations.rglob("*.json")):
        if path == conversations / "verification.json":
            continue
        match = schema_for(path)
        if match is None:
            problems.append(f"{path.relative_to(root)}: no schema covers this filename")
            continue
        kind, schema = match
        try:
            document = json.loads(path.read_text())
        except json.JSONDecodeError as err:
            problems.append(f"{path.relative_to(root)}: not valid JSON ({err})")
            continue
        for error in Draft202012Validator(schema).iter_errors(document):
            where = ".".join(str(p) for p in error.absolute_path) or "(root)"
            problems.append(f"{path.relative_to(root)}: {where}: {error.message}")
        if kind == "signal metrics":
            for problem in signal_metrics_problems(document):
                problems.append(f"{path.relative_to(root)}: (root): {problem}")
        checked += 1

    # Measurement files are absent when a track was not measured, which is
    # valid. A missing meta or transcript is not.
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
