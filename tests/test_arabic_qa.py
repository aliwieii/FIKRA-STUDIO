import unittest
from fikra_v3.arabic_qa import active_caption_page, analyze_arabic_text, paginate_arabic_caption, validate_srt


class TestArabicQA(unittest.TestCase):
    def test_zero_word_deletion_pagination(self):
        words = [{"w": f"كلمة{i}", "start": i * 0.4, "end": (i + 1) * 0.4 - 0.02} for i in range(13)]
        pages = paginate_arabic_caption(words, max_words_per_line=6)
        self.assertEqual(len(pages), 3)
        self.assertEqual(sum(len(p) for p in pages), 13)
        # Word 10 (index 9, start 3.6s) must appear in page 2
        p2 = active_caption_page(words, current_sec=3.7, max_words_per_line=6)
        self.assertIn("كلمة9", [w["w"] for w in p2])

    def test_diacritics_and_mixed_bidi(self):
        rep = analyze_arabic_text("﴿سَنُرِيهِمْ آيَاتِنَا﴾ مع Remotion 4", duration_sec=4.0)
        self.assertTrue(rep["has_arabic"])
        self.assertTrue(rep["has_mixed_latin"])
        self.assertGreater(rep["diacritics_count"], 5)
        self.assertTrue(rep["pass"])

    def test_detects_broken_spaced_letters(self):
        rep = analyze_arabic_text("ف ك ر ة ج د ي د ة")
        self.assertFalse(rep["pass"])
        self.assertGreater(rep["spaced_letters_hits"], 0)

    def test_srt_validation(self):
        srt = (
            "1\n00:00:00,200 --> 00:00:03,000\nكل نجم تراه الليلة\n\n"
            "2\n00:00:03,100 --> 00:00:06,000\nهو رسالة من الماضي البعيد\n"
        )
        res = validate_srt(srt)
        self.assertTrue(res["pass"])
        self.assertEqual(res["total_blocks"], 2)


if __name__ == "__main__":
    unittest.main()
