"""
Automated Test Suite for Dawa Dost Backend
Tests database persistence, clinical safety, Gemini explanation generator, and API endpoints.
"""

import os
import sys
import unittest
import json

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURR_DIR)
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

import database
import drug_knowledge
import gemini_service


class TestDawaDostBackend(unittest.TestCase):

    def setUp(self):
        database.init_db()

    def test_profiles_seeded(self):
        profiles = database.get_all_profiles()
        self.assertGreaterEqual(len(profiles), 2)
        haji = database.get_profile_by_id(1)
        self.assertEqual(haji["name"], "حاجی عبد الرحمٰن")
        self.assertGreaterEqual(len(haji["conditions"]), 2)
        self.assertGreaterEqual(len(haji["allergies"]), 1)
        self.assertGreaterEqual(len(haji["medicines"]), 1)

    def test_allergy_contraindication_catch(self):
        # Haji has Penicillin allergy
        haji = database.get_profile_by_id(1)
        res = drug_knowledge.check_drug_safety("Augmentin", "Amoxicillin + Clavulanic Acid", haji)
        self.assertTrue(res["has_critical_alerts"])
        self.assertGreaterEqual(len(res["allergy_warnings"]), 1)
        self.assertIn("پینسلین", res["allergy_warnings"][0]["message_ur"])

    def test_condition_contraindication_catch(self):
        # Haji has Hypertension. Arinac contains Pseudoephedrine which is dangerous for hypertension.
        haji = database.get_profile_by_id(1)
        res = drug_knowledge.check_drug_safety("Arinac", "Pseudoephedrine + Ibuprofen", haji)
        self.assertTrue(res["has_critical_alerts"])
        self.assertGreaterEqual(len(res["condition_warnings"]), 1)
        self.assertIn("ہائی بلڈ پریشر", res["condition_warnings"][0]["message_ur"])

    def test_doctor_persona_explanation_structure(self):
        haji = database.get_profile_by_id(1)
        med_data = {
            "brand_name": "Panadol",
            "generic_name": "Paracetamol",
            "strength": "500mg",
            "formulation": "Tablet",
            "instructions": "1 tablet when fever is high",
            "instructions_ur": "تیز بخار میں ایک گولی پانی سے لیں"
        }
        exp = gemini_service.generate_doctor_explanation(med_data, haji, language="ur")
        
        # Verify all 6 mandatory sections are present
        self.assertIn("purpose", exp)
        self.assertIn("how_to_take", exp)
        self.assertIn("precautions", exp)
        self.assertIn("side_effects", exp)
        self.assertIn("special_care", exp)
        self.assertIn("doctor_advisory", exp)
        self.assertTrue(len(exp["purpose"]) > 10)
        self.assertTrue(len(exp["doctor_advisory"]) > 10)

    def test_medicine_save_and_history(self):
        haji = database.get_profile_by_id(1)
        med_id = database.save_medicine(
            profile_id=1,
            brand_name="Softin",
            generic_name="Loratadine",
            strength="10mg",
            formulation="Tablet",
            instructions="Once daily at night",
            instructions_ur="رات کو ایک گولی",
            status="active"
        )
        self.assertIsNotNone(med_id)
        
        # Verify retrieved
        med = database.get_medicine_with_explanation(med_id)
        self.assertEqual(med["brand_name"], "Softin")
        self.assertEqual(med["status"], "active")

        # Test marking as discontinued
        database.update_medicine_status(med_id, "discontinued")
        updated_med = database.get_medicine_with_explanation(med_id)
        self.assertEqual(updated_med["status"], "discontinued")
        self.assertIsNotNone(updated_med["discontinued_at"])

        # Clean up
        database.delete_medicine(med_id)


if __name__ == "__main__":
    unittest.main()
