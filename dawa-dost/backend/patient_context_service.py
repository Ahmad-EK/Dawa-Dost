"""
Dawa Dost Patient Context Service
Extracts sanitized, privacy-conscious clinical context from persistent profiles
for grounding Retrieval-Augmented Generation (RAG) prompts and safety rules.
"""

from typing import Dict, Any, Optional
import database


class PatientContextService:
    """Manages isolated patient health context retrieval and prompt construction."""

    @classmethod
    def get_patient_profile(cls, profile_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves full profile with conditions, allergies, and active medicines."""
        return database.get_profile_by_id(profile_id)

    @classmethod
    def construct_rag_patient_context(cls, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Constructs a sanitized summary for RAG grounding.
        Only sends relevant medical facts, strictly distinguishing user-confirmed
        records from AI-inferred text.
        """
        if not profile:
            return {"text_summary": "No patient profile context available.", "structured": {}}

        name = profile.get("name", "Patient")
        age = profile.get("age", "Unknown age")
        gender = profile.get("gender", "Unspecified")

        conditions = profile.get("conditions", [])
        allergies = profile.get("allergies", [])
        active_meds = [m for m in profile.get("medicines", []) if m.get("status") == "active"]

        cond_list = [f"{c.get('name_ur')} / {c.get('name_en')}" for c in conditions]
        allergy_list = [f"{a.get('allergen_ur')} / {a.get('allergen_en')} (Severity: {a.get('severity', 'high')})" for a in allergies]
        med_list = [f"{m.get('brand_name')} {m.get('strength', '')} ({m.get('generic_name', '')})" for m in active_meds]

        lines = [
            f"Patient: {name} (Age: {age}, Gender: {gender})",
            f"Confirmed Chronic Conditions: {', '.join(cond_list) if cond_list else 'None recorded'}",
            f"Confirmed Drug Allergies: {', '.join(allergy_list) if allergy_list else 'None recorded'}",
            f"Currently Active Prescribed Medications: {', '.join(med_list) if med_list else 'None recorded'}"
        ]

        return {
            "text_summary": "\n".join(lines),
            "structured": {
                "name": name,
                "age": age,
                "gender": gender,
                "conditions": conditions,
                "allergies": allergies,
                "active_medicines": active_meds
            }
        }
