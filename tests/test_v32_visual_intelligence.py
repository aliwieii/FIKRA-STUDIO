import subprocess
import tempfile
import unittest
from pathlib import Path

from fikra_v3 import MODES, repo_root
from fikra_v3.approval_guard import ApprovalLockedError, lock_decision
from fikra_v3.context_loader import load_context
from fikra_v3.project_state import create_project_state
from fikra_v3.prompt_compiler import compile_v32_production_prompt, get_adaptive_interview_question
from fikra_v3.regression_guard import run_regression_checks
from fikra_v3.style_recommender import compare_styles
from fikra_v3.visual_intelligence import (
    build_video_review_report,
    create_visual_analysis_template,
    extract_contact_sheet,
    verify_reference_access,
)


class TestV32VisualIntelligence(unittest.TestCase):
    # Test A & G — Reference Access & Honest Reporting
    def test_a_and_g_reference_access_and_honest_reporting(self):
        missing = verify_reference_access("REF-999", media_path=Path("/nonexistent/video.mp4"))
        self.assertFalse(missing["accessible"])
        self.assertEqual(missing["visual_review_status"], "UNVERIFIED")
        analysis = create_visual_analysis_template("REF-999", missing)
        self.assertIn("UNAVAILABLE", analysis["dimensions"]["G_audio"])

    # Test B — Visual Preview & Contact Sheet from real FFmpeg video
    def test_b_real_ffmpeg_contact_sheet_extraction(self):
        with tempfile.TemporaryDirectory() as td:
            td_p = Path(td)
            mp4 = td_p / "sample_ref.mp4"
            sheet = td_p / "contact_sheet.png"
            subprocess.run([
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-f", "lavfi", "-i", "testsrc2=size=640x360:duration=2:rate=30",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", str(mp4),
            ], check=True)
            access = verify_reference_access("REF-TEST", media_path=mp4)
            self.assertTrue(access["accessible"])
            self.assertEqual(access["visual_review_status"], "EXTRACTED_FRAME")
            res = extract_contact_sheet(mp4, sheet, ref_id="REF-TEST", num_frames=6)
            self.assertTrue(sheet.exists())
            self.assertEqual(res["frames_extracted"], 6)
            self.assertGreater(sheet.stat().st_size, 5000)

    # Test C — 6-Criteria Weighted Style Selection & Comparison
    def test_c_weighted_style_comparison_caps_unverified(self):
        cmp_res = compare_styles("شرح علمي عن الكون والفضاء", mode="FIKRA_CHANNEL_MODE", target_tool="remotion_motion", top_k=3)
        self.assertIsNotNone(cmp_res["best_choice"])
        self.assertIsNotNone(cmp_res["alternative"])
        self.assertEqual(len(cmp_res["compared_styles"]), 3)
        for st in cmp_res["compared_styles"]:
            if st["readiness_status"] == "CATALOG_ONLY":
                self.assertEqual(st["confidence"], "LOW_UNVERIFIED_CATALOG")

    # Test D — Tool-Adapted Prompt Compilation & 15-Point QA Gate
    def test_d_prompt_compilation_assets_and_qa_gate(self):
        st = create_project_state("V32-01", "اختبار V3.2", mode="UNIVERSAL_VIDEO_MODE", aspect_ratio="16:9")
        lock_decision(st, "idea", "شرح تفاعلي لكيفية عمل الذكاء الاصطناعي")
        lock_decision(st, "script", "الذكاء الاصطناعي يتعلم من الأنماط بسرعة فائقة.")
        lock_decision(st, "style", "STY-001")
        out = compile_v32_production_prompt(st, target_tool="remotion_motion")
        self.assertIn("REQUIRED INPUT ASSETS", out["prompt_markdown"])
        self.assertIn("REFERENCE USAGE INSTRUCTIONS", out["prompt_markdown"])
        self.assertIn("Negative Prompt", out["prompt_markdown"])
        self.assertIn("STRICT NO-MUSIC DEFAULT", out["prompt_markdown"])
        self.assertTrue(out["prompt_qa_gate"]["pass"])
        self.assertEqual(out["prompt_qa_gate"]["score"], 100)

    # Test E — All 9 Modes Remain Intact & Isolated
    def test_e_all_nine_modes_isolated(self):
        self.assertEqual(len(MODES), 9)
        for m in MODES:
            ctx = load_context(mode=m)
            self.assertEqual(ctx["mode"], m)
            self.assertTrue(ctx["isolation_verified"])

    # Test F — Approval Protection
    def test_f_approval_protection_intact(self):
        st = create_project_state("V32-LOCK", "Lock Test", mode="FIKRA_CHANNEL_MODE")
        lock_decision(st, "idea", "فكرة معتمدة")
        with self.assertRaises(ApprovalLockedError):
            lock_decision(st, "idea", "تغيير غير مصرح")

    # Adaptive Interview & Localized Post-Production Video Review Diff
    def test_adaptive_interview_and_video_review_diff(self):
        q1 = get_adaptive_interview_question("product_ad", {"topic": "تطبيق إدارة وقت"})
        self.assertFalse(q1["complete"])
        self.assertEqual(q1["next_key"], "audience")
        rev = build_video_review_report([
            {"scene": "S01", "expected": "Smooth push-in", "actual": "Smooth push-in", "difference": "None", "severity": "LOW", "prompt_fix": "None"},
            {"scene": "S02", "expected": "RTL caption", "actual": "Clipped text", "difference": "Overflow", "severity": "HIGH", "prompt_fix": "Reduce font to 40px"},
        ])
        self.assertEqual(rev["localized_fix_scenes"], ["S02"])
        self.assertFalse(rev["full_rerender_required"])

    # Test H — Regression Guard Intact
    def test_h_regression_guard_passes(self):
        self.assertTrue(run_regression_checks()["pass"])


if __name__ == "__main__":
    unittest.main()
