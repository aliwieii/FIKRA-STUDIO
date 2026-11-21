import tempfile
import unittest
from pathlib import Path

from fikra_v3.approval_guard import ApprovalLockedError, lock_decision, update_decision, verify_approval_integrity
from fikra_v3.multi_agent_review import run_multi_agent_review
from fikra_v3.project_bootstrap import bootstrap_project
from fikra_v3.project_state import create_project_state
from fikra_v3.prompt_compiler import compile_production_prompt
from fikra_v3.readiness_scorer import score_readiness


class TestStateApprovalsAndPrompt(unittest.TestCase):
    def test_approval_lock_blocks_silent_mutation_and_allows_audited_override(self):
        st = create_project_state("PRJ-01", "حلقة اختبار", mode="FIKRA_CHANNEL_MODE")
        lock_decision(st, "script", "النص المعتمد الأول")
        with self.assertRaises(ApprovalLockedError):
            update_decision(st, "script", "نص معدل بدون إذن")
        # Explicit override succeeds and logs audit event
        update_decision(st, "script", "النص المعتمد المعدل", override_approved=True, override_reason="User requested edit")
        self.assertEqual(st["decisions"]["script"], "النص المعتمد المعدل")
        self.assertTrue(verify_approval_integrity(st)["valid"])

    def test_prompt_compiler_mode_isolation(self):
        st = create_project_state("PRJ-02", "Product Explainer", mode="UNIVERSAL_VIDEO_MODE", aspect_ratio="16:9")
        lock_decision(st, "idea", "شرح منتج برمجي")
        lock_decision(st, "script", "مرحباً بكم في العرض التقني الجديد.")
        lock_decision(st, "style", "STY-001")
        res = compile_production_prompt(st)
        self.assertTrue(res["isolation_clean"])
        self.assertNotIn("FIKRA CHANNEL POLICY", res["prompt_markdown"])

    def test_readiness_strict_gating(self):
        st = create_project_state("PRJ-03", "Gating Test", mode="UNIVERSAL_VIDEO_MODE")
        st["decisions"]["style"] = "STY-001"
        st["evidence"]["prompt_compiled"] = True
        st["evidence"]["spec_validated"] = True
        st["evidence"]["code_validated"] = True
        # No build log exists -> MUST stop at CODE_READY, never BUILD_TESTED
        r = score_readiness(st)
        self.assertEqual(r["readiness_tier"], "CODE_READY")
        self.assertEqual(r["score"], 65)

    def test_multi_agent_review_and_bootstrap(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "demo"
            bs = bootstrap_project(out, "BS-01", "اختبار التوليد", mode="FIKRA_CHANNEL_MODE", style_id="STY-001")
            self.assertTrue(bs["isolation_clean"])
            self.assertTrue((out / "project_state.json").exists())
            self.assertTrue((out / "compiled_prompt.md").exists())
            st = create_project_state("REV-01", "مراجعة", mode="FIKRA_CHANNEL_MODE")
            lock_decision(st, "idea", "فكرة علمية")
            lock_decision(st, "script", "كل نجم في السماء يحكي قصة.")
            lock_decision(st, "style", "STY-001")
            compiled = compile_production_prompt(st)
            rev = run_multi_agent_review(st, compiled["prompt_markdown"])
            self.assertTrue(rev["overall_pass"])


if __name__ == "__main__":
    unittest.main()
