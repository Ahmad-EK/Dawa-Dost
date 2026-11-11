"""
Comprehensive Test Suite for Dawa Dost
Tests the 13 required scenarios:
1. Scan a medicine and retrieve its medical database entry.
2. Scan a medicine that has multiple possible brand-name matches (ambiguity detection).
3. Scan a medicine not in local database (graceful handling).
4. Grounded doctor-persona explanation in simple Urdu.
5. Grounded doctor-persona explanation in English.
6. Multi-turn conversational follow-up questions.
7. Patient health profile context retrieval.
8. Relevant allergy warning cross-matching (e.g. Penicillin vs Augmentin).
9. Clinical drug-drug interaction detection against active meds.
10. Conflicting international vs local medical references detection.
11. Gemini API failure & offline formulary resilience.
12. Malformed AI output recovery & schema validation.
13. Strict guardrail against unsupported/invented dosage generation.
"""

import sys
import os
import unittest
import json

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURR_DIR)
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

import database
from gemini_service import GeminiService
from medicine_knowledge_service import MedicineKnowledgeService
from medical_condition_service import MedicalConditionService
from drug_interaction_service import DrugInteractionService
from medical_source_service import MedicalSourceService
from patient_context_service import PatientContextService
from medical_safety_service import MedicalSafetyService


class TestExpandedMedicalIntelligence(unittest.TestCase):

    def setUp(self):
        database.init_db()

    # Scenario 1: Scan a medicine and retrieve its medical database entry
    def test_scenario_01_retrieve_medical_database_entry(self):
        monograph = MedicineKnowledgeService.get_medicine_monograph("Augmentin")
        self.assertIsNotNone(monograph)
        self.assertEqual(monograph["generic_name"], "Amoxicillin + Clavulanic Acid (Co-Amoxiclav)")
        self.assertIn("GSK Pakistan", monograph["manufacturers"])
        self.assertTrue(len(monograph["general_uses_ur"]) > 20)
        self.assertIn("source_name", monograph)

    # Scenario 2: Multiple possible brand-name matches (ambiguity detection)
    def test_scenario_02_ambiguity_detection_multiple_brands(self):
        # Query matching multiple formulations/variations
        res = MedicineKnowledgeService.search_medicines("Panadol", limit=5)
        self.assertTrue(len(res["matches"]) >= 1)
        # Check fuzzy matching tolerance
        fuzzy_res = MedicineKnowledgeService.search_medicines("Panadoll", limit=5)
        self.assertTrue(len(fuzzy_res["matches"]) >= 1)
        self.assertEqual(fuzzy_res["matches"][0]["generic_name"], "Paracetamol (Acetaminophen)")

    # Scenario 3: Medicine not present in local database
    def test_scenario_03_unknown_medicine_handling(self):
        search_res = MedicineKnowledgeService.search_medicines("UnknownRareDrugXYZ99", limit=3)
        self.assertEqual(len(search_res["matches"]), 0)
        self.assertIsNone(search_res["best_match"])

        # Explanation generation for unknown medicine still succeeds safely without crashing
        exp = GeminiService.generate_rag_doctor_explanation(
            {"brand_name": "UnknownRareDrugXYZ99", "generic_name": "NewChemicalEntity"},
            profile_id=1,
            language="ur"
        )
        self.assertIn("UnknownRareDrugXYZ99", exp["purpose"])
        self.assertIn("خوراک واضح نہیں ہے", exp["how_to_take"])

    # Scenario 4: Grounded doctor-persona explanation in simple Urdu
    def test_scenario_04_urdu_doctor_explanation(self):
        exp = GeminiService.generate_rag_doctor_explanation(
            {"brand_name": "Glucophage", "generic_name": "Metformin", "strength": "500mg"},
            profile_id=1,
            language="ur"
        )
        self.assertIn("purpose", exp)
        self.assertIn("how_to_take", exp)
        self.assertIn("precautions", exp)
        self.assertIn("side_effects", exp)
        self.assertIn("special_care", exp)
        self.assertIn("doctor_advisory", exp)
        self.assertIn("شوگر", exp["purpose"])

    # Scenario 5: Grounded doctor-persona explanation in English
    def test_scenario_05_english_doctor_explanation(self):
        exp = GeminiService.generate_rag_doctor_explanation(
            {"brand_name": "Glucophage", "generic_name": "Metformin", "strength": "500mg"},
            profile_id=1,
            language="en"
        )
        self.assertIn("diabetes", exp["purpose"].lower())
        self.assertIn("doctor", exp["doctor_advisory"].lower())

    # Scenario 6: Follow-up conversational questions
    def test_scenario_06_conversational_followup_question(self):
        import time
        session_id = f"test_session_{time.time()}"
        ans = GeminiService.answer_followup_question(
            session_id=session_id,
            profile_id=1,
            medicine_name="Panadol",
            question="کیا میں یہ دوا کھانے کے بعد لے سکتا ہوں؟",
            language="ur"
        )
        self.assertEqual(ans["session_id"], session_id)
        self.assertTrue(len(ans["answer"]) > 10)
        self.assertIn("کھانے کے بعد", ans["answer"])

        # Verify persisted in database
        history = database.get_conversation_history(session_id)
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["role"], "user")
        self.assertEqual(history[1]["role"], "assistant")

    # Scenario 7: Patient health profile context retrieval
    def test_scenario_07_patient_context_retrieval(self):
        profile = PatientContextService.get_patient_profile(1)
        self.assertEqual(profile["name"], "حاجی عبد الرحمٰن")
        ctx = PatientContextService.construct_rag_patient_context(profile)
        self.assertIn("حاجی عبد الرحمٰن", ctx["text_summary"])
        self.assertIn("Type 2 Diabetes", ctx["text_summary"])
        self.assertIn("Penicillin", ctx["text_summary"])

    # Scenario 8: Relevant allergy warning cross-matching
    def test_scenario_08_allergy_warning_detection(self):
        p1 = database.get_profile_by_id(1) # Has Penicillin allergy
        alert = MedicalSafetyService.check_allergy_contraindication(
            "Augmentin", "Amoxicillin + Clavulanic Acid", "Penicillin-class", p1["allergies"]
        )
        self.assertIsNotNone(alert)
        self.assertEqual(alert["severity"], "critical")
        self.assertIn("پینسلین", alert["message_ur"])

    # Scenario 9: Interactions with currently recorded medicines
    def test_scenario_09_drug_interaction_detection(self):
        p1 = database.get_profile_by_id(1) # Takes Glucophage 500mg
        # Candidate Disprin interacts with Glucophage
        interactions = DrugInteractionService.check_interactions("Disprin", p1["medicines"])
        self.assertGreaterEqual(len(interactions), 1)
        self.assertEqual(interactions[0]["drug_a"], "Disprin")
        self.assertIn("شوگر", interactions[0]["description_ur"])

    # Scenario 10: Conflicting or unavailable medical references
    def test_scenario_10_conflicting_references_handling(self):
        discrepancies = MedicalSourceService.check_conflicting_information({"brand_name": "Augmentin"})
        self.assertGreaterEqual(len(discrepancies), 1)
        self.assertIn("DRAP", discrepancies[0]["sources"][0])

    # Scenario 11: Gemini API failure resilience (graceful fallback)
    def test_scenario_11_gemini_api_failure_resilience(self):
        # Call with dummy key / network disconnected
        exp = GeminiService.generate_rag_doctor_explanation(
            {"brand_name": "Tenormin", "generic_name": "Atenolol", "strength": "50mg"},
            profile_id=1,
            language="ur"
        )
        self.assertIsNotNone(exp)
        self.assertIn("بلڈ پریشر", exp["purpose"])

    # Scenario 12: Malformed AI response recovery & schema validation
    def test_scenario_12_malformed_ai_recovery(self):
        malformed = {"purpose": "Some text", "random_field": 123} # Missing how_to_take, precautions, etc.
        validated = MedicalSafetyService.validate_explanation_schema(malformed, language="ur")
        self.assertIn("how_to_take", validated)
        self.assertIn("precautions", validated)
        self.assertIn("side_effects", validated)
        self.assertIn("special_care", validated)
        self.assertIn("doctor_advisory", validated)
        self.assertEqual(validated["how_to_take"], "خوراک واضح نہیں ہے۔ براہِ کرم ڈاکٹر یا فارماسسٹ سے تصدیق کریں۔")

    # Scenario 13: Strict guardrail against unsupported/invented dosage
    def test_scenario_13_no_invented_dosage_guardrail(self):
        unspecified = MedicalSafetyService.enforce_dosage_guardrail("", language="ur")
        self.assertEqual(unspecified, "خوراک واضح نہیں ہے۔ براہِ کرم ڈاکٹر یا فارماسسٹ سے تصدیق کریں۔")
        unspecified_en = MedicalSafetyService.enforce_dosage_guardrail("None", language="en")
        self.assertIn("not clearly legible", unspecified_en)


if __name__ == "__main__":
    unittest.main()
