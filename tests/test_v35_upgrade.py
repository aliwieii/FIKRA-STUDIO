import json
import tempfile
import unittest
import wave
from pathlib import Path

from fikra_v3 import __version__, repo_root
from fikra_v3.__main__ import main as cli_main
from fikra_v3.project_state import create_project_state
from fikra_v3.prompt_compiler import compile_v35_production_prompt
from fikra_v3.sfx_synthesizer import SUPPORTED_SFX, synthesize_sfx_wav
from fikra_v3.tiktok_retention import audit_tiktok_retention, quickstart_blueprint


class TestV35Upgrade(unittest.TestCase):
    def setUp(self):
        self.root = repo_root()

    def test_version_and_khatt_w_noor_engine_present(self):
        self.assertEqual(__version__, "3.5.0")
        eng = self.root / "08_PROJECT_ASSETS/CODE_AND_SCRIPTS/KHATT_W_NOOR_STICKMAN_ENGINE"
        for fn in ("engine.js", "render.js", "sfx.py", "sync.py", "get_asr.sh", "scene_template.html", "README_AR.md"):
            self.assertTrue((eng / fn).exists(), f"Missing {fn}")
        tpl = (eng / "scene_template.html").read_text(encoding="utf-8")
        self.assertIn("Noto Sans Arabic", tpl)

    def test_sfx_synthesizer_generates_valid_zero_music_wav(self):
        self.assertEqual(len(SUPPORTED_SFX), 13)
        with tempfile.TemporaryDirectory() as td:
            wav_p = Path(td) / "sfx_out.wav"
            cues = [
                {"time_sec": 0.1, "name": "whoosh", "gain_db": -4},
                {"time_sec": 0.6, "name": "pop", "gain_db": -5},
                {"time_sec": 1.1, "name": "chime", "gain_db": -4},
            ]
            rep = synthesize_sfx_wav(cues, duration_sec=2.0, output_wav=wav_p)
            self.assertTrue(rep["pass"])
            self.assertTrue(rep["sfx_only_zero_music"])
            self.assertTrue(wav_p.exists())
            with wave.open(str(wav_p), "rb") as wf:
                self.assertEqual(wf.getnchannels(), 2)
                self.assertEqual(wf.getframerate(), 44100)
                self.assertGreater(wf.getnframes(), 80000)

    def test_tiktok_retention_auditor_and_quickstart(self):
        bad = audit_tiktok_retention(
            [{"text": "أهلاً بكم في هذا الفيديو سنتكلم عن النجاح", "duration_sec": 5.0}],
            hashtags=["#fyp", "#viral"],
            loop_ending=False,
        )
        self.assertFalse(bad["pass"])
        self.assertLess(bad["score_100"], 75)

        good = audit_tiktok_retention(
            [
                {"text": "لماذا يفشل 90% من المبدعين في أول 3 ثوانٍ؟", "duration_sec": 2.4},
                {"text": "السبب ليس الجودة... بل غياب الخطاف البصري", "duration_sec": 2.6},
                {"text": "ولهذا اسأل نفسك في كل مرة:", "duration_sec": 2.5},
            ],
            hashtags=["#مونتاج", "#صناعة_المحتوى", "#موشن_جرافيك", "#فكرة"],
            loop_ending=True,
        )
        self.assertTrue(good["pass"], msg=good)
        self.assertGreaterEqual(good["score_100"], 95)

        qs = quickstart_blueprint("كيف تبدأ في الموشن جرافيك", mode="UNIVERSAL_VIDEO_MODE", duration_sec=45, root=self.root)
        self.assertEqual(qs["aspect_ratio"], "9:16")
        self.assertIn("NO BACKGROUND MUSIC", qs["music_policy"])

    def test_compile_v35_production_prompt_and_cli(self):
        st = create_project_state("PRJ-V35-01", "تحدي الثلاث ثواني", mode="FIKRA_CHANNEL_MODE")
        res = compile_v35_production_prompt(st, root=self.root, archetype_slug="VOX_SCRAPBOOK_COLLAGE")
        self.assertTrue(res["music_audit"]["pass"])
        self.assertIn("V3.5 TikTok Retention", res["prompt_markdown"])
        self.assertIn("KHATT_W_NOOR_STICKMAN_ENGINE", res["prompt_markdown"])

        self.assertEqual(cli_main(["quickstart", "--topic", "التدبر في سورة العصر"]), 0)


if __name__ == "__main__":
    unittest.main()
