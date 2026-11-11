"""
Dawa Dost Medical Source Service
Tracks authoritative pharmaceutical references (FDA, NHS, MedlinePlus, DRAP, WHO),
manages source attributions, timestamps, and detects conflicting regulatory information.
"""

from typing import List, Dict, Any, Optional
import database


class MedicalSourceService:
    """Manages medical information sources and evidence verification."""

    @staticmethod
    def get_sources() -> List[Dict[str, Any]]:
        """Returns all recognized medical reference sources."""
        return database.get_all_medical_sources()

    @staticmethod
    def get_source(source_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves a specific source by ID."""
        return database.get_medical_source_by_id(source_id)

    @staticmethod
    def check_conflicting_information(drug_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Detects discrepancies across international vs local regulatory listings
        (e.g. regional differences in approved strengths, pediatric age thresholds, or OTC status).
        """
        discrepancies = []
        brand = drug_data.get("brand_name", "")
        strengths = drug_data.get("strengths", [])

        # Example: Co-amoxiclav formulation differences between US and Pakistan
        if "augmentin" in brand.lower():
            discrepancies.append({
                "topic": "Formulation Strengths & Regional Ratios",
                "finding_en": "In Pakistan (DRAP), Augmentin 625mg (500mg/125mg) and 1g (875mg/125mg) are standard adult strengths. In the US (FDA), 875mg/125mg and 1000mg extended-release are primary.",
                "finding_ur": "پاکستان میں آگمنٹین 625 ملی گرام اور 1 گرام سب سے زیادہ تجویز کی جانے والی خوراکیں ہیں جبکہ بین الاقوامی سطح پر مختلف تناسب بھی پائے جاتے ہیں۔",
                "significance": "informational",
                "sources": ["DRAP Pakistan Register", "FDA CDER"]
            })

        # Example: Aspirin OTC indication vs pediatric warning
        if "disprin" in brand.lower() or "aspirin" in brand.lower():
            discrepancies.append({
                "topic": "Pediatric Age Thresholds for Reye's Syndrome",
                "finding_en": "UK NHS strictly restricts Aspirin in children under 16 years. US FDA guidelines similarly caution against use under 19 years during viral fevers.",
                "finding_ur": "یو کے اور یو ایس دونوں ریگولیٹری ادارے بچوں اور نوعمروں میں وائرل بخار کے دوران اسپرین کو سختی سے ممنوع قرار دیتے ہیں۔",
                "significance": "critical_warning",
                "sources": ["NHS UK Medicines", "FDA Safety Warning"]
            })

        return discrepancies
