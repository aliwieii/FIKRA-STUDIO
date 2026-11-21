import unittest
from fikra_v3.context_loader import detect_mode, load_context
from fikra_v3.model_adapter import build_adapter_payload


class TestContextAndModes(unittest.TestCase):
    def test_detect_modes(self):
        self.assertEqual(detect_mode("هيا نبدأ بإنشاء فيديو قناة فكرة عن الكون"), "FIKRA_CHANNEL_MODE")
        self.assertEqual(detect_mode("تحريك الشعار بأسلوب نيون"), "LOGO_ANIMATION_MODE")
        self.assertEqual(detect_mode("فيديو تعريفي عام لمنتج تقني"), "UNIVERSAL_VIDEO_MODE")
        self.assertEqual(detect_mode("مقطع قرآن بصوت قارئ"), "QURAN_MODE")

    def test_universal_mode_isolation(self):
        ctx = load_context(mode="UNIVERSAL_VIDEO_MODE", style_id="STY-001")
        self.assertTrue(ctx["isolation_verified"])
        paths = [f["path"] for f in ctx["files"]]
        self.assertNotIn("02_WORKFLOWS/FIKRA_CHANNEL_WORKFLOW.md", paths)
        self.assertNotIn("06_PROMPT_LIBRARY/VOICE_PROMPTS/FIKRA_VOICE_01_TTS_PROMPT.md", paths)
        self.assertIn("AGENTS.md", paths)

    def test_fikra_channel_loads_voice_and_workflow(self):
        ctx = load_context(mode="FIKRA_CHANNEL_MODE")
        paths = [f["path"] for f in ctx["files"]]
        self.assertIn("02_WORKFLOWS/FIKRA_CHANNEL_WORKFLOW.md", paths)
        self.assertIn("06_PROMPT_LIBRARY/VOICE_PROMPTS/FIKRA_VOICE_01_TTS_PROMPT.md", paths)

    def test_model_adapter_targets(self):
        for target in ("gemini", "claude", "chatgpt"):
            payload = build_adapter_payload(target=target, mode="UNIVERSAL_VIDEO_MODE")
            self.assertEqual(payload["target_agent"], target)
            self.assertEqual(payload["source_of_truth"], "AGENTS.md")
            self.assertGreater(len(payload["minimal_files_to_read"]), 3)


if __name__ == "__main__":
    unittest.main()
