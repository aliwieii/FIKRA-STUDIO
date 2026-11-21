import unittest
from fikra_v3.asset_intelligence import query_assets
from fikra_v3.knowledge_graph import build_knowledge_graph, lookup_logo, lookup_style
from fikra_v3.style_recommender import recommend_styles


class TestAssetAndGraph(unittest.TestCase):
    def test_knowledge_graph_exact_counts(self):
        kg = build_knowledge_graph(write_output=False)
        self.assertEqual(kg["counts"]["styles"], 32)
        self.assertEqual(kg["counts"]["logo_animations"], 17)
        self.assertEqual(kg["counts"]["modes"], 9)

    def test_style_lookup_complete_chain(self):
        st = lookup_style("STY-001")
        self.assertIsNotNone(st)
        self.assertEqual(st["style_id"], "STY-001")
        self.assertTrue(st["spec_file"])
        self.assertTrue(st["prompt_templates"])
        self.assertTrue(st["execution_requirements"])

    def test_logo_lookup(self):
        lg = lookup_logo("L01")
        self.assertIsNotNone(lg)
        self.assertTrue(lg["animation_id"].startswith("L01"))

    def test_style_recommender(self):
        recs = recommend_styles("الكون والثقوب السوداء", mode="FIKRA_CHANNEL_MODE", top_k=5)
        self.assertEqual(len(recs), 5)
        self.assertTrue(all(r["style_id"].startswith("STY-") for r in recs))

    def test_sqlite_asset_query(self):
        hits = query_assets("STY-001")
        self.assertGreaterEqual(len(hits), 1)


if __name__ == "__main__":
    unittest.main()
