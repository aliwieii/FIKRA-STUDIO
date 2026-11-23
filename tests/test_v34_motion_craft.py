import json
import unittest
from pathlib import Path

from fikra_v3 import __version__, repo_root
from fikra_v3.__main__ import main as cli_main
from fikra_v3.motion_craft import (
    check_motion_craft_compliance,
    list_narrative_archetypes,
    list_reel_effects,
    load_motion_craft_catalog,
)
from fikra_v3.project_state import create_project_state
from fikra_v3.prompt_compiler import compile_v34_production_prompt
from fikra_v3.prompt_compiler import assert_no_music_leak


class TestV34MotionCraft(unittest.TestCase):
    def setUp(self):
        self.root = repo_root()

    def test_version_and_catalog_counts(self):
        self.assertEqual(__version__, "3.4.0")
        cat = load_motion_craft_catalog(self.root)
        self.assertEqual(len(cat["anti_slide_motion_rules"]), 6)
        self.assertEqual(len(cat["narrative_archetypes"]), 8)
        self.assertEqual(len(cat["reel_effects_catalog"]), 12)
        # Ensure zero music leaks anywhere in the V3.4 catalog text
        raw = json.dumps(cat, ensure_ascii=False)
        for arch in cat["narrative_archetypes"]:
            self.assertTrue(assert_no_music_leak(arch["audio_direction"])["pass"])
            self.assertTrue(assert_no_music_leak(arch["visual_grammar"])["pass"])
        self.assertIn("NO BACKGROUND MUSIC", raw)

    def test_archetype_mode_filtering(self):
        fikra_arch = list_narrative_archetypes(mode="FIKRA_CHANNEL_MODE", root=self.root)
        slugs = {a["slug"] for a in fikra_arch}
        self.assertIn("VOX_SCRAPBOOK_COLLAGE", slugs)
        self.assertNotIn("SHOTCRAFT_APP_PRODUCT_DEMO", slugs)
        self.assertEqual(len(list_reel_effects(self.root)), 12)

    def test_motion_craft_compliance_catches_antipatterns(self):
        bad_code = """
        const jitter = Math.random();
        const style = { transition: 'all 0.3s ease', fontSize: 18 };
        // add background music
        """
        rep = check_motion_craft_compliance(bad_code, engine="remotion")
        self.assertFalse(rep["pass"])
        rule_ids = {v["rule_id"] for v in rep["violations"]}
        self.assertIn("MC-02", rule_ids)
        self.assertIn("MC-03", rule_ids)
        self.assertIn("MC-06", rule_ids)

        good_code = """
        const frame = useCurrentFrame();
        const scale = spring({ frame, fps: 30, config: { damping: 14 } });
        const titleStyle = { fontSize: 48 };
        """
        ok = check_motion_craft_compliance(good_code, engine="remotion")
        self.assertTrue(ok["pass"], msg=ok)

    def test_compile_v34_production_prompt_across_modes(self):
        for mode in ("UNIVERSAL_VIDEO_MODE", "FIKRA_CHANNEL_MODE", "QURAN_MODE"):
            st = create_project_state("PRJ-V34-01", "تجربة الإصدار 3.4", mode=mode)
            res = compile_v34_production_prompt(
                st,
                root=self.root,
                archetype_slug="VOX_SCRAPBOOK_COLLAGE",
                reel_effects=["split-headline", "word-captions", "kinetic-callout"],
            )
            self.assertTrue(res["isolation_clean"])
            self.assertTrue(res["music_audit"]["pass"])
            self.assertIn("V3.4 Motion Craft", res["prompt_markdown"])
            self.assertIn("MC-01 (Video, Not Slides)", res["prompt_markdown"])
            self.assertIn("VOX_SCRAPBOOK_COLLAGE", res["prompt_markdown"])

    def test_cli_presets_and_craft_check(self):
        rc1 = cli_main(["presets", "--mode", "UNIVERSAL_VIDEO_MODE"])
        self.assertEqual(rc1, 0)
        rc2 = cli_main(["craft-check", "--text", "const f = useCurrentFrame(); const fontSize = 42;", "--engine", "remotion"])
        self.assertEqual(rc2, 0)


if __name__ == "__main__":
    unittest.main()
