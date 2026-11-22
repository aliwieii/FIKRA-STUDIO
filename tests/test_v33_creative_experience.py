import json
import unittest
from pathlib import Path

from fikra_v3 import MODES, repo_root
from fikra_v3.approval_guard import ApprovalLockedError, lock_decision
from fikra_v3.context_loader import load_context
from fikra_v3.project_state import create_project_state
from fikra_v3.prompt_compiler import assert_no_music_leak, compile_v33_production_prompt
from fikra_v3.regression_guard import run_regression_checks
from fikra_v3.style_recommender import recommend_styles_v33
from fikra_v3.visual_intelligence import build_style_bible, verify_reference_access


class TestV33CreativeExperience(unittest.TestCase):
    # A, B, C, M — All 9 modes work, NO MUSIC in any mode, Universal isolated from FIKRA VOICE 01
    def test_all_nine_modes_no_music_and_isolation(self):
        for m in MODES:
            ctx = load_context(mode=m)
            self.assertTrue(ctx["isolation_verified"])
            st = create_project_state(f"M-{m[:4]}", f"Test {m}", mode=m)
            lock_decision(st, "idea", "فكرة اختبارية واضحة")
            lock_decision(st, "script", "نص عربي قصير وواضح.")
            lock_decision(st, "style", "STY-003")
            compiled = compile_v33_production_prompt(st)
            self.assertTrue(compiled["music_audit"]["pass"])
            self.assertIn("NO BACKGROUND MUSIC", compiled["prompt_markdown"])
            if m == "UNIVERSAL_VIDEO_MODE":
                self.assertNotIn("FIKRA VOICE 01 —", compiled["prompt_markdown"])
            if m == "QURAN_MODE":
                self.assertIn("ZERO SFX", compiled["prompt_markdown"])

    # B/M negative check — assert_no_music_leak MUST fail if music is suggested
    def test_music_leak_detector_catches_violations(self):
        self.assertFalse(assert_no_music_leak("Please add background music to the intro.")["pass"])
        self.assertFalse(assert_no_music_leak("أضف موسيقى خلفية هادئة")["pass"])
        self.assertTrue(assert_no_music_leak("STRICTLY FORBIDDEN: NO BACKGROUND MUSIC. Use subtle SFX only.")["pass"])

    # D & E — 32 styles intact, human-friendly names & truthful Fake 3D labeling
    def test_32_styles_naming_and_fake3d_honesty(self):
        r = repo_root()
        cat = json.loads((r / "03_STYLE_LIBRARY/STYLE_UX_CATALOG_V33.json").read_text(encoding="utf-8"))
        self.assertEqual(cat["total_styles"], 32)
        ids = [s["style_id"] for s in cat["styles"]]
        self.assertEqual(ids[0], "STY-001")
        self.assertEqual(ids[-1], "STY-032")
        s14 = next(s for s in cat["styles"] if s["style_id"] == "STY-014")
        self.assertIn("ليس ثلاثي الأبعاد حقيقيًا", s14["simplified_arabic_name"])

    # F — External gallery metadata valid & ZERO heavy images added inside 03_STYLE_LIBRARY
    def test_external_gallery_links_and_no_heavy_git_images(self):
        r = repo_root()
        gal = json.loads((r / "03_STYLE_LIBRARY/STYLE_EXTERNAL_GALLERY.json").read_text(encoding="utf-8"))
        self.assertEqual(len(gal["items"]), 32)
        self.assertGreaterEqual(gal["verified_count"], 10)
        for item in gal["items"]:
            if item["image_status"] == "VERIFIED_EXTERNAL_IMAGE":
                self.assertTrue(item["image_url"].startswith("https://"))
                self.assertTrue(item["source_url"].startswith("https://"))
                self.assertTrue(item["license"])
        heavy_imgs = [p for p in (r / "03_STYLE_LIBRARY").rglob("*") if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"} and p.stat().st_size > 200_000]
        self.assertEqual(heavy_imgs, [])

    # G, H, I, J, N, O — 3 Real End-to-End Creative Scenarios (Educational 2D, Cartoon Story, Product Ad)
    def test_three_end_to_end_creative_scenarios(self):
        scenarios = [
            ("SCN-EDU-2D", "شرح دورة الماء للأطفال", "UNIVERSAL_VIDEO_MODE", "16:9", "STY-003", "remotion_motion"),
            ("SCN-STORY-2D", "قصة قصيرة عن الأمانة بشخصيات كرتونية", "FIKRA_CHANNEL_MODE", "9:16", "STY-004", "video_gen"),
            ("SCN-PROD-AD", "إعلان إطلاق تطبيق ذكي لإدارة المهام", "UNIVERSAL_VIDEO_MODE", "16:9", "STY-018", "hyperframes"),
        ]
        for pid, topic, mode, ar, sid, tool in scenarios:
            recs = recommend_styles_v33(topic=topic, aspect_ratio=ar, mode=mode, top_k=3)
            self.assertEqual(len(recs["top_choices"]), 3)
            access = verify_reference_access(f"REF-{pid}", media_path=Path("/nonexistent/ref.mp4"))
            self.assertEqual(access["visual_review_status"], "UNVERIFIED")
            bible = build_style_bible(sid, recs["top_choices"][0]["simplified_arabic_name"], sid, access, aspect_ratio=ar)
            self.assertEqual(len(bible["sections"]), 12)
            self.assertIn("NO BACKGROUND MUSIC", bible["sections"]["10_sound_direction"])

            st = create_project_state(pid, topic, mode=mode, aspect_ratio=ar)
            lock_decision(st, "idea", topic)
            lock_decision(st, "script", f"خطاف بصري قوي: {topic} بأسلوب واضح ومختصر.")
            lock_decision(st, "style", sid)
            with self.assertRaises(ApprovalLockedError):
                lock_decision(st, "style", "STY-001" if sid != "STY-001" else "STY-002")

            compiled = compile_v33_production_prompt(st, target_tool=tool)
            self.assertTrue(compiled["prompt_qa_gate"]["pass"])
            self.assertTrue(compiled["music_audit"]["pass"])

    # L — Regression guard passes
    def test_regression_guard_intact(self):
        self.assertTrue(run_regression_checks()["pass"])


if __name__ == "__main__":
    unittest.main()
