/**
 * Dawa Dost Internationalization (i18n) Engine
 * Provides complete Urdu (اردو) and English dictionaries,
 * RTL/LTR layout management, and voice narration phrases.
 */

const translations = {
  ur: {
    // Brand & Header
    app_title: "دوا دوست",
    app_subtitle: "آپ کی صحت اور دواؤں کا ہمدرد ساتھی",
    disclaimer: "یہ معلومات AI کی مدد سے دی گئی ہیں، ڈاکٹر کے مشورے کا متبادل نہیں۔",
    greeting_salutation: "السلام علیکم!",
    greeting_question: "آج ہم آپ کی دوا یا نسخے کے بارے میں کیا مدد کر سکتے ہیں؟",
    audio_greeting: "السلام علیکم! دوا دوست میں خوش آمدید۔ نسخے کی تصویر لیں یا اپنی دوا کی تفصیل جانیں۔",
    
    // Top Nav
    lang_btn: "English",
    profile_btn_prefix: "مریض:",
    
    // Home Primary Actions (3 Main Cards)
    action_scan_rx_title: "نسخے کی تصویر لیں",
    action_scan_rx_desc: "ڈاکٹر کے ہاتھ سے لکھے ہوئے نسخے کی تصویر کھینچیں اور دوائیں سمجھیں",
    audio_scan_rx: "نسخے کی تصویر لینے اور ڈاکٹر کی ہدایات سمجھنے کے لیے یہاں دبائیں۔",

    action_scan_med_title: "دوا کی تصویر لیں",
    action_scan_med_desc: "دوا کی ڈبی، پتے یا شیشی کی تصویر کھینچیں اور استعمال کا طریقہ جانیں",
    audio_scan_med: "دوا کی ڈبی یا پتے کی تصویر لینے کے لیے یہاں دبائیں۔",

    action_my_meds_title: "میری دوائیں",
    action_my_meds_desc: "پہلے سے محفوظ شدہ دوائیں دیکھیں اور دوبارہ وضاحت سنیں",
    audio_my_meds: "اپنی تمام محفوظ شدہ دوائیں اور ان کے استعمال کا طریقہ دیکھنے کے لیے یہاں دبائیں۔",

    // Image Acquisition & Scanning Screen
    scan_page_rx_title: "نسخے کی تصویر بنائیں",
    scan_page_med_title: "دوا کی تصویر بنائیں",
    photo_guidance: "تصویر صاف اور روشن ہونی چاہیے تاکہ دوا کا نام آسانی سے پڑھا جا سکے",
    camera_btn_label: "کیمرہ کھولیں اور تصویر لیں",
    upload_btn_label: "گیلری سے تصویر منتخب کریں",
    retake_btn: "دوبارہ تصویر لیں",
    proceed_btn: "آگے بڑھیں اور دوا کی شناخت کریں",
    sample_presets_label: "یا فوری ٹیسٹ کے لیے نیچے دیے گئے نمونوں میں سے چنیں:",
    sample_rx_chip: "ڈاکٹر کا نسخہ (آگمنٹین + پیناڈول)",
    sample_panadol_chip: "پیناڈول 500 ملی گرام (پتہ)",
    sample_arinac_chip: "ایرینیک فورٹ (نزلہ و زکام)",

    // Verification Step ("ہمیں یہ دوا نظر آئی ہے")
    verify_heading: "ہمیں یہ دوا نظر آئی ہے:",
    verify_sub: "براہِ کرم تصدیق کریں کہ کیا یہ نام اور تفصیل درست ہے؟",
    field_brand: "دوا کا نام (Brand Name):",
    field_generic: "اصل جزو (Generic Name):",
    field_strength: "طاقت / مقدار (Strength):",
    field_formulation: "دوا کی قسم (Formulation):",
    field_instructions: "نسخے کی ہدایات (Prescribed Instructions):",
    btn_confirm_yes: "جی ہاں، بالکل درست ہے",
    btn_confirm_no: "نہیں، دوبارہ تصویر لیں",
    unclear_handwriting_alert: "نوٹ: نسخے کی لکھائی میں کچھ حصہ پڑھنے میں دشواری تھی۔ آپ خود درست کر سکتے ہیں۔",

    // Doctor Persona Explanation Screen
    doctor_title: "ڈاکٹر صاحب کا مشورہ",
    doctor_sub: "بزرگ مریض کے لیے آسان اور محفوظ رہنمائی",
    listen_all_btn: "پورا مشورہ سنیں",
    pause_btn: "روکیں",
    resume_btn: "جاری رکھیں",
    replay_btn: "دوبارہ سنیں",
    stop_btn: "بند کریں",

    sec_purpose_title: "1. دوا کس کام آتی ہے؟",
    sec_how_to_take_title: "2. یہ دوا کیسے لینی ہے؟",
    sec_precautions_title: "3. اس دوا سے کیا احتیاط کرنی ہے؟",
    sec_side_effects_title: "4. اس دوا کے عام نقصانات کیا ہو سکتے ہیں؟",
    sec_special_care_title: "5. کن لوگوں کو خاص احتیاط کرنی چاہیے؟",
    sec_doctor_advisory_title: "6. ڈاکٹر کی طرف سے ایک ضروری بات",

    // Medical Knowledge & Conversational Assistant
    candidate_alternatives_title: "شناخت شدہ متبادل اور ملتی جلتی دوائیں:",
    ambiguity_alert: "نوٹ: نسخے یا تصویر سے ملتی جلتی ایک سے زائد دوائیں ملیں۔ اگر ضرورت ہو تو نیچے دی گئی درست دوا پر کلک کریں:",
    medical_sources_label: "مصدقہ طبی ماخذ (Authoritative Sources):",
    chat_section_title: "ڈاکٹر صاحب سے مزید سوال پوچھیں",
    chat_section_sub: "اس دوا کے متعلق کوئی بھی بات دریافت کریں (کھانے کا وقت، احتیاط وغیرہ)",
    quick_q1: "کیا میں یہ دوا کھانے کے بعد لے سکتا ہوں؟",
    quick_q2: "اگر میں خوراک لینا بھول جاؤں تو کیا کروں؟",
    quick_q3: "کیا اس دوا سے نیند یا غنودگی آ سکتی ہے؟",
    quick_q4: "اس دوا کے عام اثرات کیا ہیں؟",
    chat_input_placeholder: "اپنا سوال یہاں لکھیں یا مائیک دبائیں...",
    btn_ask_doctor: "پوچھیں",
    chat_loading: "ڈاکٹر صاحب جواب تیار کر رہے ہیں...",

    btn_save_to_history: "میری دواؤں میں محفوظ کریں",
    btn_scan_another: "ایک اور دوا دیکھیں",
    saved_success_toast: "دوا کامیابی کے ساتھ آپ کی تاریخ میں محفوظ ہو گئی!",

    // My Medicines ("میری دوائیں")
    filter_all: "سب دوائیں",
    filter_active: "ابھی لے رہے ہیں",
    filter_discontinued: "روک دی گئی",
    btn_listen_card: "سنیں",
    btn_details_card: "تفصیل دیکھیں",
    btn_discontinue_card: "دوا بند کریں",
    discontinue_confirm_msg: "کیا آپ واقعی اس دوا کو 'روک دی گئی' نشان زد کرنا چاہتے ہیں؟",
    empty_meds_msg: "ابھی تک کوئی دوا محفوظ نہیں کی گئی۔ نئی دوا اسکین کرنے کے لیے ہوم اسکرین پر جائیں۔",

    // Personal Health Profile
    profile_modal_title: "مریض کا ہیلتھ پروفائل",
    switch_family_member: "خاندان کا فرد تبدیل کریں:",
    add_family_member_btn: "+ نیا فرد شامل کریں",
    section_conditions: "طبی کیفیات اور بیماریاں:",
    add_condition_btn: "+ نئی بیماری شامل کریں",
    section_allergies: "معلوم الرجی (Allergies):",
    add_allergy_btn: "+ نئی الرجی شامل کریں",
    section_current_meds: "موجودہ زیرِ استعمال دوائیں:",
    profile_age: "عمر:",
    profile_years: "سال",
    save_btn: "محفوظ کریں",
    close_btn: "بند کریں",
    back_to_home: "واپس ہوم اسکرین"
  },

  en: {
    // Brand & Header
    app_title: "Dawa Dost",
    app_subtitle: "Your Caring Medicine & Prescription Companion",
    disclaimer: "This information is AI-generated and is not a substitute for professional medical advice.",
    greeting_salutation: "Assalam-o-Alaikum!",
    greeting_question: "How can we assist you with your medicines today?",
    audio_greeting: "Welcome to Dawa Dost. Photograph your prescription or scan a medicine to understand its use.",

    // Top Nav
    lang_btn: "اردو",
    profile_btn_prefix: "Patient:",

    // Home Primary Actions
    action_scan_rx_title: "Scan a Prescription",
    action_scan_rx_desc: "Photograph your doctor's handwritten prescription and understand instructions",
    audio_scan_rx: "Press here to photograph a prescription and understand your doctor's instructions.",

    action_scan_med_title: "Scan a Medicine",
    action_scan_med_desc: "Photograph a medicine box, blister strip or bottle to understand how to take it",
    audio_scan_med: "Press here to photograph a medicine box or blister strip.",

    action_my_meds_title: "My Medicines",
    action_my_meds_desc: "View previously scanned medications and listen to their explanations again",
    audio_my_meds: "Press here to view your saved medicines and listen to their directions.",

    // Image Acquisition & Scanning Screen
    scan_page_rx_title: "Photograph Prescription",
    scan_page_med_title: "Photograph Medicine",
    photo_guidance: "The photograph should be clear and well-lit so the medicine name is easily readable",
    camera_btn_label: "Open Camera & Take Photo",
    upload_btn_label: "Select Photo from Gallery / Device",
    retake_btn: "Retake Photo",
    proceed_btn: "Proceed & Identify Medicine",
    sample_presets_label: "Or tap a sample below for instant demonstration:",
    sample_rx_chip: "Doctor Prescription (Augmentin + Panadol)",
    sample_panadol_chip: "Panadol 500mg (Blister Strip)",
    sample_arinac_chip: "Arinac Forte (Cold & Flu)",

    // Verification Step
    verify_heading: "We identified this medicine:",
    verify_sub: "Please confirm if the extracted name and dosage details are correct:",
    field_brand: "Medicine Brand Name:",
    field_generic: "Active Ingredient (Generic):",
    field_strength: "Dosage Strength:",
    field_formulation: "Formulation Type:",
    field_instructions: "Prescription Instructions:",
    btn_confirm_yes: "Yes, this is correct",
    btn_confirm_no: "No, take photo again",
    unclear_handwriting_alert: "Note: Some handwritten text was difficult to read. You can manually adjust the fields above.",

    // Doctor Persona Explanation Screen
    doctor_title: "Doctor's Advice & Guidance",
    doctor_sub: "Compassionate, easy-to-understand explanation for elderly patients",
    listen_all_btn: "Listen to Full Advice",
    pause_btn: "Pause",
    resume_btn: "Resume",
    replay_btn: "Replay",
    stop_btn: "Stop",

    sec_purpose_title: "1. What is this medicine used for?",
    sec_how_to_take_title: "2. How should this medicine be taken?",
    sec_precautions_title: "3. What precautions should be taken?",
    sec_side_effects_title: "4. What are the common side effects?",
    sec_special_care_title: "5. Who should take special care?",
    sec_doctor_advisory_title: "6. An important note from the doctor",

    // Medical Knowledge & Conversational Assistant
    candidate_alternatives_title: "Verified Alternative Candidates:",
    ambiguity_alert: "Notice: Multiple matching medications found. Tap the correct candidate below if needed:",
    medical_sources_label: "Authoritative Medical Sources:",
    chat_section_title: "Ask Doctor Sahib a Follow-Up Question",
    chat_section_sub: "Ask anything about timing, precautions, or food interactions for this medicine",
    quick_q1: "Can I take this medicine after meals?",
    quick_q2: "What should I do if I miss a dose?",
    quick_q3: "Can this medicine cause drowsiness or sleepiness?",
    quick_q4: "What are the common side effects of this medicine?",
    chat_input_placeholder: "Type your question here...",
    btn_ask_doctor: "Ask Doctor",
    chat_loading: "Doctor Sahib is preparing your answer...",

    btn_save_to_history: "Save to My Medicines",
    btn_scan_another: "Scan Another Medicine",
    saved_success_toast: "Medicine successfully saved to your health history!",

    // My Medicines
    filter_all: "All Medicines",
    filter_active: "Currently Taking",
    filter_discontinued: "Discontinued",
    btn_listen_card: "Listen",
    btn_details_card: "View Details",
    btn_discontinue_card: "Discontinue",
    discontinue_confirm_msg: "Are you sure you want to mark this medicine as discontinued?",
    empty_meds_msg: "No medicines saved yet. Return to the home screen to scan a new medicine.",

    // Personal Health Profile
    profile_modal_title: "Patient Health Profile",
    switch_family_member: "Switch Family Member:",
    add_family_member_btn: "+ Add Family Member",
    section_conditions: "Medical Conditions & History:",
    add_condition_btn: "+ Add Condition",
    section_allergies: "Known Allergies:",
    add_allergy_btn: "+ Add Allergy",
    section_current_meds: "Active Medications:",
    profile_age: "Age:",
    profile_years: "years",
    save_btn: "Save Changes",
    close_btn: "Close",
    back_to_home: "Back to Home"
  }
};

let currentLanguage = localStorage.getItem("dawa_dost_lang") || "ur";

function getLang() {
  return currentLanguage;
}

function setLang(lang) {
  if (lang !== "ur" && lang !== "en") return;
  currentLanguage = lang;
  localStorage.setItem("dawa_dost_lang", lang);
  
  // Set document direction and language attribute
  document.documentElement.lang = lang;
  document.body.dir = lang === "ur" ? "rtl" : "ltr";
}

function t(key) {
  const dict = translations[currentLanguage] || translations["ur"];
  return dict[key] || translations["ur"][key] || key;
}
