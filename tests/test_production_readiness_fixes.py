import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from fikra_v3 import repo_root
from fikra_v3.approval_guard import ApprovalLockedError, lock_decision
from fikra_v3.asset_intelligence import extract_linked_ids
from fikra_v3.knowledge_graph import build_knowledge_graph
from fikra_v3.media_intelligence import detect_black_frames
from fikra_v3.project_bootstrap import bootstrap_project
from fikra_v3.project_state import StageTransitionError, advance_stage, create_project_state
from fikra_v3.readiness_scorer import score_readiness
from fikra_v3.style_recommender import recommend_styles


class TestProductionReadinessFixes(unittest.TestCase):
    def test_fik004_lock_decision_cannot_silently_overwrite_locked_decision(self):
        st = create_project_state("FIX-004", "Lock Guard Test", mode="FIKRA_CHANNEL_MODE")
        lock_decision(st, "script", "النص المعتمد")
        with self.assertRaises(ApprovalLockedError):
            lock_decision(st, "script", "نص جديد بدون override")
        # Explicit override works and records audit trail
        lock_decision(st, "script", "نص معدل بموافقة", override_approved=True, override_reason="Explicit user request")
        self.assertEqual(st["decisions"]["script"], "نص معدل بموافقة")

    def test_fik011_logo_id_regex_extracts_valid_and_rejects_invalid(self):
        self.assertEqual(extract_linked_ids("04_LOGO_ANIMATION_LIBRARY/L08-LightSweep.tsx")["logo_ids"], ["L08"])
        self.assertEqual(extract_linked_ids("L17-Canvas.md")["logo_ids"], ["L17"])
        self.assertEqual(extract_linked_ids("L99-Invalid.md")["logo_ids"], [])
        self.assertEqual(extract_linked_ids("XL01-NotALogo.md")["logo_ids"], [])

    def test_fik015_knowledge_graph_links_style_family_prompts(self):
        kg = build_knowledge_graph(write_output=False)
        linked = sum(
            1 for node in kg["styles"].values()
            if any("03_STYLE_LIBRARY/STYLE_PROMPTS/" in p for p in node["prompt_templates"])
        )
        self.assertGreaterEqual(linked, 20)

    def test_fik005_blackdetect_fails_on_corrupt_file(self):
        with tempfile.TemporaryDirectory() as td:
            bad = Path(td) / "corrupt.mp4"
            bad.write_bytes(b"not a valid mp4 file")
            with self.assertRaises(RuntimeError):
                detect_black_frames(bad)

    def test_fik007_readiness_rejects_unverified_boolean_and_accepts_sha256_bound_qa(self):
        with tempfile.TemporaryDirectory() as td:
            td_p = Path(td)
            st = create_project_state("FIX-007", "Readiness Proof", mode="FIKRA_CHANNEL_MODE")
            lock_decision(st, "style", "STY-001")
            blog = td_p / "build.log"
            blog.write_text("BUILD OK\n", encoding="utf-8")
            st["evidence"].update({
                "prompt_compiled": True, "spec_validated": True, "code_validated": True,
                "build_log_path": str(blog), "media_qa_passed": True,
            })
            # Without real MP4 + SHA-256 QA report, MUST stop at BUILD_TESTED (85), never RENDER_TESTED
            r1 = score_readiness(st)
            self.assertEqual(r1["readiness_tier"], "BUILD_TESTED")

            # Generate real MP4 + run real fikra_media_qa_pipeline.py with --write-report
            mp4 = td_p / "real.mp4"
            qa_json = td_p / "qa_report.json"
            subprocess.run([
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-f", "lavfi", "-i", "color=c=0x17335C:s=1080x1920:d=1:r=30",
                "-f", "lavfi", "-i", "sine=frequency=440:duration=1",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(mp4),
            ], check=True)
            pipe = repo_root() / "08_PROJECT_ASSETS/CODE_AND_SCRIPTS/MOTALIM_PYTHON_SCRIPTS/fikra_media_qa_pipeline.py"
            subprocess.run([sys.executable, str(pipe), "--video", str(mp4), "--write-report", str(qa_json)], check=True)
            st["evidence"]["render_output_path"] = str(mp4)
            st["evidence"]["qa_report_path"] = str(qa_json)
            r2 = score_readiness(st)
            self.assertEqual(r2["readiness_tier"], "RENDER_TESTED")
            self.assertEqual(r2["score"], 100)

    def test_state_machine_blocks_skipping_and_unapproved_transitions(self):
        st = create_project_state("SM-01", "State Machine Test", mode="FIKRA_CHANNEL_MODE")
        with self.assertRaises(StageTransitionError):
            advance_stage(st, "SCRIPT_LOCKED", user_approved=True)  # cannot skip IDEA_LOCKED
        with self.assertRaises(StageTransitionError):
            advance_stage(st, "IDEA_LOCKED", user_approved=False)  # missing explicit approval
        lock_decision(st, "idea", "فكرة علمية")
        advance_stage(st, "IDEA_LOCKED", user_approved=True)
        self.assertEqual(st["stage"], "IDEA_LOCKED")

    def test_fik016_cli_state_init_and_advance(self):
        with tempfile.TemporaryDirectory() as td:
            sp = Path(td) / "st.json"
            res = subprocess.run(
                [sys.executable, "-m", "fikra_v3", "state", "init", "--out", str(sp), "--id", "CLI-1", "--title", "CLI Test"],
                cwd=repo_root(), capture_output=True, text=True, check=True,
            )
            self.assertTrue(sp.exists())
            self.assertEqual(json.loads(res.stdout)["stage"], "INIT")

    def test_fik017_bootstrap_overwrite_protection_and_aspect_presets(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "proj"
            r = bootstrap_project(out, "P-16-9", "Landscape", mode="UNIVERSAL_VIDEO_MODE", style_id="STY-001", aspect_ratio="16:9")
            self.assertEqual(r["resolution"], "1920x1080")
            with self.assertRaises(FileExistsError):
                bootstrap_project(out, "P-16-9", "Landscape", mode="UNIVERSAL_VIDEO_MODE", style_id="STY-001")

    def test_fik019_music_py_blocked_by_policy_guard(self):
        mp = repo_root() / "08_PROJECT_ASSETS/CODE_AND_SCRIPTS/MOTALIM_PYTHON_SCRIPTS/music.py"
        res = subprocess.run([sys.executable, str(mp)], capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("FIKRA_NO_MUSIC_POLICY", res.stderr)

    def test_arabic_difficulty_filter_in_style_recommender(self):
        recs = recommend_styles("تعليم رياضيات", max_difficulty="low", top_k=5)
        self.assertEqual(len(recs), 5)


if __name__ == "__main__":
    unittest.main()
