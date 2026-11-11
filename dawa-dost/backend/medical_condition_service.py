"""
Dawa Dost Medical Condition Service
Maintains the medical conditions directory, resolves clinical synonyms,
and evaluates disease-drug contraindications and precautions.
"""

from typing import List, Dict, Any, Optional
import database


class MedicalConditionService:
    """Provides disease context and verifies condition-drug contraindications."""

    @classmethod
    def get_all_conditions(cls) -> List[Dict[str, Any]]:
        """Returns all reference medical conditions."""
        return database.get_all_medical_conditions()

    @classmethod
    def find_condition_by_name(cls, query: str) -> Optional[Dict[str, Any]]:
        """Finds a medical condition using English, Urdu, or alternative names."""
        if not query:
            return None
        q = query.lower().strip()
        conditions = cls.get_all_conditions()
        for cond in conditions:
            if q == cond["condition_code"].lower() or q in cond["name_en"].lower() or q in cond["name_ur"]:
                return cond
            for alt in cond.get("alternative_names", []):
                if q in alt.lower() or alt.lower() in q:
                    return cond
        return None

    @classmethod
    def evaluate_condition_safety(cls, drug_monograph: Dict[str, Any], patient_conditions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Cross-checks candidate drug's pharmacological class and active ingredients
        against the patient's confirmed medical conditions.
        """
        findings = []
        if not drug_monograph or not patient_conditions:
            return findings

        drug_class = drug_monograph.get("pharmaceutical_class", "").lower()
        drug_name = drug_monograph.get("generic_name", "").lower()
        for b in drug_monograph.get("brand_names", []):
            drug_name += f" {b.lower()}"

        for cond_entry in patient_conditions:
            cond_text = f"{cond_entry.get('name_en', '')} {cond_entry.get('name_ur', '')}".lower()
            ref_cond = cls.find_condition_by_name(cond_entry.get("name_en", "")) or cls.find_condition_by_name(cond_entry.get("name_ur", ""))

            # 1. Hypertension checks (Decongestants, NSAIDs)
            if "hypertension" in cond_text or "بلند فشار" in cond_text or "ہائی بلڈ" in cond_text:
                if "pseudoephedrine" in drug_name or "arinac" in drug_name:
                    findings.append({
                        "condition": "Hypertension (ہائی بلڈ پریشر)",
                        "severity": "critical",
                        "message_en": "CRITICAL CONTRAINDICATION: Pseudoephedrine stimulates alpha-adrenergic receptors, causing vasoconstriction that dangerously spikes blood pressure and heart rate.",
                        "message_ur": "⚠️ خطرناک ممانعت: اس دوا میں موجود ڈی کنجسٹنٹ (سیوڈو ایفیڈرین) شریانوں کو سکیڑ کر بلڈ پریشر اور نبض کی رفتار کو خطرناک حد تک بڑھا دیتا ہے۔",
                        "clinical_guidance_en": "Do not administer. Recommend saline nasal spray or non-sympathomimetic alternatives.",
                        "clinical_guidance_ur": "ہائی بلڈ پریشر کے مریض نزلہ زکام کی اس دوا سے سختی سے پرہیز کریں۔"
                    })
                elif "ibuprofen" in drug_name or "brufen" in drug_name or "nsaid" in drug_class:
                    findings.append({
                        "condition": "Hypertension (ہائی بلڈ پریشر)",
                        "severity": "moderate",
                        "message_en": "NSAIDs cause renal prostaglandin inhibition leading to sodium retention and blunting of antihypertensive medication efficacy.",
                        "message_ur": "درد کش دوائیں (NSAIDs) نمکیات روک کر بلڈ پریشر کی دواؤں کے اثر کو کم کر سکتی ہیں۔ کثرتِ استعمال سے گریز کریں۔",
                        "clinical_guidance_en": "Monitor blood pressure if short-term therapy is essential.",
                        "clinical_guidance_ur": "اگر لینا ناگزیر ہو تو بلڈ پریشر باقاعدگی سے چیک کرتے رہیں۔"
                    })

            # 2. Asthma checks (Beta-blockers, Aspirin)
            if "asthma" in cond_text or "دمہ" in cond_text or "wheez" in cond_text:
                if "atenolol" in drug_name or "tenormin" in drug_name or "beta" in drug_class:
                    findings.append({
                        "condition": "Asthma (دمہ)",
                        "severity": "critical",
                        "message_en": "CRITICAL CONTRAINDICATION: Beta-blockers antagonize bronchial beta-2 receptors, precipitating severe or fatal bronchospasm in asthma patients.",
                        "message_ur": "⚠️ انتہائی خطرناک: بیٹا بلاکرز سانس کی نالیوں کو سکیڑ کر دم گھٹنے کا شدید دورہ پیدا کر سکتے ہیں، دمہ کے مریضوں میں یہ سختی سے ممنوع ہیں۔",
                        "clinical_guidance_en": "Beta-blocker strictly contraindicated. Alternative antihypertensive classes (e.g. ARBs, CCBs) required.",
                        "clinical_guidance_ur": "دمہ کے مریض یہ دوا ہرگز نہ لیں؛ معالج سے متبادل بی پی کی دوا تجویز کروائیں۔"
                    })
                elif "aspirin" in drug_name or "disprin" in drug_name:
                    findings.append({
                        "condition": "Asthma (دمہ)",
                        "severity": "moderate",
                        "message_en": "Aspirin can trigger acute bronchoconstriction in patients with Aspirin-Exacerbated Respiratory Disease (AERD).",
                        "message_ur": "دمہ کے بعض مریضوں میں اسپرین شدید سانس کی تنگی اور کھانسی کا سبب بن سکتی ہے۔",
                        "clinical_guidance_en": "Verify if patient has tolerated salicylates previously.",
                        "clinical_guidance_ur": "اگر پہلے کبھی اسپرین سے سانس خراب ہوا ہو تو ہرگز نہ لیں۔"
                    })

            # 3. Peptic Ulcer & GERD checks (NSAIDs, Aspirin)
            if "ulcer" in cond_text or "gerd" in cond_text or "تیزابیت" in cond_text or "السر" in cond_text:
                if "aspirin" in drug_name or "disprin" in drug_name or "ibuprofen" in drug_name or "nsaid" in drug_class:
                    findings.append({
                        "condition": "Peptic Ulcer & Acid Reflux (معدے کا السر اور تیزابیت)",
                        "severity": "high",
                        "message_en": "HIGH RISK: NSAIDs and Aspirin inhibit protective gastric mucosal prostaglandins, dramatically increasing ulcer perforation and bleeding risks.",
                        "message_ur": "⚠️ شدید احتیاط: یہ درد کش دوا معدے کی حفاظتی جھلی کو نقصان پہنچاتی ہے اور السر میں سے خون رسنے کا خطرہ پیدا کرتی ہے۔",
                        "clinical_guidance_en": "Avoid or co-prescribe with a gastroprotective agent (PPI like Omeprazole) strictly after food.",
                        "clinical_guidance_ur": "خالی پیٹ ہرگز نہ لیں؛ بہتر ہے کہ معدے کے السر کے مریض پیراسیٹامول کا استعمال کریں۔"
                    })

            # 4. Chronic Kidney Disease checks (Metformin, NSAIDs)
            if "kidney" in cond_text or "renal" in cond_text or "گردے" in cond_text:
                if "metformin" in drug_name or "glucophage" in drug_name:
                    findings.append({
                        "condition": "Chronic Kidney Disease (گردوں کا عارضہ)",
                        "severity": "high",
                        "message_en": "WARNING: Metformin is cleared renally; accumulation in moderate-to-severe renal impairment significantly heightens lactic acidosis risk.",
                        "message_ur": "⚠️ احتیاط: گردے کمزور ہونے کی صورت میں میٹفارمین جسم میں جمع ہو سکتی ہے۔ ڈاکٹر کی ہدایت کے مطابق خوراک کم رکھنا یا روکنا ضروری ہے۔",
                        "clinical_guidance_en": "Check recent eGFR. Contraindicated if eGFR < 30 mL/min.",
                        "clinical_guidance_ur": "گردوں کے فنکشن کا ٹیسٹ (eGFR) باقاعدگی سے کروائیں۔"
                    })

        return findings
