import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "registry/capabilities.json").read_text())


class UpstreamRegistry(unittest.TestCase):
    def test_source_evidence_and_modes(self):
        rows = CATALOG["capabilities"]
        self.assertEqual(len(rows), len({r["id"] for r in rows}))
        shape = json.loads((ROOT / "schemas/capabilities.schema.json").read_text())
        fields = shape["properties"]["capabilities"]["items"]["properties"]
        for row in rows:
            with self.subTest(capability=row["id"]):
                self.assertEqual(set(fields), set(row))
                for key, rules in fields.items():
                    if "enum" in rules:
                        self.assertIn(row[key], rules["enum"])
                    if "pattern" in rules and row[key] is not None:
                        self.assertTrue(re.fullmatch(rules["pattern"], row[key]))
                prefix = f"https://github.com/{row['published_repository']}/blob/{row['revision']}/"
                self.assertTrue(row["source_url"].startswith(prefix))
                self.assertEqual(row["license_url"], None if row["license"] == "NOASSERTION" else prefix + "LICENSE")
                self.assertEqual(row["verification"] == "local-fixture-passed", row["mode"] == "optional-local-probe")
                self.assertGreater(len(row["dependencies"]), 0)

    def test_exercised_optional_contracts(self):
        exercised = {r["id"] for r in CATALOG["capabilities"] if r["mode"] == "optional-local-probe"}
        self.assertEqual(exercised, {"commercial-workflow", "model-economics"})
