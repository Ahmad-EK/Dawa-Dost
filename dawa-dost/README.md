# Dawa Dost (دوا دوست) — Gemini-Powered Medical Intelligence Engine & Pharmaceutical Knowledge Platform for Pakistan

> **"یہ معلومات AI کی مدد سے دی گئی ہیں، ڈاکٹر کے مشورے کا متبادل نہیں۔"**  
> *"This information is AI-generated and is not a substitute for professional medical advice."*

---

## 1. Executive Summary

**Dawa Dost (دوا دوست)** is an AI-powered medicine, prescription explainer, and conversational digital healthcare companion specially engineered for the Pakistani population, with a dedicated focus on:

- **Elderly individuals** who require large visual hit areas, high contrast, and gentle spoken audio guidance.
- **Low-literacy patients** or individuals unfamiliar with cursive medical handwriting and English pharmaceutical packaging.
- **Family caregivers** managing chronic multi-drug regimens for elderly parents.
- **Patient safety**: Enforcing strict clinical guardrails against invented dosages, unrecognized diagnoses, or contraindicated combinations.

---

## 2. Major System Architecture & Components

```
                   USER INPUT (Camera / File / Preset / Chat)
                                      ↓
                   GEMINI MULTIMODAL VISION & OCR
               (Identifies Medicine, Strengths, Handwriting)
                                      ↓
                    MEDICINE KNOWLEDGE BASE SEARCH
            (Fuzzy Matching, Ambiguity Detection, Candidates)
                                      ↓
                  USER VERIFICATION (جی ہاں، درست ہے)
                                      ↓
      ┌──────────────────────────────────────────────────────────────┐
      │          RETRIEVAL-AUGMENTED GENERATION (RAG) PIPELINE       │
      │                                                              │
      │  1. Medicine Monograph (FDA, NHS, MedlinePlus, DRAP, WHO)    │
      │  2. Medical Condition Directory (T2D, HTN, Asthma, CKD, etc.)│
      │  3. Patient Health Profile (Allergies, Conditions, Regimen)  │
      │  4. Drug-Drug & Drug-Disease Interaction Checker             │
      │  5. Regulatory Discrepancy & Evidence Analysis               │
      └──────────────────────────────────────────────────────────────┘
                                      ↓
                        GEMINI DOCTOR PERSONA ENGINE
        (Warm Pakistani Physician Tone • Grounded in Monograph Facts)
                                      ↓
                       MEDICAL SAFETY & SCHEMA GUARDRAIL
         (No Invented Dosage • 6 Mandatory Sections • Emergency Banner)
                                      ↓
              TEXT + SECTION-BY-SECTION AUDIO PLAYBACK (0.85x)
                                      ↓
             CONVERSATIONAL MEDICAL ASSISTANT (FOLLOW-UP CHAT)
```

---

## 3. Implemented Modular Backend Services

The backend architecture is cleanly separated into specialized, decoupled modules:

1. **`GeminiService` (`backend/gemini_service.py`)**:
   - Central LLM and Multimodal Vision engine.
   - Grounded RAG explanation generator and multi-turn conversational follow-up assistant.
   - Configurable model via `GEMINI_MODEL` (default: `gemini-1.5-flash`), 30s timeout, exponential backoff retries, and JSON schema cleaner.
2. **`MedicineKnowledgeService` (`backend/medicine_knowledge_service.py`)**:
   - Authoritative pharmaceutical monograph search by brand name, generic name, active ingredients, and category.
   - Fuzzy matching algorithm tolerant to OCR errors, Pakistani brand variations, and typos.
   - Ambiguity detection: Flags multiple plausible candidates for patient confirmation instead of guessing.
3. **`MedicalConditionService` (`backend/medical_condition_service.py`)**:
   - Condition directory (Type 2 Diabetes, Hypertension, Bronchial Asthma, Peptic Ulcers/GERD, Chronic Kidney Disease, Liver Cirrhosis).
   - Disease-drug contraindication cross-matching (e.g. Pseudoephedrine in Hypertension, Beta-blockers in Asthma).
4. **`DrugInteractionService` (`backend/drug_interaction_service.py`)**:
   - Multi-drug regimen checker evaluating candidates against active medications.
   - Severity classification (`critical`, `moderate`, `mild`), clinical evidence rating, and actionable management in Urdu & English.
5. **`PatientContextService` (`backend/patient_context_service.py`)**:
   - Extracts privacy-conscious, minimal clinical context from persistent profiles.
   - Distinguishes user-confirmed information from unverified document findings.
6. **`MedicalSafetyService` (`backend/medical_safety_service.py`)**:
   - Enforces the strict rule against invented dosages: if prescription instructions are missing, guarantees *"خوراک واضح نہیں ہے۔ براہِ کرم ڈاکٹر یا فارماسسٹ سے تصدیق کریں۔"*
   - Cross-matches active ingredients against confirmed patient allergies (e.g. Penicillin group).
   - Validates response schemas to prevent malformed outputs from reaching the UI.
7. **`MedicalSourceService` (`backend/medical_source_service.py`)**:
   - Manages source attributions and detects regional regulatory discrepancies (e.g. US vs Pakistan formulation ratios, pediatric age thresholds).

---

## 4. Connected Medical References & Sources

Dawa Dost references Tier-1 regulatory and clinical evidence sources:

| Source | Jurisdiction | Role in Dawa Dost |
| :--- | :--- | :--- |
| **FDA Drug Safety Database** | United States | Official drug monographs, mechanism of action, and boxed warnings. |
| **NHS UK Medicines A-Z** | United Kingdom | Patient-centered administration guidance, food timing, and missed-dose rules. |
| **MedlinePlus (NIH / NLM)** | United States | Clinical precautions and patient health summaries. |
| **DRAP National Register** | Pakistan | Approved Pakistani brand names, available strengths, and local manufacturers. |
| **WHO Essential Medicines** | International | Global essential healthcare classifications and priority indications. |

---

## 5. Status of Application Features

| Feature | Implementation Status | Notes |
| :--- | :--- | :--- |
| **Structured Medicine Database** | **Fully Functional** | SQLite-backed pharmaceutical monographs with indications, precautions, side effects, and storage. |
| **Medical Condition Database** | **Fully Functional** | Pre-seeded with top Pakistani chronic conditions and contraindication rules. |
| **Fuzzy Search & Ambiguity Detection** | **Fully Functional** | Resolves typos, OCR variations, and returns candidate alternatives when ambiguous. |
| **Multimodal Vision OCR** | **Fully Functional** | Uses Gemini Vision when `GEMINI_API_KEY` is present, with offline Pakistani formulary fallback. |
| **RAG Grounded Explanations** | **Fully Functional** | Explanations are strictly grounded in retrieved database facts and patient context. |
| **Conversational Follow-Up Chat** | **Fully Functional** | Multi-turn dialogue with Doctor Sahib about the current medicine, with audio playback. |
| **Clinical Allergy Cross-Match** | **Fully Functional** | Detects Penicillin, Aspirin/NSAID, and Sulfa cross-hypersensitivities. |
| **Drug Interaction Checker** | **Fully Functional** | Compares against patient's active medications with severity ratings. |
| **Audio Speech Synthesis** | **Fully Functional** | Web Speech API speech synthesis at elderly-friendly `0.85x` pace in Urdu and English. |
| **Multi-Profile Family Memory** | **Fully Functional** | Isolated patient records for parents, spouses, and children in SQLite database. |

### Limitations & External Subscriptions:
- **Google Gemini API**: Dynamic multimodal vision and unconstrained AI text generation require a free API key from [Google AI Studio](https://aistudio.google.com/). When no key or network is present, the built-in local clinical formulary handles all core workflows offline.
- **Medical Advice Boundary**: Dawa Dost is an informational and explanatory companion; it explicitly disclaims diagnosing diseases or modifying prescriptions.

---

## 6. How to Run Locally

### Quick Launch (Windows)
Double-click [`run.bat`](file:///C:/Users/Rafey/.gemini/antigravity/scratch/dawa-dost/run.bat) or run from PowerShell:
```powershell
cd C:\Users\Rafey\.gemini\antigravity\scratch\dawa-dost
.\run.ps1
```
The browser will automatically open at:  
👉 **`http://localhost:8080`** *(or `http://127.0.0.1:8080`)*

---

## 7. Running the Automated Test Suite

To run all 19 automated tests validating the 13 clinical scenarios, RAG pipeline, ambiguity detection, and conversational assistant:
```powershell
& "C:\msys64\ucrt64\bin\python.exe" -m unittest discover -s "C:\Users\Rafey\.gemini\antigravity\scratch\dawa-dost\tests"
```
**Result**: 19 tests executed with 0 failures (`Ran 19 tests in 0.318s. OK`).
