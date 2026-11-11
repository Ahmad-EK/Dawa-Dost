"""
Dawa Dost Drug Knowledge Base & Clinical Interaction Checker
Specially curated for the Pakistani pharmaceutical ecosystem and patient demographics.
Provides verified drug facts, allergy cross-matching, and drug-disease/drug-drug interaction checking.
"""

from typing import Dict, List, Any, Optional

# Verified Drug Knowledge Base for commonly prescribed Pakistani medications
PAKISTAN_DRUG_DATABASE: Dict[str, Dict[str, Any]] = {
    "augmentin": {
        "brand_name": "Augmentin",
        "generic_name": "Amoxicillin + Clavulanic Acid",
        "drug_class": "Penicillin-class Antibiotic (پینسلین اینٹی بائیوٹک)",
        "common_strengths": ["375mg", "625mg", "1g", "156mg/5ml", "312mg/5ml"],
        "formulations": ["Tablet (گولی)", "Syrup / Suspension (شربت)"],
        "purpose_ur": "یہ دوا بیکٹیریا سے ہونے والے انفیکشن (جیسے گلے، سینے، کان، پیشاب یا جلد کی سوزش) کے علاج کے لیے استعمال ہوتی ہے۔ یہ بیکٹیریا کا خاتمہ کرتی ہے۔",
        "purpose_en": "Augmentin is an antibiotic used to treat bacterial infections such as throat, chest, ear, skin, and urinary tract infections.",
        "how_to_take_guidance_ur": "ڈاکٹر کے بتائے ہوئے وقت پر لیں۔ عموماً کھانے کے آغاز میں لینے سے پیٹ کی خرابی نہیں ہوتی۔ کورس پورا کرنا لازمی ہے، خود سے جلدی بند نہ کریں۔",
        "how_to_take_guidance_en": "Take at the start of a meal to reduce stomach upset. Complete the full course prescribed by your doctor even if you feel better.",
        "precautions_ur": "اگر اسہال یا پیٹ خراب ہو تو وافر پانی پیئیں۔ دوا کا کورس درمیان میں نہ چھوڑیں ورنہ بیکٹیریا میں مدافعت پیدا ہو جاتی ہے۔",
        "precautions_en": "Drink plenty of fluids. Do not stop treatment early as bacterial resistance may develop.",
        "side_effects_ur": "عام اثرات میں پتلے پاخانے (دست)، پیٹ میں ہلکا درد یا متلی شامل ہیں۔ یہ عموماً کورس ختم ہونے پر ٹھیک ہو جاتے ہیں۔",
        "side_effects_en": "Common side effects include loose stools, mild nausea, and stomach upset.",
        "special_care_ur": "جن لوگوں کو پینسلین یا اینٹی بائیوٹک سے الرجی ہو، یا جنہیں جگر کا عارضہ رہا ہو، وہ یہ دوا ہرگز نہ لیں۔",
        "special_care_en": "Contraindicated in individuals with a history of penicillin allergy or severe liver dysfunction.",
        "doctor_advisory_ur": "میری آپ کو ایک ضروری بات: یہ اینٹی بائیوٹک ہے۔ عام نزلہ زکام یا وائرل بخار میں یہ دوا کام نہیں کرتی۔ ہمیشہ اپنے ڈاکٹر کے مشورے سے مقررہ دنوں کا کورس مکمل کریں۔",
        "doctor_advisory_en": "Doctor's note: This is an antibiotic and does not treat viral colds. Always finish the exact duration prescribed by your physician.",
        "allergy_triggers": ["penicillin", "amoxicillin", "ampicillin", "beta-lactam", "پینسلین"],
        "disease_contraindications": {
            "liver": "جگر کے مریضوں میں احتیاط ضروری ہے کیونکہ کلاوولینک ایسڈ جگر پر اثر انداز ہو سکتا ہے۔",
            "kidney": "گردوں کی شدید تکلیف میں خوراک کو کم کرنا ضروری ہوتا ہے۔"
        }
    },
    "panadol": {
        "brand_name": "Panadol",
        "generic_name": "Paracetamol (Acetaminophen)",
        "drug_class": "Analgesic & Antipyretic (درد کش اور بخار کی دوا)",
        "common_strengths": ["500mg", "665mg (Extend)", "120mg/5ml", "160mg/5ml (Drops)"],
        "formulations": ["Tablet (گولی)", "Syrup (شربت)", "Suspension / Drops (قطرے)"],
        "purpose_ur": "یہ دوا ہلکے سے درمیانے درد (جیسے سر درد، دانت درد، پٹھوں کا درد) اور بخار کو کم کرنے کے لیے استعمال کی جاتی ہے۔",
        "purpose_en": "Panadol is used for the relief of mild to moderate pain (headache, body aches, toothache) and reduction of fever.",
        "how_to_take_guidance_ur": "کھانے کے بعد یا پہلے پانی کے ساتھ لی جا سکتی ہے۔ بالغ افراد کے لیے ایک وقت میں ایک یا دو گولیاں، کم از کم 4 سے 6 گھنٹے کے وقفے سے۔ 24 گھنٹے میں 8 گولیوں (4 گرام) سے زیادہ ہرگز نہ لیں۔",
        "how_to_take_guidance_en": "Take with water. Adults: 1-2 tablets every 4 to 6 hours as needed. Never exceed 4000mg (8 tablets) in 24 hours.",
        "precautions_ur": "ایک ہی وقت میں پیراسیٹامول والی دیگر دوائیں (جیسے کولڈ اینڈ فلو ساشے یا کف سیرپ) نہ لیں تاکہ زیادہ مقدار نہ ہو۔",
        "precautions_en": "Avoid combining with other paracetamol-containing medications to prevent accidental overdose.",
        "side_effects_ur": "تجویز کردہ خوراک میں یہ دوا نہایت محفوظ ہے اور اس کے مضر اثرات شاذ و نادر ہی ہوتے ہیں۔",
        "side_effects_en": "Rare at recommended doses. High doses can cause severe liver damage.",
        "special_care_ur": "جگر کے دائمی مریض یا وہ لوگ جو بہت کمزور یا پانی کی کمی کا شکار ہوں، وہ ڈاکٹر کے بتائے بغیر نہ لیں۔",
        "special_care_en": "Patients with chronic liver disease or severe malnutrition should consult a doctor before use.",
        "doctor_advisory_ur": "میری آپ کو ایک ضروری بات: اگر بخار 3 دن سے زیادہ رہے یا درد ٹھیک نہ ہو تو خود سے گولیاں کھاتے رہنے کے بجائے فوراً ڈاکٹر سے رجوع کریں۔",
        "doctor_advisory_en": "Doctor's note: If fever lasts more than 3 days, do not self-medicate continuously; see a doctor.",
        "allergy_triggers": ["paracetamol", "acetaminophen", "پیراسیٹامول"],
        "disease_contraindications": {
            "liver": "جگر کے امراض میں پیراسیٹامول کی زیادہ خوراک جان لیوا ثابت ہو سکتی ہے۔"
        }
    },
    "glucophage": {
        "brand_name": "Glucophage",
        "generic_name": "Metformin Hydrochloride",
        "drug_class": "Biguanide Antidiabetic (شوگر کنٹرول کرنے والی دوا)",
        "common_strengths": ["500mg", "850mg", "1000mg", "500mg XR", "1000mg XR"],
        "formulations": ["Tablet (گولی)", "Extended Release Tablet (دیرپا اثر گولی)"],
        "purpose_ur": "یہ دوا نوع 2 کی ذیابیطس (شوگر) کے مریضوں میں خون میں شوگر کی مقدار کو متوازن رکھنے کے لیے استعمال کی جاتی ہے۔",
        "purpose_en": "Glucophage is an oral antihyperglycemic medication used to control high blood sugar in type 2 diabetes.",
        "how_to_take_guidance_ur": "کھانے کے دوران یا فوری بعد پانی کے ساتھ لیں۔ XR گولی کو توڑیں یا چبائیں نہیں، بلکہ ثابت نگلیں۔",
        "how_to_take_guidance_en": "Take with or right after meals to minimize stomach upset. Swallow XR tablets whole without crushing or chewing.",
        "precautions_ur": "شوگر باقاعدگی سے چیک کریں۔ اگر اسہال، الٹیاں یا شدید پانی کی کمی ہو تو ڈاکٹر کو بتائیں۔",
        "precautions_en": "Monitor blood glucose. Inform your doctor if you experience severe vomiting, dehydration, or diarrhea.",
        "side_effects_ur": "پیٹ میں خرابی، متلی، بھوک میں کمی یا منہ کا ذائقہ دھاتی ہونا۔ یہ شکایتیں عموماً کھانے کے ساتھ دوا لینے سے کم ہو جاتی ہیں۔",
        "side_effects_en": "Gastrointestinal disturbances (nausea, loose stools, bloating, metallic taste). Usually improves over time.",
        "special_care_ur": "گردوں کے مریضوں، دل کی شدید کمزوری یا اگر کوئی بڑا آپریشن یا سی ٹی اسکین کنٹراسٹ والا ہونا ہو تو یہ دوا عارضی طور پر روکی جاتی ہے۔",
        "special_care_en": "Contraindicated in severe renal impairment (eGFR < 30). Must be temporarily paused before iodinated contrast scans.",
        "doctor_advisory_ur": "میری آپ کو ایک ضروری بات: شوگر کی دوا لینے کے ساتھ ساتھ صبح کی چہل قدمی اور میٹھے و چکنائی والے کھانوں سے پرہیز اتنی ہی ضروری ہے جتنا یہ گولی۔",
        "doctor_advisory_en": "Doctor's note: Medication must be paired with daily walking and dietary portion control for optimal diabetes control.",
        "allergy_triggers": ["metformin", "glucophage", "میٹفارمین"],
        "disease_contraindications": {
            "kidney": "گردے کمزور ہونے پر میٹفارمین جسم میں جمع ہو کر لیکٹک ایسڈوسس کا خطرہ بنا سکتی ہے، لہٰذا ڈاکٹر کی نگرانی لازمی ہے۔",
            "heart": "شدید ہارٹ فیلیئر میں احتیاط درکار ہے۔"
        }
    },
    "disprin": {
        "brand_name": "Disprin",
        "generic_name": "Aspirin (Acetylsalicylic Acid)",
        "drug_class": "NSAID & Antiplatelet (درد کش اور خون پتلا کرنے والی دوا)",
        "common_strengths": ["300mg", "75mg (Loprin/Cardio-aspirin)"],
        "formulations": ["Soluble Tablet (پانی میں حل ہونے والی گولی)", "Enteric Coated Tablet"],
        "purpose_ur": "سر درد، دانت درد اور بخار میں فوری آرام کے لیے، اور کم مقدار (75 ملی گرام) میں دل کے دورے اور فالج سے بچاؤ کے لیے خون پتلا کرنے کے لیے استعمال ہوتی ہے۔",
        "purpose_en": "Disprin is used for rapid pain and fever relief, and at low doses (75mg) as a blood thinner to prevent heart attacks and strokes.",
        "how_to_take_guidance_ur": "ڈسپرین 300 ملی گرام گولی کو آدھے گلاس پانی میں گھول کر کھانے کے بعد پئیں۔ خالی پیٹ ہرگز نہ لیں۔",
        "how_to_take_guidance_en": "Dissolve in half a glass of water and drink immediately after food. Never take on an empty stomach.",
        "precautions_ur": "معدے میں تیزابیت پیدا کر سکتی ہے۔ اگر پاخانے کا رنگ سیاہ ہو جائے یا معدے میں جلن ہو تو فوری طور پر بند کر دیں۔",
        "precautions_en": "May irritate the stomach lining. Stop immediately and seek help if dark/black stools or severe epigastric pain occurs.",
        "side_effects_ur": "معدے میں جلن، متلی، سینے کی جلن، اور چوٹ لگنے پر خون زیادہ دیر بہنا۔",
        "side_effects_en": "Stomach burning, dyspepsia, increased tendency to bleed, and easy bruising.",
        "special_care_ur": "جن لوگوں کو معدے کا السر ہو، دمے کا مرض ہو، یا خون بہنے کی بیماری ہو، وہ یہ دوا نہ لیں۔ بچوں کو وائرل بخار میں ہرگز نہ دیں۔",
        "special_care_en": "Contraindicated in active peptic ulcer disease, bleeding disorders, asthma triggered by NSAIDs, and children with viral illness (Reye's syndrome risk).",
        "doctor_advisory_ur": "میری آپ کو ایک ضروری بات: اگر آپ پہلے سے خون پتلا کرنے والی کوئی دوا لے رہے ہیں، یا آپ کو معدے میں السر کی تاریخ ہے، تو ڈسپرین لینے سے پہلے ڈاکٹر سے تصدیق ضرور کریں۔",
        "doctor_advisory_en": "Doctor's note: If you have a history of stomach ulcers or are taking anticoagulants, never take Disprin without clinical clearance.",
        "allergy_triggers": ["aspirin", "acetylsalicylic acid", "nsaids", "اسپرین", "ڈسپرین"],
        "disease_contraindications": {
            "ulcer": "معدے کے السر میں اسپرین معدے سے شدید خون بہنے (بلیڈنگ) کا باعث بن سکتی ہے۔",
            "asthma": "دمہ کے مریضوں میں برونکوسپیزم اور سانس کی بندش کر سکتی ہے۔",
            "bleeding": "خون پتلا کرنے والی بیماریوں میں ممنوع ہے۔"
        }
    },
    "arinac": {
        "brand_name": "Arinac",
        "generic_name": "Ibuprofen + Pseudoephedrine HCl",
        "drug_class": "NSAID Decongestant (نزلہ زکام اور بند ناک کی دوا)",
        "common_strengths": ["200mg/30mg (Arinac)", "400mg/60mg (Arinac Forte)"],
        "formulations": ["Tablet (گولی)", "Suspension (شربت)"],
        "purpose_ur": "یہ دوا شدید نزلہ، زکام، بند ناک، سر درد اور بخار کی علامات سے وقتی نجات کے لیے استعمال کی جاتی ہے۔",
        "purpose_en": "Arinac combines an anti-inflammatory painkiller (Ibuprofen) with a nasal decongestant (Pseudoephedrine) for cold, sinusitis, and blocked nose relief.",
        "how_to_take_guidance_ur": "کھانے کے بعد پانی کے ساتھ لیں۔ خالی پیٹ نہ لیں۔ شام کے بعد دیر سے لینے پر نیند اڑ سکتی ہے۔",
        "how_to_take_guidance_en": "Take after a meal with a full glass of water. Avoid taking late at night as it may cause restlessness or insomnia.",
        "precautions_ur": "یہ دوا بلڈ پریشر کو تیزی سے بڑھا سکتی ہے اور دل کی دھڑکن تیز کر سکتی ہے۔ 5 دن سے زیادہ لگاتار استعمال نہ کریں۔",
        "precautions_en": "Significantly elevates blood pressure and heart rate. Do not use for more than 5 consecutive days without medical supervision.",
        "side_effects_ur": "گھبراہٹ، دل کی دھڑکن تیز ہونا، بلڈ پریشر بڑھنا، معدے میں بوجھ، بے خوابی۔",
        "side_effects_en": "Palpitations, hypertension, insomnia, nervousness, dizziness, and stomach irritation.",
        "special_care_ur": "ہائی بلڈ پریشر، دل کے امراض، کالے موتیے (گلاکوما) یا پروسٹیٹ کے مریضوں کے لیے یہ دوا خطرناک ہو سکتی ہے۔",
        "special_care_en": "Strongly contraindicated in hypertension, ischemic heart disease, glaucoma, and severe renal failure.",
        "doctor_advisory_ur": "میری آپ کو ایک ضروری بات: اگر آپ کو بلڈ پریشر کی بیماری ہے تو عام نزلہ زکام میں 'ایرینیک' جیسی دوا ہرگز نہ لیں۔ اس میں موجود مادہ آپ کا بی پی خطرناک حد تک بڑھا سکتا ہے۔",
        "doctor_advisory_en": "Doctor's note: If you have high blood pressure, do NOT take Arinac; Pseudoephedrine can cause severe blood pressure spikes.",
        "allergy_triggers": ["ibuprofen", "pseudoephedrine", "nsaids", "ایرینیک", "بروفن"],
        "disease_contraindications": {
            "hypertension": "ہائی بلڈ پریشر کے مریضوں میں یہ دوا بی پی اور دل کی دھڑکن کو خطرناک حد تک بڑھا دیتی ہے۔",
            "heart": "دل کے مریضوں کے لیے سخت احتیاط ضروری ہے۔",
            "glaucoma": "کالے موتیے کے مریضوں میں آنکھ کا دباؤ بڑھا سکتی ہے۔"
        }
    },
    "tenormin": {
        "brand_name": "Tenormin",
        "generic_name": "Atenolol",
        "drug_class": "Beta-Blocker (بلڈ پریشر اور دل کی دھڑکن کنٹرول کرنے والی دوا)",
        "common_strengths": ["25mg", "50mg", "100mg"],
        "formulations": ["Tablet (گولی)"],
        "purpose_ur": "یہ دوا ہائی بلڈ پریشر کو کم کرنے، سینے کے درد (انجائنا) کو روکنے اور دل کی غیر متوازن دھڑکن کو معمول پر لانے کے لیے استعمال کی جاتی ہے۔",
        "purpose_en": "Tenormin is a beta-blocker prescribed for hypertension, angina pectoris, and cardiac arrhythmias.",
        "how_to_take_guidance_ur": "روزانہ ایک مقررہ وقت پر (عموماً صبح) پانی کے ساتھ لیں۔ ڈاکٹر کے مشورے کے بغیر اچانک بند نہ کریں، ورنہ بی پی اچانک بڑھ سکتا ہے۔",
        "how_to_take_guidance_en": "Take once daily at the same time every morning. Do not stop abruptly as rebound hypertension or angina may occur.",
        "precautions_ur": "دل کی نبض اور بی پی وقتاً فوقتاً چیک کرتے رہیں۔ اچانک کھڑے ہونے پر چکر آ سکتے ہیں، آہستہ اٹھیں۔",
        "precautions_en": "Monitor pulse and blood pressure. Rise slowly from sitting or lying positions to avoid orthostatic dizziness.",
        "side_effects_ur": "ہاتھ پاؤں کا ٹھنڈا رہنا، تھکن، سست نبض (بریڈی کارڈیا) اور چکر آنا۔",
        "side_effects_en": "Cold extremities, fatigue, slow heart rate, and lightheadedness.",
        "special_care_ur": "دمہ کے مریض، سست نبض والے یا جن کا بلڈ پریشر پہلے سے کم رہتا ہو وہ یہ دوا نہ لیں۔ شوگر کے مریضوں میں یہ کم شوگر کی علامات (جیسے دھڑکن تیز ہونا) کو چھپا سکتی ہے۔",
        "special_care_en": "Contraindicated in bronchial asthma, severe bradycardia, and cardiogenic shock. Can mask hypoglycemia tachycardia in diabetics.",
        "doctor_advisory_ur": "میری آپ کو ایک ضروری بات: بلڈ پریشر کی اس دوا کو باقاعدگی سے لینا ضروری ہے۔ اگر نبض کی رفتار 50 سے کم ہو جائے یا شدید سستی محسوس ہو تو ڈاکٹر سے فوری رابطہ کریں۔",
        "doctor_advisory_en": "Doctor's note: Take consistently. If resting heart rate drops below 50 bpm or extreme lethargy occurs, contact your doctor.",
        "allergy_triggers": ["atenolol", "beta-blocker", "ٹینارمین"],
        "disease_contraindications": {
            "asthma": "دمہ کے مریضوں میں یہ دوا سانس کی نالیوں کو سکیڑ کر دم گھٹنے کا شدید سبب بن سکتی ہے۔",
            "bradycardia": "سست نبض کے مریضوں میں دل کی حرکت مزید دھیمی کر دیتی ہے۔"
        }
    },
    "flagyl": {
        "brand_name": "Flagyl",
        "generic_name": "Metronidazole",
        "drug_class": "Antimicrobial & Antiprotozoal (معدے اور پیٹ کے انفیکشن کی دوا)",
        "common_strengths": ["200mg", "400mg", "200mg/5ml (Syrup)"],
        "formulations": ["Tablet (گولی)", "Suspension (شربت)"],
        "purpose_ur": "یہ دوا پیٹ کے کیڑوں، پیچش (امیبک ڈیسنٹری)، دانتوں کے انفیکشن اور بیکٹیریل انفیکشن کے علاج کے لیے استعمال کی جاتی ہے۔",
        "purpose_en": "Flagyl is an antimicrobial effective against anaerobic bacteria and protozoal infections (amoebic dysentery, dental infections).",
        "how_to_take_guidance_ur": "کھانے کے دوران یا بعد میں ایک گلاس پانی کے ساتھ نگلیں۔ دوا کو چبائیں نہیں کیونکہ اس کا ذائقہ کڑوا ہوتا ہے۔ مقررہ دنوں کا کورس مکمل کریں۔",
        "how_to_take_guidance_en": "Take with or after food with plenty of water. Swallow whole; do not chew due to strong bitter taste. Complete full duration.",
        "precautions_ur": "دوا کے استعمال کے دوران پیشاب کا رنگ گہرا مائل بہ سرخ ہو سکتا ہے جو بے ضرر ہے۔",
        "precautions_en": "Urine may darken during therapy, which is harmless. Complete the full prescribed course.",
        "side_effects_ur": "منہ میں دھاتی یا کڑوا ذائقہ، متلی، بھوک میں کمی، سر درد یا پیٹ میں ہلکی گیس۔",
        "side_effects_en": "Metallic taste, nausea, dry mouth, headache, and epigastric discomfort.",
        "special_care_ur": "اعصابی امراض، مرگی یا جگر کے شدید مریضوں میں خصوصی احتیاط کی ضرورت ہوتی ہے۔",
        "special_care_en": "Use with caution in severe hepatic impairment and active central nervous system diseases.",
        "doctor_advisory_ur": "میری آپ کو ایک ضروری بات: منہ کا کڑوا ذائقہ اس دوا کا عام اثر ہے، اس سے گھبرائیں نہیں۔ دست یا پیٹ کی تکلیف میں کورس پورا کرنا ضروری ہے تاکہ انفیکشن جڑ سے ختم ہو۔",
        "doctor_advisory_en": "Doctor's note: The bitter metallic taste is harmless. Stay hydrated and complete the full regimen.",
        "allergy_triggers": ["metronidazole", "flagyl", "میٹرو نیڈازول", "فلیجل"],
        "disease_contraindications": {
            "liver": "جگر کے شدید عارضے میں خوراک کی کمی لازمی ہے۔"
        }
    },
    "risek": {
        "brand_name": "Risek",
        "generic_name": "Omeprazole",
        "drug_class": "Proton Pump Inhibitor (معدے کی تیزابیت کم کرنے والی دوا)",
        "common_strengths": ["20mg", "40mg", "Insta Sachet"],
        "formulations": ["Capsule (کیپسول)", "Sachet (ساشے)"],
        "purpose_ur": "یہ دوا معدے میں تیزاب کی مقدار کو کم کرتی ہے۔ معدے کے السر، سینے کی جلن اور تیزابیت (GERD) کے علاج کے لیے بہترین دوا ہے۔",
        "purpose_en": "Risek is a proton pump inhibitor that reduces stomach acid production, treating ulcers, GERD, and acid reflux.",
        "how_to_take_guidance_ur": "صبح ناشتے سے 30 سے 60 منٹ پہلے نہار منہ پانی کے ساتھ لیں۔ کیپسول کو کھولیں یا چبائیں نہیں، ثابت نگلیں۔",
        "how_to_take_guidance_en": "Take once daily in the morning 30-60 minutes before breakfast with a glass of water. Swallow capsule whole.",
        "precautions_ur": "طویل عرصے (مہینوں) تک مسلسل بلا ضرورت استعمال کرنے سے جسم میں کیلشیم اور وٹامن بی12 کی کمی ہو سکتی ہے۔",
        "precautions_en": "Prolonged unmonitored use may lead to vitamin B12 and magnesium deficiency or decreased bone density.",
        "side_effects_ur": "سر درد، ہلکا اسہال، پیٹ میں ہوا بھرنا یا قبض۔ عموماً یہ دوا بہت آرام دہ ثابت ہوتی ہے۔",
        "side_effects_en": "Mild headache, diarrhea, abdominal pain, or flatulence. Generally well tolerated.",
        "special_care_ur": "اگر خون کی الٹی ہو، پاخانہ سیاہ آئے، یا وزن میں اچانک کمی ہو تو فوراً ڈاکٹر کو دکھائیں۔",
        "special_care_en": "Alarm symptoms such as unexplained weight loss, dysphagia, or hematemesis require urgent clinical evaluation.",
        "doctor_advisory_ur": "میری آپ کو ایک ضروری بات: تیزابیت سے بچنے کے لیے رات کا کھانا سونے سے 2 سے 3 گھنٹے پہلے کھائیں، اور زیادہ تلی ہوئی یا تیز مرچوں والی چیزوں سے پرہیز کریں۔",
        "doctor_advisory_en": "Doctor's note: For optimal reflux relief, avoid lying down for 3 hours after eating and minimize deep-fried spicy foods.",
        "allergy_triggers": ["omeprazole", "risek", "اومپرازول"],
        "disease_contraindications": {
            "liver": "شدید جگر کی خرابی میں خوراک 20 ملی گرام روزانہ تک محدود رکھنی چاہیے۔"
        }
    },
    "brufen": {
        "brand_name": "Brufen",
        "generic_name": "Ibuprofen",
        "drug_class": "NSAID Pain Reliever (درد کش اور سوجن کم کرنے والی دوا)",
        "common_strengths": ["200mg", "400mg", "600mg", "100mg/5ml (Syrup)"],
        "formulations": ["Tablet (گولی)", "Syrup (شربت)"],
        "purpose_ur": "یہ دوا جوڑوں کے درد، سوجن، پٹھوں کی تکلیف، دانت کے درد اور ماہواری کے درد میں آرام پہنچاتی ہے۔",
        "purpose_en": "Brufen is an anti-inflammatory pain reliever used for joint stiffness, osteoarthritis, dental pain, and muscular inflammation.",
        "how_to_take_guidance_ur": "ہمیشہ کھانا کھانے کے بعد دودھ یا پانی کے ساتھ لیں۔ خالی پیٹ کھانے سے معدہ خراب ہو سکتا ہے۔",
        "how_to_take_guidance_en": "Always take after food or with milk to protect stomach lining. Never take on an empty stomach.",
        "precautions_ur": "زیادہ دن یا زیادہ مقدار میں لینے سے معدے میں زخم (السر) اور گردوں پر بوجھ بن سکتا ہے۔",
        "precautions_en": "Prolonged use can damage kidneys and cause gastric ulcers or gastrointestinal bleeding.",
        "side_effects_ur": "معدے میں تیزابیت، متلی، پیٹ کا پھولنا، اور پاؤں میں ہلکا ورم۔",
        "side_effects_en": "Dyspepsia, heartburn, fluid retention, nausea, and gastrointestinal irritation.",
        "special_care_ur": "گردوں کے مریض، ہائی بلڈ پریشر، دل کے عارضے میں مبتلا افراد اور بزرگ مریض خاص احتیاط کریں۔",
        "special_care_en": "Contraindicated in severe heart failure, active ulcer, severe renal impairment, and NSAID hypersensitivity.",
        "doctor_advisory_ur": "میری آپ کو ایک ضروری بات: بزرگ افراد میں درد کش ادویات کا بلا ضرورت استعمال گردوں کو نقصان پہنچا سکتا ہے۔ درد کم ہوتے ہی دوا روک دیں یا ڈاکٹر سے متبادل پر بات کریں۔",
        "doctor_advisory_en": "Doctor's note: Avoid chronic use of NSAIDs in elderly patients due to renal and cardiovascular risks.",
        "allergy_triggers": ["ibuprofen", "brufen", "nsaids", "بروفن"],
        "disease_contraindications": {
            "ulcer": "معدے کے السر میں خون بہنے کا سنگین خطرہ ہے۔",
            "kidney": "گردوں کے فیل ہونے یا کمزور ہونے کا خطرہ بڑھ جاتا ہے۔",
            "hypertension": "بلڈ پریشر کی دواؤں کے اثر کو زائل کر سکتی ہے۔"
        }
    },
    "softin": {
        "brand_name": "Softin",
        "generic_name": "Loratadine",
        "drug_class": "Antihistamine (الرجی اور چھینکوں کی دوا)",
        "common_strengths": ["10mg", "5mg/5ml (Syrup)"],
        "formulations": ["Tablet (گولی)", "Syrup (شربت)"],
        "purpose_ur": "یہ دوا الرجی کی علامات جیسے چھینکیں، ناک بہنا، آنکھوں سے پانی آنا اور جلد پر خارش یا دھپڑوں کے علاج کے لیے استعمال ہوتی ہے۔",
        "purpose_en": "Softin is a non-drowsy antihistamine that treats seasonal allergic rhinitis, runny nose, sneezing, and skin hives.",
        "how_to_take_guidance_ur": "دن میں ایک بار، کھانے کے بعد یا پہلے پانی کے ساتھ لیں۔",
        "how_to_take_guidance_en": "Take once daily with or without food.",
        "precautions_ur": "عام طور پر نیند نہیں لاتی، لیکن اگر غنودگی محسوس ہو تو ڈرائیونگ سے گریز کریں۔",
        "precautions_en": "Generally non-sedating, but exercise caution if driving until you know how it affects you.",
        "side_effects_ur": "منہ کا خشک ہونا، ہلکا سر درد یا ہلکی تھکن۔ یہ عموماً بہت ہلکے ہوتے ہیں۔",
        "side_effects_en": "Dry mouth, mild headache, or mild drowsiness in rare sensitive individuals.",
        "special_care_ur": "جگر کی شدید خرابی میں ڈاکٹر سے خوراک کی تصدیق کرائیں۔",
        "special_care_en": "Dose adjustment required in severe liver failure.",
        "doctor_advisory_ur": "میری آپ کو ایک ضروری بات: الرجی سے بچنے کے لیے گرد و غبار، دھواں اور قالینوں کی مٹی سے بچاؤ بھی ضروری ہے۔ دوا آرام تو دے گی مگر پرہیز ہی بہترین علاج ہے۔",
        "doctor_advisory_en": "Doctor's note: Avoid allergen triggers like dust and smoke to prevent symptom flare-ups.",
        "allergy_triggers": ["loratadine", "softin", "لوراٹاڈین"],
        "disease_contraindications": {}
    }
}

# Known clinical Drug-Drug Interactions
DRUG_INTERACTIONS = [
    {
        "drug_a": "augmentin",
        "drug_b": "disprin",
        "severity": "moderate",
        "message_ur": "اینٹی بائیوٹک اور اسپرین کا بیک وقت استعمال معدے کی جلن اور خون بہنے کے خطرے کو تھوڑا بڑھا سکتا ہے۔ کھانے کے بعد مناسب وقفے سے لیں۔",
        "message_en": "Augmentin and Aspirin co-administration may increase gastric irritation. Take with meals and adequate spacing."
    },
    {
        "drug_a": "arinac",
        "drug_b": "tenormin",
        "severity": "critical",
        "message_ur": "خطرناک تعامل: ایرینیک (جس میں سیوڈو ایفیڈرین اور بروفن شامل ہے) ٹینارمین کے بلڈ پریشر کم کرنے والے اثر کو زائل کر دیتی ہے اور بلڈ پریشر کو تیزی سے اوپر لے جاتی ہے۔ یہ دونوں ایک ساتھ ہرگز نہ لیں۔",
        "message_en": "CRITICAL INTERACTION: Arinac (Pseudoephedrine + Ibuprofen) opposes Tenormin's antihypertensive effect and spikes blood pressure dangerously. Do not combine."
    },
    {
        "drug_a": "brufen",
        "drug_b": "disprin",
        "severity": "critical",
        "message_ur": "خطرناک تعامل: بروفن اور ڈسپرین دونوں درد کش (NSAID) گروہ سے ہیں۔ دونوں کو ایک ساتھ لینے سے معدے میں زخم (السر) اور خون بہنے کا خطرہ بہت زیادہ بڑھ جاتا ہے۔",
        "message_en": "CRITICAL INTERACTION: Taking Brufen and Disprin together multiplies gastrointestinal ulceration and internal bleeding risks."
    },
    {
        "drug_a": "brufen",
        "drug_b": "tenormin",
        "severity": "moderate",
        "message_ur": "بروفن باقاعدگی سے لینے پر ٹینارمین کے بی پی کنٹرول کرنے کے اثر کو کم کر سکتی ہے اور جسم میں نمکیات جمع کر سکتی ہے۔",
        "message_en": "Ibuprofen may blunt the blood-pressure-lowering efficacy of beta-blockers like Tenormin."
    },
    {
        "drug_a": "glucophage",
        "drug_b": "disprin",
        "severity": "mild",
        "message_ur": "ڈسپرین زیادہ مقدار میں شوگر کی دوا کے اثر کو بڑھا سکتی ہے جس سے شوگر زیادہ گرنے (ہائپوگلائسیمیا) کا ہلکا اندیشہ ہوتا ہے۔ شوگر چیک کرتے رہیں۔",
        "message_en": "High doses of salicylates may potentiate hypoglycemia when combined with Metformin. Monitor blood sugar."
    }
]


def normalize_drug_name(name: str) -> str:
    """Normalizes brand or generic name for lookup."""
    clean = name.lower().strip()
    # Strip strength / numbers like 500mg, 625, etc.
    words = [w for w in clean.replace("+", " ").replace("/", " ").replace("-", " ").split() if not any(c.isdigit() for c in w)]
    for key in PAKISTAN_DRUG_DATABASE.keys():
        if key in clean:
            return key
    # Check generics
    for key, data in PAKISTAN_DRUG_DATABASE.items():
        if any(w in data["generic_name"].lower() for w in words):
            return key
    return clean.split()[0] if clean else ""


def find_drug_info(query: str) -> Optional[Dict[str, Any]]:
    """Looks up structured clinical data for a given medicine query."""
    key = normalize_drug_name(query)
    if key in PAKISTAN_DRUG_DATABASE:
        return PAKISTAN_DRUG_DATABASE[key]
    # Secondary check by substring
    q = query.lower()
    for k, v in PAKISTAN_DRUG_DATABASE.items():
        if k in q or v["brand_name"].lower() in q or v["generic_name"].lower() in q:
            return v
    return None


def check_drug_safety(candidate_medicine: str, candidate_generic: str, profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Performs comprehensive safety check:
    1. Allergy cross-matching
    2. Disease-drug contraindications
    3. Drug-drug interactions against patient's current medication list
    """
    safety_report = {
        "has_critical_alerts": False,
        "allergy_warnings": [],
        "condition_warnings": [],
        "drug_interactions": [],
        "overall_summary_ur": "",
        "overall_summary_en": ""
    }

    norm_cand = normalize_drug_name(candidate_medicine) or normalize_drug_name(candidate_generic)
    cand_info = PAKISTAN_DRUG_DATABASE.get(norm_cand)

    cand_text_to_match = f"{candidate_medicine} {candidate_generic}".lower()
    if cand_info:
        cand_text_to_match += f" {cand_info['generic_name']} {cand_info['drug_class']}".lower()

    # 1. Allergy Checking
    allergies = profile.get("allergies", [])
    for a in allergies:
        allergen = f"{a.get('allergen_en', '')} {a.get('allergen_ur', '')}".lower()
        matched = False
        
        # Check against drug's known allergy triggers
        if cand_info:
            for trigger in cand_info.get("allergy_triggers", []):
                if trigger in allergen or allergen in trigger:
                    matched = True
                    break
        
        # Direct string matching
        if "penicillin" in allergen and ("amoxicillin" in cand_text_to_match or "augmentin" in cand_text_to_match or "ampicillin" in cand_text_to_match):
            matched = True
        if ("aspirin" in allergen or "nsaid" in allergen) and ("disprin" in cand_text_to_match or "brufen" in cand_text_to_match or "arinac" in cand_text_to_match or "ibuprofen" in cand_text_to_match):
            matched = True

        if matched:
            safety_report["has_critical_alerts"] = True
            msg_ur = f"⚠️ شدید الرجی الرٹ: مریض کو '{a.get('allergen_ur', a.get('allergen_en'))}' سے الرجی ہے۔ یہ دوا اس کے ساتھ جان لیوا ثابت ہو سکتی ہے۔ یہ دوا ہرگز استعمال نہ کریں!"
            msg_en = f"CRITICAL ALLERGY ALERT: Patient has a recorded allergy to '{a.get('allergen_en', '')}'. This medication is contraindicated!"
            safety_report["allergy_warnings"].append({
                "severity": "critical",
                "allergen": a.get("allergen_en", ""),
                "message_ur": msg_ur,
                "message_en": msg_en
            })

    # 2. Disease / Medical Condition Checking
    conditions = profile.get("conditions", [])
    for c in conditions:
        cond_name = f"{c.get('name_en', '')} {c.get('name_ur', '')}".lower()
        
        # Specific high-risk clinical pairs
        # Arinac / Pseudoephedrine in Hypertension
        if ("hypertension" in cond_name or "blood pressure" in cond_name or "بلند فشار" in cond_name or "ہائی بلڈ" in cond_name):
            if "arinac" in cand_text_to_match or "pseudoephedrine" in cand_text_to_match:
                safety_report["has_critical_alerts"] = True
                safety_report["condition_warnings"].append({
                    "severity": "critical",
                    "condition": "Hypertension (ہائی بلڈ پریشر)",
                    "message_ur": "⚠️ احتیاط: مریض کو ہائی بلڈ پریشر کا عارضہ ہے۔ اس دوا میں موجود اجزاء بلڈ پریشر اور نبض کو خطرناک حد تک بڑھا سکتے ہیں۔",
                    "message_en": "CONTRAINDICATION: Patient has hypertension. Decongestants in this medication cause severe blood pressure spikes."
                })

        # Disprin / Brufen in Ulcers / GERD
        if ("ulcer" in cond_name or "تیزابیت" in cond_name or "السر" in cond_name or "gerd" in cond_name or "acid" in cond_name):
            if "disprin" in cand_text_to_match or "aspirin" in cand_text_to_match or "brufen" in cand_text_to_match or "ibuprofen" in cand_text_to_match:
                safety_report["condition_warnings"].append({
                    "severity": "warning",
                    "condition": "Stomach Acid / Ulcer (معدے کی تکلیف)",
                    "message_ur": "⚠️ احتیاط: مریض کو معدے کی جلن/السر کا عارضہ ہے۔ یہ درد کش دوا معدے پر سوزش یا خون بہنے کا خطرہ پیدا کر سکتی ہے۔",
                    "message_en": "WARNING: Patient has stomach ulcer/GERD. This NSAID can cause gastric bleeding or mucosal damage."
                })

        # Tenormin in Asthma
        if ("asthma" in cond_name or "دمہ" in cond_name or "سانس" in cond_name):
            if "tenormin" in cand_text_to_match or "atenolol" in cand_text_to_match or "propranolol" in cand_text_to_match:
                safety_report["has_critical_alerts"] = True
                safety_report["condition_warnings"].append({
                    "severity": "critical",
                    "condition": "Asthma (دمہ)",
                    "message_ur": "⚠️ خطرناک ممانعت: دمہ کے مریضوں میں یہ دوا سانس کی نالیوں کو سکیڑ کر دم گھٹنے کا شدید سبب بن سکتی ہے۔",
                    "message_en": "CRITICAL CONTRAINDICATION: Beta-blockers can trigger life-threatening bronchospasm in asthma patients."
                })

        # Glucophage in severe kidney
        if ("kidney" in cond_name or "گردے" in cond_name):
            if "glucophage" in cand_text_to_match or "metformin" in cand_text_to_match:
                safety_report["condition_warnings"].append({
                    "severity": "warning",
                    "condition": "Kidney Disease (گردوں کا مرض)",
                    "message_ur": "⚠️ احتیاط: گردوں کے امراض میں میٹفارمین کی مقدار ڈاکٹر کے مشورے سے جانچنا ضروری ہے۔",
                    "message_en": "WARNING: Renal function must be verified before and during Metformin therapy."
                })

    # 3. Drug-Drug Interactions against Active Medications
    active_meds = [m for m in profile.get("medicines", []) if m.get("status") == "active"]
    for existing_med in active_meds:
        ex_name = normalize_drug_name(existing_med.get("brand_name", "")) or normalize_drug_name(existing_med.get("generic_name", ""))
        
        for inter in DRUG_INTERACTIONS:
            da, db = inter["drug_a"], inter["drug_b"]
            if (da == norm_cand and db == ex_name) or (db == norm_cand and da == ex_name):
                if inter["severity"] == "critical":
                    safety_report["has_critical_alerts"] = True
                safety_report["drug_interactions"].append({
                    "severity": inter["severity"],
                    "conflicting_med": existing_med.get("brand_name"),
                    "message_ur": inter["message_ur"],
                    "message_en": inter["message_en"]
                })

    return safety_report
