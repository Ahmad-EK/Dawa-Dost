"""
Dawa Dost Drug Interaction Service
Structured clinical drug-drug interaction checker with severity classification,
evidence-level weighting, and source-attributed clinical management recommendations.
"""

from typing import List, Dict, Any, Optional
import database
from medicine_knowledge_service import MedicineKnowledgeService


class DrugInteractionService:
    """Evaluates multi-drug regimens against the verified clinical interactions database."""

    @classmethod
    def get_all_interactions(cls) -> List[Dict[str, Any]]:
        """Returns all reference drug-drug interactions."""
        return database.get_clinical_drug_interactions()

    @classmethod
    def check_interactions(cls, candidate_drug_name: str, active_medications: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Cross-checks a candidate drug against a patient's confirmed active medications.
        Returns identified interactions with severity, clinical description, and management advice.
        """
        results = []
        if not candidate_drug_name or not active_medications:
            return results

        norm_candidate = MedicineKnowledgeService.normalize_name(candidate_drug_name)
        ref_interactions = cls.get_all_interactions()

        for active_med in active_medications:
            if active_med.get("status") != "active":
                continue

            active_brand = active_med.get("brand_name", "")
            active_generic = active_med.get("generic_name", "")
            norm_active_brand = MedicineKnowledgeService.normalize_name(active_brand)
            norm_active_gen = MedicineKnowledgeService.normalize_name(active_generic)

            for inter in ref_interactions:
                da = inter["drug_a_normalized"].lower()
                db = inter["drug_b_normalized"].lower()

                match_a = (da in norm_candidate or norm_candidate in da)
                match_b = (db in norm_active_brand or db in norm_active_gen or norm_active_brand in db)

                reverse_match_a = (db in norm_candidate or norm_candidate in db)
                reverse_match_b = (da in norm_active_brand or da in norm_active_gen or norm_active_brand in da)

                if (match_a and match_b) or (reverse_match_a and reverse_match_b):
                    results.append({
                        "drug_a": candidate_drug_name,
                        "drug_b": active_brand or active_generic,
                        "severity": inter["severity"],
                        "description_en": inter["description_en"],
                        "description_ur": inter["description_ur"],
                        "management_en": inter["clinical_management_en"],
                        "management_ur": inter["clinical_management_ur"],
                        "evidence_level": inter.get("evidence_level", "probable"),
                        "source_name": inter.get("source_name", "Authoritative Pharmacopeia"),
                        "source_url": inter.get("source_url", "")
                    })

        return results
