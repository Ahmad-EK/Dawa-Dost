"""
Dawa Dost Database Layer (Expanded)
SQLite-backed persistent health memory, medication records, medical knowledge database,
authoritative clinical sources, conditions directory, and multi-turn conversational records.
"""

import os
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

from medical_knowledge_data import (
    MEDICAL_SOURCES_SEED,
    MEDICAL_CONDITIONS_SEED,
    MEDICINES_SEED,
    CLINICAL_DRUG_INTERACTIONS_SEED
)

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dawa_dost.db")


def get_db_connection():
    """Returns a connection to the SQLite database with row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    """Initializes the database schema and seeds initial Pakistani family profiles and medical knowledge."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Profiles table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        relationship TEXT DEFAULT 'self',
        age INTEGER,
        gender TEXT,
        language TEXT DEFAULT 'ur',
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. Medical conditions (patient recorded)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conditions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        profile_id INTEGER NOT NULL,
        name_ur TEXT NOT NULL,
        name_en TEXT NOT NULL,
        diagnosed_year TEXT,
        notes TEXT,
        FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
    );
    """)

    # 3. Allergies table (patient recorded)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS allergies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        profile_id INTEGER NOT NULL,
        allergen_ur TEXT NOT NULL,
        allergen_en TEXT NOT NULL,
        severity TEXT DEFAULT 'high',
        reaction TEXT,
        FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
    );
    """)

    # 4. Medicines table (patient scanned/saved)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        profile_id INTEGER NOT NULL,
        brand_name TEXT NOT NULL,
        generic_name TEXT,
        strength TEXT,
        formulation TEXT,
        instructions TEXT,
        instructions_ur TEXT,
        status TEXT DEFAULT 'active',
        image_path TEXT,
        scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        discontinued_at TIMESTAMP,
        FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
    );
    """)

    # 5. Explanations table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS explanations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        medicine_id INTEGER NOT NULL,
        language TEXT DEFAULT 'ur',
        purpose TEXT NOT NULL,
        how_to_take TEXT NOT NULL,
        precautions TEXT NOT NULL,
        side_effects TEXT NOT NULL,
        special_care TEXT NOT NULL,
        doctor_advisory TEXT NOT NULL,
        emergency_warning TEXT,
        personalized_warnings TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (medicine_id) REFERENCES medicines(id) ON DELETE CASCADE
    );
    """)

    # 6. Authoritative Medical Sources table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medical_sources (
        id INTEGER PRIMARY KEY,
        source_name TEXT NOT NULL,
        source_url TEXT NOT NULL,
        jurisdiction TEXT,
        reliability_score TEXT,
        retrieved_at TEXT,
        last_verified_at TEXT,
        notes TEXT
    );
    """)

    # 7. Medical Conditions Directory (Reference Knowledge)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medical_conditions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        condition_code TEXT UNIQUE,
        name_en TEXT NOT NULL,
        name_ur TEXT NOT NULL,
        alternative_names_json TEXT,
        description_en TEXT,
        description_ur TEXT,
        associated_drug_classes_json TEXT,
        contraindicated_drug_classes_json TEXT,
        precautions_en TEXT,
        precautions_ur TEXT,
        special_considerations_json TEXT
    );
    """)

    # 8. Structured Medical Knowledge Medicines (Pharmaceutical Knowledge Base)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medical_knowledge_medicines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        generic_name TEXT NOT NULL,
        brand_names_json TEXT NOT NULL,
        active_ingredients_json TEXT NOT NULL,
        pharmaceutical_class TEXT NOT NULL,
        drug_category TEXT NOT NULL,
        strengths_json TEXT NOT NULL,
        dosage_forms_json TEXT NOT NULL,
        manufacturers_json TEXT,
        general_uses_en TEXT NOT NULL,
        general_uses_ur TEXT NOT NULL,
        approved_indications_json TEXT,
        mechanism_of_action_en TEXT,
        mechanism_of_action_ur TEXT,
        precautions_en TEXT,
        precautions_ur TEXT,
        contraindications_json TEXT,
        common_side_effects_json TEXT,
        serious_adverse_reactions_json TEXT,
        food_interactions_json TEXT,
        storage_instructions_en TEXT,
        storage_instructions_ur TEXT,
        special_populations_json TEXT,
        administration_guidance_en TEXT,
        administration_guidance_ur TEXT,
        missed_dose_guidance_en TEXT,
        missed_dose_guidance_ur TEXT,
        overdose_warning_en TEXT,
        overdose_warning_ur TEXT,
        prescription_required BOOLEAN DEFAULT 1,
        source_id INTEGER,
        is_verified BOOLEAN DEFAULT 1,
        verification_notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (source_id) REFERENCES medical_sources(id)
    );
    """)

    # 9. Clinical Drug Interactions (Reference Knowledge)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clinical_drug_interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        drug_a_normalized TEXT NOT NULL,
        drug_b_normalized TEXT NOT NULL,
        severity TEXT NOT NULL,
        description_en TEXT NOT NULL,
        description_ur TEXT NOT NULL,
        clinical_management_en TEXT,
        clinical_management_ur TEXT,
        evidence_level TEXT,
        source_id INTEGER,
        FOREIGN KEY (source_id) REFERENCES medical_sources(id)
    );
    """)

    # 10. Multi-turn Conversational Messages table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversation_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        profile_id INTEGER NOT NULL,
        medicine_name TEXT,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
    );
    """)

    conn.commit()

    # Seed initial Pakistani family profiles if empty
    cursor.execute("SELECT COUNT(*) AS count FROM profiles;")
    if cursor.fetchone()["count"] == 0:
        seed_default_data(conn)

    # Seed medical knowledge if empty
    cursor.execute("SELECT COUNT(*) AS count FROM medical_sources;")
    if cursor.fetchone()["count"] == 0:
        seed_medical_knowledge(conn)

    conn.close()


def seed_default_data(conn):
    """Seeds authentic sample Pakistani profiles and medication records."""
    cursor = conn.cursor()

    # Profile 1: Haji Abdul Rehman (Elderly Father, 68)
    cursor.execute("""
    INSERT INTO profiles (name, relationship, age, gender, language, notes)
    VALUES (?, ?, ?, ?, ?, ?)
    """, ("حاجی عبد الرحمٰن", "والد صاحب (Father)", 68, "male", "ur", "مریض کو دل اور شوگر کا عارضہ ہے"))
    p1_id = cursor.lastrowid

    # Conditions for P1
    cursor.execute("""
    INSERT INTO conditions (profile_id, name_ur, name_en, diagnosed_year, notes)
    VALUES (?, ?, ?, ?, ?)
    """, (p1_id, "ذیابیطس نوع 2 (شوگر)", "Type 2 Diabetes", "2015", "خون میں شکر کی مقدار قابو میں رکھنی ضروری ہے"))

    cursor.execute("""
    INSERT INTO conditions (profile_id, name_ur, name_en, diagnosed_year, notes)
    VALUES (?, ?, ?, ?, ?)
    """, (p1_id, "بلند فشار خون (ہائی بلڈ پریشر)", "Hypertension", "2018", "روزانہ بی پی چیک کرنا ہوتا ہے"))

    # Allergy for P1: Penicillin (Crucial for interaction testing)
    cursor.execute("""
    INSERT INTO allergies (profile_id, allergen_ur, allergen_en, severity, reaction)
    VALUES (?, ?, ?, ?, ?)
    """, (p1_id, "پینسلین اور اینٹی بائیوٹک گروہ", "Penicillin & Beta-lactam Antibiotics", "severe", "جسم پر سرخ نشان، خارش اور سانس کی تنگی"))

    # Active Medicine for P1: Glucophage (Metformin)
    cursor.execute("""
    INSERT INTO medicines (profile_id, brand_name, generic_name, strength, formulation, instructions, instructions_ur, status, scanned_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (p1_id, "Glucophage", "Metformin HCl", "500mg", "Tablet (گولی)", 
          "Take 1 tablet at night after dinner with water.", 
          "رات کے کھانے کے بعد پانی کے ساتھ ایک گولی لیں۔", 
          "active", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    med1_id = cursor.lastrowid

    # Explanation for Glucophage
    cursor.execute("""
    INSERT INTO explanations (medicine_id, language, purpose, how_to_take, precautions, side_effects, special_care, doctor_advisory, emergency_warning, personalized_warnings)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        med1_id,
        "ur",
        "یہ دوا خون میں شکر (شوگر) کی مقدار کو معمول پر رکھنے میں مدد دیتی ہے۔ یہ جگر میں بننے والی شوگر کو کم کرتی ہے۔",
        "نسخے کے مطابق: رات کے کھانے کے بعد ایک گولی پانی کے ساتھ نگل لیں۔ گولی کو چبائیں نہیں۔ خالی پیٹ ہرگز نہ لیں۔",
        "کھانا وقت پر کھائیں تاکہ کمزوری نہ ہو۔ روزانہ مناسب مقدار میں پانی پئیں۔ اپنے معمول کی ورزش یا چہل قدمی جاری رکھیں۔",
        "شروع کے دنوں میں پیٹ میں ہلکا بوجھ، گیس یا متلی ہو سکتی ہے۔ کھانے کے ساتھ لینے سے یہ شکایتیں کم ہو جاتی ہیں۔",
        "گردوں یا جگر کی شدید تکلیف میں ڈاکٹر سے مشورہ ضروری ہے۔ اگر کوئی بڑا ٹیسٹ (جیسے سی ٹی اسکین مع کنٹراسٹ) کروانا ہو تو ڈاکٹر کو پہلے مطلع کریں۔",
        "میری آپ کو ایک ضروری بات: شوگر کی دوا کبھی بھی اپنی مرضی سے بند نہ کریں اور میٹھی چیزوں سے پرہیز جاری رکھیں۔ باقاعدگی سے شوگر چیک کرواتے رہیں۔",
        "اگر شدید کمزوری، غنودگی، سردی لگنا یا سانس لینے میں غیر معمولی دشواری ہو تو فوری طور پر اسپتال ایمرجنسی سے رابطہ کریں۔",
        json.dumps(["مریض کی ذیابیطس کی تاریخ سے مطابقت رکھتی ہے"])
    ))

    # Profile 2: Zubaida Begum (Elderly Mother, 64)
    cursor.execute("""
    INSERT INTO profiles (name, relationship, age, gender, language, notes)
    VALUES (?, ?, ?, ?, ?, ?)
    """, ("زبیدہ بیگم", "والدہ محترمہ (Mother)", 64, "female", "ur", "جوڑوں اور معدے کا مسئلہ ہے"))
    p2_id = cursor.lastrowid

    cursor.execute("""
    INSERT INTO conditions (profile_id, name_ur, name_en, diagnosed_year, notes)
    VALUES (?, ?, ?, ?, ?)
    """, (p2_id, "جوڑوں کا درد (گٹھیا)", "Osteoarthritis", "2020", "گھٹنوں میں درد رہتا ہے"))

    cursor.execute("""
    INSERT INTO conditions (profile_id, name_ur, name_en, diagnosed_year, notes)
    VALUES (?, ?, ?, ?, ?)
    """, (p2_id, "معدے کی تیزابیت اور جلن", "GERD / Acid Reflux", "2019", "مرچ مصالحے والی چیزوں سے تکلیف بڑھتی ہے"))

    # Allergy for P2: Aspirin / NSAIDs (Causes stomach bleed)
    cursor.execute("""
    INSERT INTO allergies (profile_id, allergen_ur, allergen_en, severity, reaction)
    VALUES (?, ?, ?, ?, ?)
    """, (p2_id, "ڈسپرین اور درد کش دوائیں (NSAIDs)", "Aspirin & NSAIDs (Brufen/Disprin)", "high", "معدے میں شدید درد اور تیزابیت کی شکایت"))

    cursor.execute("""
    INSERT INTO medicines (profile_id, brand_name, generic_name, strength, formulation, instructions, instructions_ur, status, scanned_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (p2_id, "Risek", "Omeprazole", "20mg", "Capsule (کیپسول)", 
          "Take 1 capsule in the morning on an empty stomach.", 
          "صبح ناشتے سے آدھا گھنٹہ پہلے نہار منہ ایک کیپسول لیں۔", 
          "active", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    conn.commit()


def seed_medical_knowledge(conn):
    """Seeds authoritative pharmaceutical monographs, sources, conditions, and interactions."""
    cursor = conn.cursor()

    # Seed Sources
    for src in MEDICAL_SOURCES_SEED:
        cursor.execute("""
        INSERT INTO medical_sources (id, source_name, source_url, jurisdiction, reliability_score, retrieved_at, last_verified_at, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            src["id"], src["source_name"], src["source_url"], src["jurisdiction"],
            src["reliability_score"], src["retrieved_at"], src["last_verified_at"], src["notes"]
        ))

    # Seed Conditions
    for cond in MEDICAL_CONDITIONS_SEED:
        cursor.execute("""
        INSERT INTO medical_conditions (
            condition_code, name_en, name_ur, alternative_names_json, description_en, description_ur,
            associated_drug_classes_json, contraindicated_drug_classes_json, precautions_en, precautions_ur,
            special_considerations_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            cond["condition_code"], cond["name_en"], cond["name_ur"],
            json.dumps(cond["alternative_names"], ensure_ascii=False),
            cond["description_en"], cond["description_ur"],
            json.dumps(cond["associated_drug_classes"], ensure_ascii=False),
            json.dumps(cond["contraindicated_drug_classes"], ensure_ascii=False),
            cond["precautions_en"], cond["precautions_ur"],
            json.dumps(cond["special_considerations"], ensure_ascii=False)
        ))

    # Seed Medicines
    for med in MEDICINES_SEED:
        cursor.execute("""
        INSERT INTO medical_knowledge_medicines (
            generic_name, brand_names_json, active_ingredients_json, pharmaceutical_class, drug_category,
            strengths_json, dosage_forms_json, manufacturers_json, general_uses_en, general_uses_ur,
            approved_indications_json, mechanism_of_action_en, mechanism_of_action_ur,
            precautions_en, precautions_ur, contraindications_json, common_side_effects_json,
            serious_adverse_reactions_json, food_interactions_json, storage_instructions_en, storage_instructions_ur,
            special_populations_json, administration_guidance_en, administration_guidance_ur,
            missed_dose_guidance_en, missed_dose_guidance_ur, overdose_warning_en, overdose_warning_ur,
            prescription_required, source_id, is_verified, verification_notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            med["generic_name"],
            json.dumps(med["brand_names"], ensure_ascii=False),
            json.dumps(med["active_ingredients"], ensure_ascii=False),
            med["pharmaceutical_class"],
            med["drug_category"],
            json.dumps(med["strengths"], ensure_ascii=False),
            json.dumps(med["dosage_forms"], ensure_ascii=False),
            json.dumps(med["manufacturers"], ensure_ascii=False),
            med["general_uses_en"], med["general_uses_ur"],
            json.dumps(med["approved_indications"], ensure_ascii=False),
            med["mechanism_of_action_en"], med["mechanism_of_action_ur"],
            med["precautions_en"], med["precautions_ur"],
            json.dumps(med["contraindications"], ensure_ascii=False),
            json.dumps(med["common_side_effects"], ensure_ascii=False),
            json.dumps(med["serious_adverse_reactions"], ensure_ascii=False),
            json.dumps(med["food_interactions"], ensure_ascii=False),
            med["storage_instructions_en"], med["storage_instructions_ur"],
            json.dumps(med["special_populations"], ensure_ascii=False),
            med["administration_guidance_en"], med["administration_guidance_ur"],
            med["missed_dose_guidance_en"], med["missed_dose_guidance_ur"],
            med["overdose_warning_en"], med["overdose_warning_ur"],
            1 if med["prescription_required"] else 0,
            med["source_id"],
            1 if med["is_verified"] else 0,
            med["verification_notes"]
        ))

    # Seed Interactions
    for inter in CLINICAL_DRUG_INTERACTIONS_SEED:
        cursor.execute("""
        INSERT INTO clinical_drug_interactions (
            drug_a_normalized, drug_b_normalized, severity, description_en, description_ur,
            clinical_management_en, clinical_management_ur, evidence_level, source_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            inter["drug_a_normalized"], inter["drug_b_normalized"], inter["severity"],
            inter["description_en"], inter["description_ur"],
            inter["clinical_management_en"], inter["clinical_management_ur"],
            inter["evidence_level"], inter["source_id"]
        ))

    conn.commit()


# --- Profile CRUD ---

def get_all_profiles() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profiles ORDER BY id ASC;")
    rows = cursor.fetchall()
    profiles = [dict(row) for row in rows]
    conn.close()
    return profiles


def get_profile_by_id(profile_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profiles WHERE id = ?;", (profile_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None
    
    profile = dict(row)

    # Fetch conditions
    cursor.execute("SELECT * FROM conditions WHERE profile_id = ?;", (profile_id,))
    profile["conditions"] = [dict(r) for r in cursor.fetchall()]

    # Fetch allergies
    cursor.execute("SELECT * FROM allergies WHERE profile_id = ?;", (profile_id,))
    profile["allergies"] = [dict(r) for r in cursor.fetchall()]

    # Fetch active medicines
    cursor.execute("SELECT * FROM medicines WHERE profile_id = ? ORDER BY id DESC;", (profile_id,))
    profile["medicines"] = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return profile


def create_profile(name: str, relationship: str = "خود", age: Optional[int] = None, gender: Optional[str] = None, language: str = "ur", notes: str = "") -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO profiles (name, relationship, age, gender, language, notes)
    VALUES (?, ?, ?, ?, ?, ?);
    """, (name, relationship, age, gender, language, notes))
    profile_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return profile_id


def update_profile(profile_id: int, name: str, relationship: str, age: Optional[int], gender: Optional[str], language: str, notes: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE profiles
    SET name = ?, relationship = ?, age = ?, gender = ?, language = ?, notes = ?
    WHERE id = ?;
    """, (name, relationship, age, gender, language, notes, profile_id))
    conn.commit()
    conn.close()


def delete_profile(profile_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM profiles WHERE id = ?;", (profile_id,))
    conn.commit()
    conn.close()


# --- Conditions & Allergies Management ---

def add_condition(profile_id: int, name_ur: str, name_en: str = "", diagnosed_year: str = "", notes: str = "") -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO conditions (profile_id, name_ur, name_en, diagnosed_year, notes)
    VALUES (?, ?, ?, ?, ?);
    """, (profile_id, name_ur, name_en or name_ur, diagnosed_year, notes))
    cond_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return cond_id


def delete_condition(condition_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM conditions WHERE id = ?;", (condition_id,))
    conn.commit()
    conn.close()


def add_allergy(profile_id: int, allergen_ur: str, allergen_en: str = "", severity: str = "high", reaction: str = "") -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO allergies (profile_id, allergen_ur, allergen_en, severity, reaction)
    VALUES (?, ?, ?, ?, ?);
    """, (profile_id, allergen_ur, allergen_en or allergen_ur, severity, reaction))
    allergy_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return allergy_id


def delete_allergy(allergy_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM allergies WHERE id = ?;", (allergy_id,))
    conn.commit()
    conn.close()


# --- Medicines & Explanations Management ---

def get_medicines_by_profile(profile_id: int, status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    if status_filter:
        cursor.execute("SELECT * FROM medicines WHERE profile_id = ? AND status = ? ORDER BY id DESC;", (profile_id, status_filter))
    else:
        cursor.execute("SELECT * FROM medicines WHERE profile_id = ? ORDER BY id DESC;", (profile_id,))
    rows = cursor.fetchall()
    meds = []
    for r in rows:
        m = dict(r)
        # Fetch latest explanation if present
        cursor.execute("SELECT * FROM explanations WHERE medicine_id = ? ORDER BY id DESC LIMIT 1;", (m["id"],))
        exp_row = cursor.fetchone()
        m["explanation"] = dict(exp_row) if exp_row else None
        meds.append(m)
    conn.close()
    return meds


def save_medicine(profile_id: int, brand_name: str, generic_name: str, strength: str, formulation: str, instructions: str, instructions_ur: str, status: str = "active", image_path: str = "") -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO medicines (profile_id, brand_name, generic_name, strength, formulation, instructions, instructions_ur, status, image_path)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (profile_id, brand_name, generic_name, strength, formulation, instructions, instructions_ur, status, image_path))
    med_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return med_id


def update_medicine_status(medicine_id: int, status: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    discontinued_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if status == "discontinued" else None
    cursor.execute("""
    UPDATE medicines
    SET status = ?, discontinued_at = COALESCE(?, discontinued_at)
    WHERE id = ?;
    """, (status, discontinued_at, medicine_id))
    conn.commit()
    conn.close()


def delete_medicine(medicine_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM medicines WHERE id = ?;", (medicine_id,))
    conn.commit()
    conn.close()


def save_explanation(medicine_id: int, language: str, purpose: str, how_to_take: str, precautions: str, side_effects: str, special_care: str, doctor_advisory: str, emergency_warning: str = "", personalized_warnings: List[str] = None) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    pw_json = json.dumps(personalized_warnings or [], ensure_ascii=False)
    cursor.execute("""
    INSERT INTO explanations (medicine_id, language, purpose, how_to_take, precautions, side_effects, special_care, doctor_advisory, emergency_warning, personalized_warnings)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (medicine_id, language, purpose, how_to_take, precautions, side_effects, special_care, doctor_advisory, emergency_warning, pw_json))
    exp_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return exp_id


def get_medicine_with_explanation(medicine_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicines WHERE id = ?;", (medicine_id,))
    med_row = cursor.fetchone()
    if not med_row:
        conn.close()
        return None
    med = dict(med_row)
    cursor.execute("SELECT * FROM explanations WHERE medicine_id = ? ORDER BY id DESC LIMIT 1;", (medicine_id,))
    exp_row = cursor.fetchone()
    if exp_row:
        med["explanation"] = dict(exp_row)
        if med["explanation"].get("personalized_warnings"):
            try:
                med["explanation"]["personalized_warnings"] = json.loads(med["explanation"]["personalized_warnings"])
            except:
                pass
    else:
        med["explanation"] = None
    conn.close()
    return med


# ==========================================================================
# MEDICAL KNOWLEDGE & SOURCES QUERY SERVICES
# ==========================================================================

def get_all_medical_sources() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medical_sources ORDER BY id ASC;")
    rows = cursor.fetchall()
    sources = [dict(r) for r in rows]
    conn.close()
    return sources


def get_medical_source_by_id(source_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medical_sources WHERE id = ?;", (source_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_all_medical_conditions() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medical_conditions ORDER BY id ASC;")
    rows = cursor.fetchall()
    conditions = []
    for r in rows:
        c = dict(r)
        c["alternative_names"] = json.loads(c.get("alternative_names_json") or "[]")
        c["associated_drug_classes"] = json.loads(c.get("associated_drug_classes_json") or "[]")
        c["contraindicated_drug_classes"] = json.loads(c.get("contraindicated_drug_classes_json") or "[]")
        c["special_considerations"] = json.loads(c.get("special_considerations_json") or "[]")
        conditions.append(c)
    conn.close()
    return conditions


def get_all_knowledge_medicines() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT m.*, s.source_name, s.source_url, s.jurisdiction
    FROM medical_knowledge_medicines m
    LEFT JOIN medical_sources s ON m.source_id = s.id
    ORDER BY m.id ASC;
    """)
    rows = cursor.fetchall()
    medicines = []
    for r in rows:
        m = dict(r)
        m["brand_names"] = json.loads(m.get("brand_names_json") or "[]")
        m["active_ingredients"] = json.loads(m.get("active_ingredients_json") or "[]")
        m["strengths"] = json.loads(m.get("strengths_json") or "[]")
        m["dosage_forms"] = json.loads(m.get("dosage_forms_json") or "[]")
        m["manufacturers"] = json.loads(m.get("manufacturers_json") or "[]")
        m["approved_indications"] = json.loads(m.get("approved_indications_json") or "[]")
        m["contraindications"] = json.loads(m.get("contraindications_json") or "[]")
        m["common_side_effects"] = json.loads(m.get("common_side_effects_json") or "[]")
        m["serious_adverse_reactions"] = json.loads(m.get("serious_adverse_reactions_json") or "[]")
        m["food_interactions"] = json.loads(m.get("food_interactions_json") or "[]")
        m["special_populations"] = json.loads(m.get("special_populations_json") or "{}")
        medicines.append(m)
    conn.close()
    return medicines


def get_clinical_drug_interactions() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT i.*, s.source_name, s.source_url
    FROM clinical_drug_interactions i
    LEFT JOIN medical_sources s ON i.source_id = s.id;
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# Multi-turn Conversational Memory Management
def save_conversation_message(session_id: str, profile_id: int, medicine_name: str, role: str, content: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO conversation_messages (session_id, profile_id, medicine_name, role, content)
    VALUES (?, ?, ?, ?, ?);
    """, (session_id, profile_id, medicine_name, role, content))
    conn.commit()
    conn.close()


def get_conversation_history(session_id: str, limit: int = 20) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT role, content, created_at
    FROM conversation_messages
    WHERE session_id = ?
    ORDER BY id ASC
    LIMIT ?;
    """, (session_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]
