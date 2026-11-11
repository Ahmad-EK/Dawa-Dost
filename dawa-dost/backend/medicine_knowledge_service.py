"""
Dawa Dost Medicine Knowledge Service
Search, fuzzy matching, entity normalization, ambiguity detection,
and authoritative pharmaceutical monograph retrieval.
"""

import difflib
import json
from typing import List, Dict, Any, Optional
import database


class MedicineKnowledgeService:
    """Provides high-precision retrieval and fuzzy matching for pharmaceutical products."""

    @classmethod
    def get_all_medicines(cls) -> List[Dict[str, Any]]:
        """Retrieves all medicines from the structured knowledge database."""
        return database.get_all_knowledge_medicines()

    @classmethod
    def normalize_name(cls, query: str) -> str:
        """Cleans and standardizes drug names for indexing."""
        if not query:
            return ""
        clean = query.lower().strip()
        # Remove common dosage symbols and punctuation
        for ch in ["+", "/", "-", ",", "(", ")", ".", "tab", "cap", "syp", "inj"]:
            clean = clean.replace(ch, " ")
        words = [w for w in clean.split() if not any(c.isdigit() for c in w)]
        return " ".join(words).strip()

    @classmethod
    def search_medicines(cls, query: str, limit: int = 5) -> Dict[str, Any]:
        """
        Fuzzy searches the medicine database using brand names, generic names, and active ingredients.
        Detects ambiguity if multiple distinct medicines are plausible candidates.
        """
        if not query or len(query.strip()) < 2:
            return {"matches": [], "is_ambiguous": False, "best_match": None}

        clean_query = query.lower().strip()
        norm_query = cls.normalize_name(query)
        all_meds = cls.get_all_medicines()

        scored_candidates = []

        for med in all_meds:
            gen_name = med["generic_name"].lower()
            brands = [b.lower() for b in med.get("brand_names", [])]
            ingredients = [i.lower() for i in med.get("active_ingredients", [])]
            category = med.get("drug_category", "").lower()

            score = 0.0

            # 1. Exact brand or generic match
            if clean_query in brands or clean_query == gen_name:
                score = 1.0
            # 2. Substring match in brand
            elif any(clean_query in b or b in clean_query for b in brands):
                score = 0.88
            # 3. Substring match in generic name
            elif clean_query in gen_name or gen_name in clean_query:
                score = 0.82
            # 4. Ingredient match
            elif any(clean_query in i for i in ingredients):
                score = 0.78
            # 5. Fuzzy ratio matching (accommodating OCR errors / typos)
            else:
                max_brand_ratio = max([difflib.SequenceMatcher(None, norm_query, cls.normalize_name(b)).ratio() for b in brands] or [0.0])
                gen_ratio = difflib.SequenceMatcher(None, norm_query, cls.normalize_name(gen_name)).ratio()
                score = max(max_brand_ratio, gen_ratio)

            if score > 0.45:
                scored_candidates.append({
                    "score": round(score, 3),
                    "id": med["id"],
                    "brand_name": med["brand_names"][0] if med["brand_names"] else med["generic_name"],
                    "all_brands": med["brand_names"],
                    "generic_name": med["generic_name"],
                    "pharmaceutical_class": med["pharmaceutical_class"],
                    "drug_category": med["drug_category"],
                    "available_strengths": med["strengths"],
                    "dosage_forms": med["dosage_forms"],
                    "manufacturers": med["manufacturers"],
                    "source_name": med.get("source_name", "Authoritative Compendium"),
                    "is_verified": bool(med.get("is_verified", 1))
                })

        # Sort by score descending
        scored_candidates.sort(key=lambda x: x["score"], reverse=True)
        top_matches = scored_candidates[:limit]

        # Determine ambiguity: if top two matches are within 0.15 of each other and not exact 1.0
        is_ambiguous = False
        if len(top_matches) > 1:
            first_score = top_matches[0]["score"]
            second_score = top_matches[1]["score"]
            if first_score < 0.95 and (first_score - second_score) < 0.15:
                is_ambiguous = True

        best_match = top_matches[0] if (top_matches and top_matches[0]["score"] >= 0.6) else None

        return {
            "query": query,
            "matches": top_matches,
            "is_ambiguous": is_ambiguous,
            "best_match": best_match
        }

    @classmethod
    def get_medicine_monograph(cls, identifier: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves the complete pharmaceutical monograph for a given brand or generic name.
        """
        search_res = cls.search_medicines(identifier, limit=1)
        best = search_res.get("best_match")
        if not best:
            return None

        # Fetch full object from all meds
        all_meds = cls.get_all_medicines()
        for m in all_meds:
            if m["id"] == best["id"]:
                return m
        return None
