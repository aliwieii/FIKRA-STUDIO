import subprocess
import tempfile
import unittest
from pathlib import Path

from fikra_v3.approval_guard import lock_decision
from fikra_v3.media_intelligence import detect_black_frames
from fikra_v3.project_state import create_project_state, format_stage_footer
from fikra_v3.prompt_compiler import compile_production_prompt, generate_publishing_pack


class TestV31Upgrades(unittest.TestCase):
    def test_real_ffmpeg_blackdetect_catches_black_frames(self):
        with tempfile.TemporaryDirectory() as td:
            mp4 = Path(td) / "black_test.mp4"
            # 1s pure black followed by 1s bright blue
            cmd = [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-f", "lavfi", "-i", "color=c=black:s=320x180:d=1:r=30",
                "-f", "lavfi", "-i", "color=c=0x38BDF8:s=320x180:d=1:r=30",
                "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0[v]",
                "-map", "[v]", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(mp4),
            ]
            subprocess.run(cmd, check=True)
            rep = detect_black_frames(mp4, min_duration=0.3)
            self.assertEqual(rep["measurement_type"], "REAL_FFMPEG_BLACKDETECT")
            self.assertFalse(rep["pass"])
            self.assertGreaterEqual(rep["black_intervals_count"], 1)

    def test_stage_closure_footer(self):
        footer = format_stage_footer("تمت المقابلة التفاعلية", "كتابة النص النهائي", "صياغة السيناريو")
        self.assertIn("ما تم إنجازه", footer)
        self.assertIn("ما المتبقي", footer)
        self.assertIn("الخطوة التالية", footer)
        self.assertIn("موافقتك الصريحة", footer)

    def test_publishing_pack_hashtag_bounds(self):
        pack = generate_publishing_pack(
            title="سرعة الضوء في ثانية",
            short_description="هل تخيلت كم مرة يدور الضوء حول الأرض في ثانية واحدة؟",
            cover_text="7.5 دورات في ثانية!",
            engagement_question="ما أكثر حقيقة كونية أدهشتك؟",
            hashtags=["فكرة", "علوم", "الفضاء", "سرعة_الضوء", "معلومة", "موشن_جرافيك"],
        )
        self.assertEqual(pack["hashtag_count"], 6)
        self.assertTrue(all(h.startswith("#") for h in pack["hashtags"]))
        with self.assertRaises(ValueError):
            generate_publishing_pack("t", "d", "c", "q", ["one", "two"])

    def test_prompt_compiler_v31_no_music_and_2d_guardrails(self):
        st = create_project_state("V31-01", "اختبار 3.1", mode="UNIVERSAL_VIDEO_MODE")
        lock_decision(st, "idea", "فكرة تعليمية")
        lock_decision(st, "script", "نص واضح ومختصر.")
        lock_decision(st, "style", "STY-001")
        out = compile_production_prompt(st)["prompt_markdown"]
        self.assertIn("STRICT NO-MUSIC DEFAULT", out)
        self.assertIn("avoid photorealistic 3D humans", out)
        self.assertIn("Problem -> Escalation -> Resolution", out)


if __name__ == "__main__":
    unittest.main()
