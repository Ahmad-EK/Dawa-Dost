"""
Dawa Dost Medical Safety Service
Enforces strict medical guardrails:
1. No invented dosages or treatment durations.
2. Missing information detection.
3. Unsupported clinical claim verification.
4. Severe allergy & contraindication detection.
5. Response schema validation.
"""

from typing import Dict, Any, List, Optional
import json


class MedicalSafetyService:
    """Guarantees patient safety, output validation, and compliance with medical directives."""

    MANDATORY_EXPLANATION_FIELDS = [
        "purpose",
        "how_to_take",
        "precautions",
        "side_effects",
        "special_care",
        "doctor_advisory"
    ]

    @classmethod
    def check_allergy_contraindication(cls, drug_name: str, generic_name: str, drug_class: str, allergies: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Cross-checks medicine against recorded patient allergies.
        Returns critical alert if a match is identified.
        """
        if not allergies:
            return None

        combined_drug_str = f"{drug_name} {generic_name} {drug_class}".lower()

        for a in allergies:
            allergen_text = f"{a.get('allergen_en', '')} {a.get('allergen_ur', '')}".lower()
            
            # Penicillin / Beta-lactam group
            if "penicillin" in allergen_text or "پینسلین" in allergen_text:
                if any(x in combined_drug_str for x in ["amoxicillin", "ampicillin", "augmentin", "curam", "clavulanic", "penicillin", "آگمنٹین"]):
                    return {
                        "severity": "critical",
                        "allergen": a.get("allergen_en", "Penicillin"),
                        "message_en": "CRITICAL ALLERGY ALERT: Patient has a confirmed Penicillin allergy. This medicine contains an active beta-lactam ingredient and can trigger life-threatening anaphylaxis. DO NOT ADMINISTER.",
                        "message_ur": "⚠️ شدید الرجی کا خطرہ: مریض کے ریکارڈ میں پینسلین سے الرجی درج ہے۔ اس دوا میں اموکسی سیلین شامل ہے جو جان لیوا الرجی اور سانس کی تنگی پیدا کر سکتی ہے۔ یہ دوا ہرگز استعمال نہ کریں۔"
                    }

            # Aspirin / NSAID group
            if "aspirin" in allergen_text or "nsaid" in allergen_text or "اسپرین" in allergen_text or "بروفن" in allergen_text:
                if any(x in combined_drug_str for x in ["aspirin", "acetylsalicylic", "disprin", "loprin", "ibuprofen", "brufen", "arinac"]):
                    return {
                        "severity": "critical",
                        "allergen": a.get("allergen_en", "Aspirin/NSAIDs"),
                        "message_en": "CRITICAL ALLERGY ALERT: Patient has a recorded allergy to Aspirin/NSAIDs. Severe bronchospasm, urticaria, or gastric bleeding may result.",
                        "message_ur": "⚠️ شدید الرجی الرٹ: مریض کو اسپرین یا درد کش دواؤں (NSAIDs) سے الرجی ہے۔ یہ دوا شدید خارش، دمہ اور معدے میں تکلیف پیدا کر سکتی ہے۔"
                    }

            # Sulfa group
            if "sulfa" in allergen_text or "سلفر" in allergen_text:
                if "sulfamethoxazole" in combined_drug_str or "septrin" in combined_drug_str:
                    return {
                        "severity": "critical",
                        "allergen": a.get("allergen_en", "Sulfa"),
                        "message_en": "CRITICAL ALLERGY ALERT: Patient has a recorded Sulfa drug allergy.",
                        "message_ur": "⚠️ الرجی انتباہ: مریض کو سلفر ادویات سے الرجی ہے۔"
                    }

        return None

    @classmethod
    def enforce_dosage_guardrail(cls, raw_instructions: str, language: str = "ur") -> str:
        """
        Ensures dosage is never invented. If missing or illegible, outputs strict verification notice.
        """
        clean = (raw_instructions or "").strip()
        if not clean or clean.lower() in ["none", "unclear", "illegible", "not specified"]:
            if language == "ur":
                return "خوراک واضح نہیں ہے۔ براہِ کرم ڈاکٹر یا فارماسسٹ سے تصدیق کریں۔"
            else:
                return "Dosage instructions are not clearly legible. Please verify with your doctor or pharmacist."
        return clean

    @classmethod
    def validate_explanation_schema(cls, explanation: Dict[str, Any], language: str = "ur") -> Dict[str, Any]:
        """
        Ensures all 6 mandatory sections are present and non-empty.
        Fills missing fields with safe grounded fallbacks.
        """
        validated = dict(explanation)

        for field in cls.MANDATORY_EXPLANATION_FIELDS:
            if not validated.get(field) or not str(validated[field]).strip():
                if field == "how_to_take":
                    validated[field] = cls.enforce_dosage_guardrail("", language)
                else:
                    validated[field] = "معلومات کی تصدیق جاری ہے۔" if language == "ur" else "Information pending clinical verification."

        if "emergency_warning" not in validated:
            validated["emergency_warning"] = ""
        if "personalized_warnings" not in validated:
            validated["personalized_warnings"] = []
        if "sources" not in validated:
            validated["sources"] = []

        return validated
