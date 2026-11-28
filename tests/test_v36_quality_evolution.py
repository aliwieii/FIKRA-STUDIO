import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from fikra_v3 import MODES, __version__, repo_root
from fikra_v3.arabic_qa import render_arabic_caption_fixture
from fikra_v3.consistency_engine import build_consistency_manifest
from fikra_v3.media_intelligence import analyze_audio_mastering
from fikra_v3.project_state import create_project_state
from fikra_v3.prompt_compiler import assert_no_music_leak, compile_v35_production_prompt
from fikra_v3.quality_scorer import compute_evidence_based_quality_score
from fikra_v3.scene_schema import validate_scene_timeline
from fikra_v3.sfx_synthesizer import synthesize_sfx_wav
from fikra_v3.style_execution import build_executable_style_spec
from fikra_v3.tiktok_retention import evaluate_storytelling_and_retention, quickstart_blueprint
from fikra_v3.visual_quality import evaluate_visual_quality


class TestV36QualityEvolution(unittest.TestCase):
    def setUp(self):
        self.root = repo_root()

    def test_conflict_a_no_music_across_all_nine_modes(self):
        self.assertEqual(__version__, "3.6.0")
        self.assertEqual(len(MODES), 9)
        for mode in MODES:
            st = create_project_state(f"PRJ-{mode[:6]}", "اختبار الوضع", mode=mode)
            res = compile_v35_production_prompt(st, root=self.root)
            self.assertTrue(res["music_audit"]["pass"], msg=f"Music leak in {mode}")
            if mode == "QURAN_MODE":
                self.assertIn("ZERO SFX", res["prompt_markdown"])
        uw = (self.root / "02_WORKFLOWS/UNIVERSAL_VIDEO_WORKFLOW.md").read_text(encoding="utf-8")
        self.assertNotIn("ولا حظر الموسيقى", uw)

    def test_conflict_b_aspect_ratios_in_quickstart(self):
        default_qs = quickstart_blueprint("فكرة سريعة", mode="UNIVERSAL_VIDEO_MODE", root=self.root)
        self.assertEqual(default_qs["aspect_ratio"], "9:16")
        self.assertEqual(default_qs["aspect_ratio_status"], "DEFAULT_COMPATIBILITY_UNCONFIRMED")
        for ar in ("9:16", "16:9", "1:1"):
            qs = quickstart_blueprint("فكرة سريعة", mode="UNIVERSAL_VIDEO_MODE", aspect_ratio=ar, root=self.root)
            self.assertEqual(qs["aspect_ratio"], ar)
            self.assertEqual(qs["aspect_ratio_status"], "USER_APPROVED")

    def test_conflict_e_no_duplicate_caption_layer_in_remotion_scenes(self):
        scenes_dir = self.root / "08_PROJECT_ASSETS/CODE_AND_SCRIPTS/MOTALIM_REMOTION_VIDEO_TEMPLATE/src/scenes"
        for tsx in scenes_dir.glob("*.tsx"):
            txt = tsx.read_text(encoding="utf-8")
            self.assertNotIn("<ArabicCaptionOverlay", txt, msg=f"Duplicate caption layer found in {tsx.name}")

    def test_scene_schema_style_execution_and_consistency(self):
        scenes = [
            {
                "scene_id": "S01", "start_frame": 0, "duration_frames": 90,
                "visual_style": "STY-001", "scene_objective": "Hook",
                "background": "obsidian", "assets": [], "characters": [],
                "camera_motion": "push-in 4%", "element_animations": ["spring_title"],
                "narration_segment": "لماذا يضيع وقتك؟", "captions": "لماذا يضيع وقتك؟",
                "sound_effects": "whoosh", "transition_in": "cut", "transition_out": "iris",
                "safe_zones": "9:16",
            },
            {
                "scene_id": "S02", "start_frame": 90, "duration_frames": 90,
                "visual_style": "STY-001", "scene_objective": "Payoff",
                "background": "obsidian", "assets": [], "characters": [],
                "camera_motion": "pull-out 3%", "element_animations": ["checklist"],
                "narration_segment": "السر في الخطوة الأولى.", "captions": "السر في الخطوة الأولى.",
                "sound_effects": "chime", "transition_in": "iris", "transition_out": "cut",
                "safe_zones": "9:16",
            },
        ]
        sc_rep = validate_scene_timeline(scenes, fps=30, aspect_ratio="9:16", audio_duration_sec=6.0)
        self.assertTrue(sc_rep["pass"], msg=sc_rep)

        spec = build_executable_style_spec("STY-001", mode="FIKRA_CHANNEL_MODE", root=self.root)
        self.assertIn(spec["readiness_status"], ("CATALOG_ONLY", "SPEC_READY", "REFERENCE_ONLY", "RENDER_TESTED"))
        cons = build_consistency_manifest("PRJ-V36", spec, fixed_assets=[self.root / "AGENTS.md"])
        self.assertTrue(cons["consistency_status"]["textual_spec_consistent"])
        self.assertFalse(cons["consistency_status"]["visual_verified_consistent"])

    def test_evidence_based_scorer_blocks_unrendered_and_passes_real_smoke_render(self):
        unrendered = compute_evidence_based_quality_score(technical_render_verified=False)
        self.assertFalse(unrendered["pass"])
        self.assertEqual(unrendered["status"], "UNVERIFIED_INCOMPLETE")

        with tempfile.TemporaryDirectory() as td:
            td_p = Path(td)
            wav_p = td_p / "sfx.wav"
            mp4_p = td_p / "smoke_9_16.mp4"
            sheet_p = td_p / "sheet.png"
            cap_p = td_p / "cap_9_16.png"

            synthesize_sfx_wav(
                [{"time_sec": 0.1, "name": "whoosh", "gain_db": -6}, {"time_sec": 1.2, "name": "pop", "gain_db": -6}],
                duration_sec=2.0, output_wav=wav_p,
            )
            subprocess.run(
                [
                    "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-f", "lavfi", "-i", "testsrc2=size=1080x1920:rate=30:duration=2",
                    "-i", str(wav_p), "-t", "2",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(mp4_p),
                ],
                check=True,
            )

            vis = evaluate_visual_quality(mp4_p, expected_aspect="9:16", contact_sheet_out=sheet_p)
            aud = analyze_audio_mastering(mp4_p, video_duration_sec=2.0)
            ar = render_arabic_caption_fixture("لماذا يضيع وقتك؟ إليك الحل العملي.", cap_p, aspect_ratio="9:16")
            st = evaluate_storytelling_and_retention(
                [
                    {"text": "لماذا يضيع وقتك؟", "duration_sec": 2.2, "visual": "hook"},
                    {"text": "السبب غياب الخطة", "duration_sec": 2.5, "visual": "chart"},
                    {"text": "ابدأ الآن", "duration_sec": 2.3, "visual": "payoff"},
                ]
            )
            spec = build_executable_style_spec("STY-001", root=self.root)
            cons = build_consistency_manifest("PRJ-SMOKE", spec)
            sc = validate_scene_timeline(
                [
                    {
                        "scene_id": "S01", "start_frame": 0, "duration_frames": 60,
                        "visual_style": "STY-001", "scene_objective": "Smoke",
                        "background": "test", "assets": [], "characters": [],
                        "camera_motion": "push", "element_animations": ["fade"],
                        "narration_segment": "test", "captions": "test",
                        "sound_effects": "whoosh", "transition_in": "cut", "transition_out": "cut",
                        "safe_zones": "9:16",
                    }
                ],
                fps=30, aspect_ratio="9:16", audio_duration_sec=2.0,
            )

            final = compute_evidence_based_quality_score(
                visual_report=vis, scene_report=sc, storytelling_report=st,
                audio_report=aud, arabic_report=ar, consistency_report=cons,
                technical_render_verified=True,
            )
            self.assertTrue(final["pass"], msg=final)
            self.assertEqual(final["status"], "VERIFIED_PASS")
            self.assertTrue(sheet_p.exists())


if __name__ == "__main__":
    unittest.main()
