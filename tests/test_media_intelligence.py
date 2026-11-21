import subprocess
import tempfile
import unittest
from pathlib import Path

from fikra_v3.media_intelligence import analyze_audio_real


class TestMediaIntelligenceRealFFmpeg(unittest.TestCase):
    def test_real_ffmpeg_audio_video_analysis(self):
        with tempfile.TemporaryDirectory() as td:
            mp4 = Path(td) / "fixture_9x16.mp4"
            # Generate real 2s 1080x1920 H.264/AAC video with 1s tone + 1s silence
            cmd = [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-f", "lavfi", "-i", "color=c=0x060B14:s=1080x1920:d=2:r=30",
                "-f", "lavfi", "-i", "sine=frequency=440:duration=1",
                "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono:d=1",
                "-filter_complex", "[1:a][2:a]concat=n=2:v=0:a=1[aout]",
                "-map", "0:v", "-map", "[aout]",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest",
                str(mp4),
            ]
            subprocess.run(cmd, check=True)
            rep = analyze_audio_real(mp4, fps=30)
            self.assertEqual(rep["measurement_type"], "REAL_FFMPEG_ANALYSIS")
            self.assertTrue(rep["has_audio"])
            self.assertAlmostEqual(rep["duration_sec"], 2.0, delta=0.25)
            self.assertIsNotNone(rep["mean_volume_db"])
            self.assertGreaterEqual(len(rep["silence_intervals"]), 1)
            self.assertGreaterEqual(rep["envelope_frames"], 50)
            # First half has signal > second half silence
            first_half = sum(rep["envelope"][:25]) / 25
            second_half = sum(rep["envelope"][35:55]) / 20
            self.assertGreater(first_half, second_half + 0.1)


if __name__ == "__main__":
    unittest.main()
