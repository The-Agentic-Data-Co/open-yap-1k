import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from validate_archive import signal_metrics_problems, verification_problems


class VerificationValidationTest(unittest.TestCase):
    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        conversations = self.root / "conversations"
        conversations.mkdir()
        self.manifest = conversations / "manifest.json"
        self.manifest.write_text(json.dumps({
            "dataset_version": "2.0", "measurement_schema_version": 4,
        }))
        self.record = conversations / "verification.json"
        contents = self.manifest.read_bytes()
        self.entry = {
            "sha256": hashlib.sha256(contents).hexdigest(), "byteLength": len(contents),
        }

    def write_proof(self, files: dict) -> None:
        self.record.write_text(json.dumps({
            "version": 1, "measurement_schema_version": 4, "files": files,
        }))

    def test_accepts_matching_file_hashes(self) -> None:
        self.write_proof({"conversations/manifest.json": self.entry})
        self.assertEqual(verification_problems(self.root), [])

    def test_reports_changed_and_unverified_files(self) -> None:
        self.write_proof({"conversations/manifest.json": self.entry})
        self.manifest.write_text(self.manifest.read_text() + "\n")
        (self.root / "conversations" / "extra.json").write_text("{}")
        self.assertEqual(verification_problems(self.root), [
            "changed file: conversations/manifest.json",
            "unverified file: conversations/extra.json",
        ])

    def test_requires_proof_for_current_archives(self) -> None:
        self.assertEqual(verification_problems(self.root), ["missing conversations/verification.json"])

    def test_accepts_legacy_archives_without_proof(self) -> None:
        self.manifest.write_text(json.dumps({"dataset_version": "1.0"}))
        self.assertEqual(verification_problems(self.root), [])

    def test_reports_non_object_manifest_and_proof(self) -> None:
        for value in (None, [], "invalid", 1):
            with self.subTest(value=value):
                original = self.manifest.read_text()
                self.manifest.write_text(json.dumps(value))
                self.assertEqual(verification_problems(self.root), ["dataset manifest is not an object"])
                self.manifest.write_text(original)
                self.record.write_text(json.dumps(value))
                self.assertEqual(verification_problems(self.root), ["verification record is not an object"])

    def test_reports_invalid_measurement_versions(self) -> None:
        for version in (None, "4", True, -1):
            with self.subTest(version=version):
                self.manifest.write_text(json.dumps({"measurement_schema_version": version}))
                self.assertEqual(verification_problems(self.root), [
                    "invalid measurement_schema_version in dataset manifest",
                ])

    def test_reports_malformed_entries_and_continues(self) -> None:
        entries = [None, [], "invalid", 1, {},
                   {**self.entry, "sha256": "invalid"},
                   *({**self.entry, "byteLength": value} for value in (None, True, -1, 1.5))]
        for entry in entries:
            with self.subTest(entry=entry):
                self.write_proof({
                    "conversations/manifest.json": entry,
                    "conversations/missing.json": self.entry,
                })
                self.assertEqual(verification_problems(self.root), [
                    "invalid verification entry: conversations/manifest.json",
                    "missing or linked file: conversations/missing.json",
                ])


class SignalMetricsValidationTest(unittest.TestCase):
    def test_accepts_aligned_series(self) -> None:
        document = {
            "duration_seconds": 2,
            "step_seconds": 1,
            "measurement_count": 2,
            "snr_db": [20, None],
            "noise_floor_dbfs": [-50, -51],
            "clipping_pct": [0, 0.1],
        }

        self.assertEqual(signal_metrics_problems(document), [])

    def test_rejects_a_metric_array_with_the_wrong_length(self) -> None:
        document = {
            "duration_seconds": 2,
            "step_seconds": 1,
            "measurement_count": 2,
            "snr_db": [20],
            "noise_floor_dbfs": [-50, -51],
            "clipping_pct": [0, 0.1],
        }

        self.assertEqual(
            signal_metrics_problems(document),
            ["measurement_count is 2 but snr_db has 1 entries"],
        )

    def test_rejects_a_count_that_does_not_cover_the_duration(self) -> None:
        document = {
            "duration_seconds": 2.5,
            "step_seconds": 1,
            "measurement_count": 2,
            "snr_db": [20, 21],
            "noise_floor_dbfs": [-50, -51],
            "clipping_pct": [0, 0.1],
        }

        self.assertEqual(
            signal_metrics_problems(document),
            ["measurement_count is 2 but duration_seconds requires 3 entries"],
        )


if __name__ == "__main__":
    unittest.main()
