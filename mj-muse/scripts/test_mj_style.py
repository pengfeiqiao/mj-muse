#!/usr/bin/env python3

import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("mj_style.py")
SPEC = importlib.util.spec_from_file_location("mj_style", MODULE_PATH)
assert SPEC and SPEC.loader
MJ = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MJ)


class MidjourneyStyleTests(unittest.TestCase):
    def setUp(self):
        self.catalog = MJ.load_catalog()

    def test_catalog_has_84_unique_styles(self):
        ids = [style["id"] for style in self.catalog["styles"]]
        self.assertEqual(len(ids), 84)
        self.assertEqual(len(set(ids)), 84)

    def test_legacy_alias_resolves_to_mechanism_name(self):
        style = MJ.style_lookup(self.catalog, "ghibli")
        self.assertEqual(style["id"], "hand-painted-pastoral")

    def test_compose_replaces_subject_placeholder(self):
        style = MJ.style_lookup(self.catalog, "mecha-ruin")
        prompt = MJ.compose_prompt("a lunar rover", style)
        self.assertIn("lunar rover", prompt)
        self.assertNotIn("a colossal battle-worn a lunar rover", prompt)
        self.assertNotIn("{subject}", prompt)

    def test_strip_controlled_flags(self):
        clean = MJ.strip_controlled_flags("portrait --v 8.2 --ar 4:5 --style raw")
        self.assertEqual(clean, "portrait")


if __name__ == "__main__":
    unittest.main()
