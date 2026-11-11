/**
 * Dawa Dost Main Application Controller
 * Handles routing, camera streaming, scan extraction, verification,
 * explanation rendering, audio controls, and health profile management.
 */

const state = {
  currentView: "home",
  scanMode: "prescription", // "prescription" or "medicine"
  activeProfileId: 1,
  activeProfile: null,
  allProfiles: [],
  capturedImage: null, // base64 or sample filename
  sampleFilename: null,
  extractedMedicine: null,
  activeExplanation: null,
  cameraStream: null,
  historyFilter: "all",
  chatSessionId: "sess_" + Math.random().toString(36).substring(2, 10),
  chatMessages: []
};

// --- Initialization ---

document.addEventListener("DOMContentLoaded", async () => {
  // Initialize language from storage or default Urdu
  const savedLang = localStorage.getItem("dawa_dost_lang") || "ur";
  setLang(savedLang);

  // Bind audio status events
  audioAssistant.onStatusChange = updateAudioPlayerState;

  // Load profiles and render
  await loadProfiles();
  renderApp();
});

async function loadProfiles() {
  try {
    state.allProfiles = await api.getProfiles();
    const savedId = parseInt(localStorage.getItem("dawa_dost_profile_id")) || (state.allProfiles[0]?.id || 1);
    state.activeProfileId = savedId;
    state.activeProfile = await api.getProfile(state.activeProfileId);
  } catch (e) {
    console.error("Failed to load profiles:", e);
  }
}

async function switchProfile(profileId) {
  state.activeProfileId = profileId;
  localStorage.setItem("dawa_dost_profile_id", profileId);
  state.activeProfile = await api.getProfile(profileId);
  closeModal();
  renderApp();
}

function toggleLanguage() {
  const newLang = getLang() === "ur" ? "en" : "ur";
  setLang(newLang);
  audioAssistant.stop();
  renderApp();
}

// --- View Navigation ---

function navigateTo(view, params = {}) {
  audioAssistant.stop();
  stopCamera();
  state.currentView = view;
  if (params.scanMode) state.scanMode = params.scanMode;
  if (params.extracted) state.extractedMedicine = params.extracted;
  if (params.explanation) state.activeExplanation = params.explanation;
  renderApp();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// --- Main Render Dispatcher ---

function renderApp() {
  const container = document.getElementById("main-content");
  if (!container) return;

  // Update top bar text & indicators
  updateTopBar();

  switch (state.currentView) {
    case "home":
      container.innerHTML = renderHomeView();
      break;
    case "scan":
      container.innerHTML = renderScanView();
      bindScanEvents();
      break;
    case "verify":
      container.innerHTML = renderVerifyView();
      break;
    case "explain":
      container.innerHTML = renderExplainView();
      break;
    case "history":
      container.innerHTML = renderHistoryView();
      loadHistoryMeds();
      break;
    default:
      container.innerHTML = renderHomeView();
  }
}

function updateTopBar() {
  const langBtn = document.getElementById("lang-btn-text");
  if (langBtn) langBtn.textContent = t("lang_btn");

  const disclaimer = document.getElementById("top-disclaimer-text");
  if (disclaimer) disclaimer.textContent = t("disclaimer");

  const profilePill = document.getElementById("profile-pill-name");
  if (profilePill && state.activeProfile) {
    profilePill.textContent = state.activeProfile.name;
  }
}

// ==========================================================================
// VIEW 1: HOME VIEW
// ==========================================================================

function renderHomeView() {
  const profName = state.activeProfile ? state.activeProfile.name : "محترم";
  return `
    <!-- Welcoming Greeting Card -->
    <div class="greeting-card">
      <div class="greeting-text-area">
        <h2 class="greeting-salutation">
          ${t("greeting_salutation")} ${profName}
        </h2>
        <p class="greeting-subtext">
          ${t("greeting_question")}
        </p>
      </div>
      <button class="greeting-audio-btn" onclick="audioAssistant.narrateUI('audio_greeting')" title="سلام سنیں" aria-label="Listen greeting">
        🔊
      </button>
    </div>

    <!-- The 3 Giant Action Cards -->
    <div class="primary-actions-grid">
      
      <!-- Card 1: Scan Prescription -->
      <div class="main-action-card card-rx" onclick="navigateTo('scan', { scanMode: 'prescription' })" role="button" tabindex="0">
        <div class="action-card-icon-wrap">
          📝
        </div>
        <div class="action-card-content">
          <h3 class="action-card-title">${t("action_scan_rx_title")}</h3>
          <p class="action-card-desc">${t("action_scan_rx_desc")}</p>
        </div>
        <div class="action-card-side">
          <button class="card-listen-btn" onclick="event.stopPropagation(); audioAssistant.narrateUI('audio_scan_rx')" title="سنیں" aria-label="Listen button explanation">
            🔊
          </button>
          <span class="card-arrow">➔</span>
        </div>
      </div>

      <!-- Card 2: Scan Medicine -->
      <div class="main-action-card card-medicine" onclick="navigateTo('scan', { scanMode: 'medicine' })" role="button" tabindex="0">
        <div class="action-card-icon-wrap">
          💊
        </div>
        <div class="action-card-content">
          <h3 class="action-card-title">${t("action_scan_med_title")}</h3>
          <p class="action-card-desc">${t("action_scan_med_desc")}</p>
        </div>
        <div class="action-card-side">
          <button class="card-listen-btn" onclick="event.stopPropagation(); audioAssistant.narrateUI('audio_scan_med')" title="سنیں" aria-label="Listen button explanation">
            🔊
          </button>
          <span class="card-arrow">➔</span>
        </div>
      </div>

      <!-- Card 3: My Medicines -->
      <div class="main-action-card card-history" onclick="navigateTo('history')" role="button" tabindex="0">
        <div class="action-card-icon-wrap">
          🗄️
        </div>
        <div class="action-card-content">
          <h3 class="action-card-title">${t("action_my_meds_title")}</h3>
          <p class="action-card-desc">${t("action_my_meds_desc")}</p>
        </div>
        <div class="action-card-side">
          <button class="card-listen-btn" onclick="event.stopPropagation(); audioAssistant.narrateUI('audio_my_meds')" title="سنیں" aria-label="Listen button explanation">
            🔊
          </button>
          <span class="card-arrow">➔</span>
        </div>
      </div>

    </div>
  `;
}

// ==========================================================================
// VIEW 2: SCAN & IMAGE ACQUISITION VIEW
// ==========================================================================

function renderScanView() {
  const isRx = state.scanMode === "prescription";
  const title = isRx ? t("scan_page_rx_title") : t("scan_page_med_title");

  return `
    <div class="scanner-container">
      
      <div class="section-back-bar">
        <button class="back-btn" onclick="navigateTo('home')">
          <span>⬅</span> ${t("back_to_home")}
        </button>
        <h2 class="page-title">${title}</h2>
      </div>

      <!-- Clear Photo Guidance Box -->
      <div class="photo-guidance-callout">
        <span class="guidance-icon">💡</span>
        <span>${t("photo_guidance")}</span>
      </div>

      <!-- Live Camera Stream Box (Hidden initially until requested) -->
      <div id="camera-container" style="display: none; margin-bottom: 20px;">
        <div class="camera-video-wrap">
          <video id="camera-video" class="camera-video" autoplay playsinline></video>
          <div class="camera-controls-bar">
            <button class="snap-photo-btn" onclick="capturePhotoFromCamera()" title="تصویر لیں">
              📸
            </button>
            <button class="back-btn" onclick="stopCameraAndShowUpload()">
              ${t("close_btn")}
            </button>
          </div>
        </div>
        <canvas id="camera-canvas" style="display: none;"></canvas>
      </div>

      <!-- Capture / Upload Options Area -->
      <div id="upload-methods-area">
        <div class="capture-box" onclick="startCameraCapture()">
          <div class="capture-icon-giant">📷</div>
          <div class="capture-title">${t("camera_btn_label")}</div>
          <div class="capture-sub">آپ کے فون یا لیپ ٹاپ کا کیمرہ کھل جائے گا</div>
        </div>

        <div style="text-align: center; margin: 16px 0; font-size: 16px; color: var(--color-text-muted);">
          — یا —
        </div>

        <label class="capture-box" style="min-height: 120px; cursor: pointer;">
          <input type="file" id="file-input" accept="image/*" style="display: none;" onchange="handleFileSelected(event)">
          <div style="display: flex; align-items: center; gap: 14px;">
            <span style="font-size: 32px;">📁</span>
            <div style="text-align: right;">
              <div class="capture-title" style="font-size: 19px;">${t("upload_btn_label")}</div>
              <div class="capture-sub">پہلے سے کھینچی ہوئی تصویر منتخب کریں</div>
            </div>
          </div>
        </label>
      </div>

      <!-- Image Preview Area (Appears once photo is taken/chosen) -->
      <div id="preview-area" style="display: none;">
        <div class="preview-card">
          <img id="preview-img" class="preview-img" alt="Captured Scan">
          <div class="preview-actions-bar">
            <button class="btn-huge btn-huge-secondary" onclick="resetScan()">
              🔄 ${t("retake_btn")}
            </button>
            <button class="btn-huge btn-huge-primary" id="btn-process-scan" onclick="processExtraction()">
              🔍 ${t("proceed_btn")}
            </button>
          </div>
        </div>
      </div>

      <!-- Loading State (Pulse Spinner) -->
      <div id="scan-loading-area" class="loading-pulse-box" style="display: none;">
        <div class="pulse-spinner"></div>
        <div style="font-size: 22px; font-weight: 700; color: var(--color-primary);">
          دوا کی شناخت کی جا رہی ہے...
        </div>
        <div style="font-size: 16px; color: var(--color-text-muted);">
          براہِ کرم ایک لمحہ انتظار فرمائیں۔ نسخے کی تفصیل پڑھی جا رہی ہے۔
        </div>
      </div>

      <!-- 1-Click Pakistani Samples Chips for Instant Demonstration -->
      <div class="sample-presets-area">
        <div class="sample-presets-title">
          <span>🧪</span> ${t("sample_presets_label")}
        </div>
        <div class="sample-chips-row">
          <button class="sample-chip" onclick="loadSamplePreset('prescription_augmentin.svg')">
            📝 ${t("sample_rx_chip")}
          </button>
          <button class="sample-chip" onclick="loadSamplePreset('panadol_500mg.svg')">
            💊 ${t("sample_panadol_chip")}
          </button>
          <button class="sample-chip" onclick="loadSamplePreset('arinac_pack.svg')">
            ⚠️ ${t("sample_arinac_chip")}
          </button>
        </div>
      </div>

    </div>
  `;
}

function bindScanEvents() {
  state.capturedImage = null;
  state.sampleFilename = null;
}

// Camera Streaming handlers
async function startCameraCapture() {
  const video = document.getElementById("camera-video");
  const camContainer = document.getElementById("camera-container");
  const uploadArea = document.getElementById("upload-methods-area");

  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "environment" },
      audio: false
    });
    state.cameraStream = stream;
    video.srcObject = stream;
    camContainer.style.display = "block";
    uploadArea.style.display = "none";
  } catch (err) {
    console.warn("Camera access failed:", err);
    alert("کیمرہ تک رسائی نہیں ہو سکی۔ براہِ کرم فائل اپ لوڈ کا آپشن استعمال کریں۔");
  }
}

function stopCamera() {
  if (state.cameraStream) {
    state.cameraStream.getTracks().forEach(t => t.stop());
    state.cameraStream = null;
  }
}

function stopCameraAndShowUpload() {
  stopCamera();
  const camContainer = document.getElementById("camera-container");
  const uploadArea = document.getElementById("upload-methods-area");
  if (camContainer) camContainer.style.display = "none";
  if (uploadArea) uploadArea.style.display = "block";
}

function capturePhotoFromCamera() {
  const video = document.getElementById("camera-video");
  const canvas = document.getElementById("camera-canvas");
  if (!video || !canvas) return;

  canvas.width = video.videoWidth || 640;
  canvas.height = video.videoHeight || 480;
  const ctx = canvas.getContext("2d");
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

  const b64 = canvas.toDataURL("image/jpeg", 0.9);
  stopCamera();
  displayPreview(b64);
}

function handleFileSelected(event) {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = (e) => {
    displayPreview(e.target.result);
  };
  reader.readAsDataURL(file);
}

function loadSamplePreset(filename) {
  state.sampleFilename = filename;
  state.capturedImage = `/api/samples/${filename}`;
  displayPreview(`/api/samples/${filename}`, true);
}

function displayPreview(src, isSample = false) {
  const previewArea = document.getElementById("preview-area");
  const uploadArea = document.getElementById("upload-methods-area");
  const camContainer = document.getElementById("camera-container");
  const previewImg = document.getElementById("preview-img");

  if (camContainer) camContainer.style.display = "none";
  if (uploadArea) uploadArea.style.display = "none";

  previewImg.src = src;
  previewArea.style.display = "block";

  if (!isSample) {
    state.capturedImage = src;
    state.sampleFilename = null;
  }
}

function resetScan() {
  const previewArea = document.getElementById("preview-area");
  const uploadArea = document.getElementById("upload-methods-area");
  state.capturedImage = null;
  state.sampleFilename = null;
  if (previewArea) previewArea.style.display = "none";
  if (uploadArea) uploadArea.style.display = "block";
}

async function processExtraction() {
  const previewArea = document.getElementById("preview-area");
  const loadingArea = document.getElementById("scan-loading-area");

  if (previewArea) previewArea.style.display = "none";
  if (loadingArea) loadingArea.style.display = "flex";

  try {
    const payload = {};
    if (state.sampleFilename) {
      payload.sample_filename = state.sampleFilename;
    } else {
      payload.image_b64 = state.capturedImage;
      payload.mime_type = "image/jpeg";
    }

    const result = await api.scanImage(payload);
    state.extractedMedicine = result;
    navigateTo("verify", { extracted: result });
  } catch (err) {
    console.error("Scan extraction error:", err);
    alert("دوا کی تفصیل حاصل کرنے میں دشواری ہوئی۔ براہِ کرم تصویر دوبارہ لیں یا نمونہ آزمائیں۔");
    resetScan();
  }
}

// ==========================================================================
// VIEW 3: VERIFICATION VIEW ("ہمیں یہ دوا نظر آئی ہے")
// ==========================================================================

function renderVerifyView() {
  const med = state.extractedMedicine || {
    brand_name: "Panadol",
    generic_name: "Paracetamol",
    strength: "500mg",
    formulation: "Tablet (گولی)",
    instructions: "1 tablet after food",
    instructions_ur: "کھانے کے بعد ایک گولی پانی سے لیں۔",
    unclear_notes: ""
  };

  return `
    <div class="verification-card">
      <div class="section-back-bar">
        <button class="back-btn" onclick="navigateTo('scan')">
          <span>⬅</span> ${t("retake_btn")}
        </button>
        <span style="font-size: 15px; color: var(--color-primary); font-weight: 600;">
          مرحلہ 2: تصدیق (Verification)
        </span>
      </div>

      <h2 class="verification-heading">${t("verify_heading")}</h2>
      <p class="verification-sub">${t("verify_sub")}</p>

      ${med.unclear_notes ? `
        <div style="background: #FEF3C7; border: 1.5px solid #F59E0B; border-radius: 12px; padding: 12px 16px; margin-bottom: 20px; font-size: 16px; color: #92400E;">
          ⚠️ ${t("unclear_handwriting_alert")}
        </div>
      ` : ""}

      ${med.candidate_alternatives && med.candidate_alternatives.length > 0 ? `
        <div style="background: #F0FDF4; border: 1.5px solid #BBF7D0; border-radius: 12px; padding: 14px 18px; margin-bottom: 20px;">
          <div style="font-weight: 700; color: #166534; font-size: 16px; margin-bottom: 6px;">
            🔍 ${t("candidate_alternatives_title")}
          </div>
          ${med.is_ambiguous ? `<div style="color: #854D0E; font-size: 14px; margin-bottom: 8px;">⚠️ ${t("ambiguity_alert")}</div>` : ''}
          <div style="display: flex; flex-wrap: wrap; gap: 8px;">
            ${med.candidate_alternatives.map(c => `
              <button type="button" class="sample-chip" onclick="selectCandidateMedicine('${escapeQuotes(c.brand_name)}', '${escapeQuotes(c.generic_name)}', '${escapeQuotes(c.available_strengths[0] || '')}', '${escapeQuotes(c.dosage_forms[0] || 'Tablet')}')">
                💊 <strong>${c.brand_name}</strong> (${c.generic_name}) • ${c.available_strengths[0] || ''}
              </button>
            `).join("")}
          </div>
        </div>
      ` : ''}

      <div class="extracted-fields-list">
        
        <div class="field-group">
          <label class="field-label" for="v-brand">🏷️ ${t("field_brand")}</label>
          <input type="text" id="v-brand" class="field-input" value="${med.brand_name || ''}">
        </div>

        <div class="field-group">
          <label class="field-label" for="v-generic">🧬 ${t("field_generic")}</label>
          <input type="text" id="v-generic" class="field-input" value="${med.generic_name || ''}">
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
          <div class="field-group">
            <label class="field-label" for="v-strength">⚖️ ${t("field_strength")}</label>
            <input type="text" id="v-strength" class="field-input" value="${med.strength || ''}">
          </div>
          <div class="field-group">
            <label class="field-label" for="v-form">💊 ${t("field_formulation")}</label>
            <input type="text" id="v-form" class="field-input" value="${med.formulation || 'Tablet'}">
          </div>
        </div>

        <div class="field-group">
          <label class="field-label" for="v-instructions">📋 ${t("field_instructions")}</label>
          <input type="text" id="v-instructions" class="field-input" value="${getLang() === 'ur' ? (med.instructions_ur || med.instructions || '') : (med.instructions || med.instructions_ur || '')}">
        </div>

      </div>

      <div class="verification-buttons-grid">
        <button class="btn-huge btn-huge-success" onclick="confirmMedicineAndExplain()">
          ✅ ${t("btn_confirm_yes")}
        </button>
        <button class="btn-huge btn-huge-secondary" onclick="navigateTo('scan')">
          🔄 ${t("btn_confirm_no")}
        </button>
      </div>

    </div>
  `;
}

function selectCandidateMedicine(brand, generic, strength, form) {
  const brandInput = document.getElementById("v-brand");
  const genericInput = document.getElementById("v-generic");
  const strengthInput = document.getElementById("v-strength");
  const formInput = document.getElementById("v-form");
  if (brandInput) brandInput.value = brand;
  if (genericInput) genericInput.value = generic;
  if (strengthInput && strength) strengthInput.value = strength;
  if (formInput && form) formInput.value = form;
}

async function confirmMedicineAndExplain() {
  const brand = document.getElementById("v-brand").value.trim();
  const generic = document.getElementById("v-generic").value.trim();
  const strength = document.getElementById("v-strength").value.trim();
  const form = document.getElementById("v-form").value.trim();
  const instructions = document.getElementById("v-instructions").value.trim();

  const medData = {
    brand_name: brand,
    generic_name: generic,
    strength: strength,
    formulation: form,
    instructions: instructions,
    instructions_ur: instructions,
    image_path: state.extractedMedicine?.image_path || ""
  };
  state.activeMedicine = medData;

  // Show loading indicator
  const container = document.getElementById("main-content");
  container.innerHTML = `
    <div class="verification-card loading-pulse-box">
      <div class="pulse-spinner"></div>
      <h2 style="font-size: 24px; color: var(--color-primary);">ڈاکٹر صاحب کا مشورہ تیار کیا جا رہا ہے...</h2>
      <p style="font-size: 18px; color: var(--color-text-muted);">
        آپ کے ہیلتھ ریکارڈ، بیماریوں اور سابقہ دواؤں کو مدنظر رکھتے ہوئے تفصیلی رہنمائی لکھی جا رہی ہے۔
      </p>
    </div>
  `;

  try {
    const explanation = await api.getExplanation(medData, state.activeProfileId, getLang());
    state.activeExplanation = explanation;
    navigateTo("explain", { explanation });
  } catch (err) {
    console.error("Explanation generation failed:", err);
    alert("وضاحت حاصل نہیں ہو سکی۔ براہِ کرم دوبارہ کوشش کریں۔");
    navigateTo("verify");
  }
}

// ==========================================================================
// VIEW 4: DOCTOR PERSONA EXPLANATION VIEW
// ==========================================================================

function renderExplainView() {
  const exp = state.activeExplanation;
  const med = state.activeMedicine;
  if (!exp || !med) return navigateTo("home");

  const fullAudioScript = `
    ڈاکٹر صاحب کا مشورہ برائے ${med.brand_name}۔
    ${exp.emergency_warning ? "خبردار! فوری انتباہ: " + exp.emergency_warning : ""}
    پہلا حصہ: دوا کس کام آتی ہے؟ ${exp.purpose}
    دوسرا حصہ: یہ دوا کیسے لینی ہے؟ ${exp.how_to_take}
    تیسرا حصہ: احتیاط۔ ${exp.precautions}
    چوتھا حصہ: عام نقصانات۔ ${exp.side_effects}
    پانچواں حصہ: خاص احتیاط۔ ${exp.special_care}
    چھٹا حصہ: ڈاکٹر کی طرف سے ایک ضروری بات۔ ${exp.doctor_advisory}
  `;

  return `
    <!-- Doctor Persona Header Banner -->
    <div class="doctor-persona-header">
      <div class="doctor-avatar-wrap">
        👨‍⚕️
      </div>
      <div class="doctor-header-content">
        <h2 class="doctor-header-name">${t("doctor_title")}: ${med.brand_name} ${med.strength || ''}</h2>
        <p class="doctor-header-sub">${med.generic_name || ''} • ${t("doctor_sub")}</p>
      </div>
    </div>

    <!-- Master Audio Player Bar -->
    <div class="master-audio-player">
      <div class="player-left">
        <span style="font-size: 28px;">🎙️</span>
        <div>
          <div class="player-title">${t("listen_all_btn")}</div>
          <div style="font-size: 14px; color: var(--color-text-muted);" id="audio-status-label">بزرگ مریض کے لیے آرام دہ رفتار</div>
        </div>
      </div>
      <div class="player-controls">
        <button class="audio-ctrl-btn btn-play-big" id="btn-master-play" onclick="togglePlayFullAdvice(\`${escapeQuotes(fullAudioScript)}\`)" title="چلائیں">
          ▶️
        </button>
        <button class="audio-ctrl-btn" onclick="audioAssistant.replay()" title="دوبارہ سنیں">
          🔄
        </button>
        <button class="audio-ctrl-btn" onclick="audioAssistant.stop()" title="بند کریں">
          ⏹️
        </button>
      </div>
    </div>

    <!-- Emergency Warning Banner (Triggered if contraindications or severe allergies detected) -->
    ${exp.emergency_warning ? `
      <div class="emergency-warning-banner" id="sec-emergency">
        <div class="emergency-icon-wrap">⚠️</div>
        <div class="emergency-content">
          <div class="emergency-title">فوری انتباہ (CRITICAL MEDICAL ALERT)</div>
          <div class="emergency-text">${exp.emergency_warning}</div>
          <button class="section-listen-btn" style="margin-top: 10px; border-color: #EF4444; color: #991B1B;" onclick="audioAssistant.speak(\`${escapeQuotes(exp.emergency_warning)}\`, { highlightElementId: 'sec-emergency' })">
            🔊 یہ انتباہ سنیں
          </button>
        </div>
      </div>
    ` : ""}

    <!-- The 6 Mandatory Accessible Explanation Section Cards -->
    <div class="explanation-sections-container">
      
      <!-- Section 1: دوا کس کام آتی ہے؟ -->
      <div class="explanation-section-card" id="sec-1">
        <div class="section-card-header">
          <div class="section-title-wrap">
            <span class="section-icon-badge section-1-icon">💊</span>
            <h3 class="section-heading-text">${t("sec_purpose_title")}</h3>
          </div>
          <button class="section-listen-btn" onclick="audioAssistant.speak(\`${escapeQuotes(exp.purpose)}\`, { highlightElementId: 'sec-1' })">
            🔊 ${t("btn_listen_card")}
          </button>
        </div>
        <div class="section-body-text">${exp.purpose}</div>
      </div>

      <!-- Section 2: یہ دوا کیسے لینی ہے؟ -->
      <div class="explanation-section-card" id="sec-2">
        <div class="section-card-header">
          <div class="section-title-wrap">
            <span class="section-icon-badge section-2-icon">🕒</span>
            <h3 class="section-heading-text">${t("sec_how_to_take_title")}</h3>
          </div>
          <button class="section-listen-btn" onclick="audioAssistant.speak(\`${escapeQuotes(exp.how_to_take)}\`, { highlightElementId: 'sec-2' })">
            🔊 ${t("btn_listen_card")}
          </button>
        </div>
        <div class="section-body-text">${exp.how_to_take}</div>
      </div>

      <!-- Section 3: اس دوا سے کیا احتیاط کرنی ہے؟ -->
      <div class="explanation-section-card" id="sec-3">
        <div class="section-card-header">
          <div class="section-title-wrap">
            <span class="section-icon-badge section-3-icon">🛡️</span>
            <h3 class="section-heading-text">${t("sec_precautions_title")}</h3>
          </div>
          <button class="section-listen-btn" onclick="audioAssistant.speak(\`${escapeQuotes(exp.precautions)}\`, { highlightElementId: 'sec-3' })">
            🔊 ${t("btn_listen_card")}
          </button>
        </div>
        <div class="section-body-text">${exp.precautions}</div>
      </div>

      <!-- Section 4: اس دوا کے عام نقصانات کیا ہو سکتے ہیں؟ -->
      <div class="explanation-section-card" id="sec-4">
        <div class="section-card-header">
          <div class="section-title-wrap">
            <span class="section-icon-badge section-4-icon">ℹ️</span>
            <h3 class="section-heading-text">${t("sec_side_effects_title")}</h3>
          </div>
          <button class="section-listen-btn" onclick="audioAssistant.speak(\`${escapeQuotes(exp.side_effects)}\`, { highlightElementId: 'sec-4' })">
            🔊 ${t("btn_listen_card")}
          </button>
        </div>
        <div class="section-body-text">${exp.side_effects}</div>
      </div>

      <!-- Section 5: کن لوگوں کو خاص احتیاط کرنی چاہیے؟ -->
      <div class="explanation-section-card" id="sec-5">
        <div class="section-card-header">
          <div class="section-title-wrap">
            <span class="section-icon-badge section-5-icon">⚠️</span>
            <h3 class="section-heading-text">${t("sec_special_care_title")}</h3>
          </div>
          <button class="section-listen-btn" onclick="audioAssistant.speak(\`${escapeQuotes(exp.special_care)}\`, { highlightElementId: 'sec-5' })">
            🔊 ${t("btn_listen_card")}
          </button>
        </div>
        <div class="section-body-text">${exp.special_care}</div>
      </div>

      <!-- Section 6: ڈاکٹر کی طرف سے ایک ضروری بات -->
      <div class="explanation-section-card" id="sec-6" style="border-color: #A7D7C5; background: #F7FAF8;">
        <div class="section-card-header">
          <div class="section-title-wrap">
            <span class="section-icon-badge section-6-icon">🩺</span>
            <h3 class="section-heading-text" style="color: var(--color-primary);">${t("sec_doctor_advisory_title")}</h3>
          </div>
          <button class="section-listen-btn" onclick="audioAssistant.speak(\`${escapeQuotes(exp.doctor_advisory)}\`, { highlightElementId: 'sec-6' })">
            🔊 ${t("btn_listen_card")}
          </button>
        </div>
        <div class="section-body-text" style="font-weight: 600; color: var(--color-primary-dark);">${exp.doctor_advisory}</div>
      </div>

    </div>

    <!-- Authoritative Sources Attribution Badge -->
    ${exp.sources && exp.sources.length > 0 ? `
      <div style="background: #F8FAFC; border: 1.5px solid #E2E8F0; border-radius: var(--radius-lg); padding: 14px 20px; margin-bottom: 24px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
        <div style="display: flex; align-items: center; gap: 10px; font-size: 15px; color: #334155;">
          <span style="font-size: 20px;">📚</span>
          <strong>${t("medical_sources_label")}</strong>
          <span>${exp.sources.map(s => `<a href="${s.source_url || '#'}" target="_blank" rel="noopener noreferrer" style="color: var(--color-primary); font-weight: 600; text-decoration: underline;">${s.source_name} (${s.jurisdiction})</a>`).join(" • ")}</span>
        </div>
        <span style="background: #DCFCE7; color: #15803D; font-size: 13.5px; font-weight: 700; padding: 4px 12px; border-radius: 20px;">✓ مصدقہ طبی ریکارڈ (Grounded RAG)</span>
      </div>
    ` : ""}

    <!-- Regulatory Discrepancies Callout (if any) -->
    ${exp.discrepancies && exp.discrepancies.length > 0 ? `
      <div style="background: #FFFBEB; border: 1.5px solid #FDE68A; border-radius: var(--radius-lg); padding: 14px 18px; margin-bottom: 22px;">
        <div style="font-weight: 700; color: #92400E; margin-bottom: 4px;">⚖️ علاقائی طبی رہنمائی و بین الاقوامی ماخذ (Regulatory Reference Note):</div>
        <div style="font-size: 16px; color: #78350F;">${exp.discrepancies[0][getLang() === 'ur' ? 'finding_ur' : 'finding_en']}</div>
      </div>
    ` : ""}

    <!-- Conversational Medical Assistant (Ask Doctor Sahib) -->
    <div class="chat-assistant-card" id="chat-assistant-card">
      <div class="chat-assistant-header">
        <div class="chat-doc-avatar">👨‍⚕️</div>
        <div class="chat-title-group">
          <h3>${t("chat_section_title")}</h3>
          <p>${t("chat_section_sub")}</p>
        </div>
      </div>

      <div class="chat-history-box" id="chat-messages-container">
        <div class="chat-bubble chat-bubble-doctor">
          <div>السلام علیکم! آپ مجھ سے <strong>${med.brand_name}</strong> کے استعمال، پرہیز، یا خوراک چھوٹ جانے کے متعلق کوئی بھی سوال بلا جھجھک پوچھ سکتے ہیں۔</div>
          <button class="section-listen-btn" style="align-self: flex-start; margin-top: 4px;" onclick="audioAssistant.speak('السلام علیکم! آپ مجھ سے اس دوا کے متعلق کوئی بھی سوال پوچھ سکتے ہیں۔')">
            🔊 ${t("btn_listen_card")}
          </button>
        </div>
      </div>

      <div class="quick-questions-label">💡 بزرگ مریضوں کے لیے فوری سوالات (Quick Questions):</div>
      <div class="quick-questions-row">
        <button class="quick-q-btn" onclick="sendQuickQuestion(t('quick_q1'))">
          🍽️ ${t("quick_q1")}
        </button>
        <button class="quick-q-btn" onclick="sendQuickQuestion(t('quick_q2'))">
          ⏰ ${t("quick_q2")}
        </button>
        <button class="quick-q-btn" onclick="sendQuickQuestion(t('quick_q3'))">
          😴 ${t("quick_q3")}
        </button>
        <button class="quick-q-btn" onclick="sendQuickQuestion(t('quick_q4'))">
          ℹ️ ${t("quick_q4")}
        </button>
      </div>

      <div class="chat-input-row">
        <input type="text" id="chat-user-input" class="chat-text-input" placeholder="${t('chat_input_placeholder')}" onkeydown="if(event.key === 'Enter') submitChatQuestion()">
        <button class="chat-send-btn" id="btn-chat-send" onclick="submitChatQuestion()">
          <span>💬</span> ${t("btn_ask_doctor")}
        </button>
      </div>
    </div>

    <!-- Actions Bar at Bottom -->
    <div style="display: flex; gap: 16px; flex-wrap: wrap;">
      <button class="btn-huge btn-huge-primary" style="flex: 1;" onclick="saveCurrentMedicineToHistory()">
        💾 ${t("btn_save_to_history")}
      </button>
      <button class="btn-huge btn-huge-secondary" onclick="navigateTo('home')">
        🔍 ${t("btn_scan_another")}
      </button>
    </div>
  `;
}

function togglePlayFullAdvice(script) {
  if (audioAssistant.isPlaying) {
    audioAssistant.pause();
  } else if (audioAssistant.isPaused) {
    audioAssistant.resume();
  } else {
    audioAssistant.speak(script);
  }
}

function updateAudioPlayerState(status) {
  const playBtn = document.getElementById("btn-master-play");
  const label = document.getElementById("audio-status-label");
  if (!playBtn) return;

  if (status === "playing") {
    playBtn.textContent = "⏸️";
    if (label) label.textContent = "وضاحت سنائی جا رہی ہے...";
  } else if (status === "paused") {
    playBtn.textContent = "▶️";
    if (label) label.textContent = "روکا گیا ہے";
  } else {
    playBtn.textContent = "▶️";
    if (label) label.textContent = "بزرگ مریض کے لیے آرام دہ رفتار";
  }
}

async function sendQuickQuestion(questionText) {
  const input = document.getElementById("chat-user-input");
  if (input) input.value = questionText;
  await submitChatQuestion();
}

async function submitChatQuestion() {
  const input = document.getElementById("chat-user-input");
  const sendBtn = document.getElementById("btn-chat-send");
  const container = document.getElementById("chat-messages-container");
  if (!input || !container) return;

  const question = input.value.trim();
  if (!question) return;

  // Add User Message Bubble
  appendChatMessage("user", question);
  input.value = "";
  if (sendBtn) sendBtn.disabled = true;

  // Add Loading Bubble
  const loadingId = "chat-loading-" + Date.now();
  const loadingDiv = document.createElement("div");
  loadingDiv.id = loadingId;
  loadingDiv.className = "chat-bubble chat-bubble-doctor";
  loadingDiv.innerHTML = `<div>⏳ ${t("chat_loading")}</div>`;
  container.appendChild(loadingDiv);
  container.scrollTop = container.scrollHeight;

  try {
    const medName = state.activeMedicine?.brand_name || "Medicine";
    const res = await api.askFollowupQuestion(
      state.chatSessionId,
      state.activeProfileId,
      medName,
      question,
      getLang()
    );

    // Remove loading bubble
    const lEl = document.getElementById(loadingId);
    if (lEl) lEl.remove();

    // Append Doctor Answer Bubble
    appendChatMessage("doctor", res.answer);

  } catch (err) {
    console.error("Chat error:", err);
    const lEl = document.getElementById(loadingId);
    if (lEl) lEl.remove();
    appendChatMessage("doctor", "معذرت، جواب موصول کرنے میں مسئلہ پیش آیا۔ براہِ کرم دوبارہ کوشش فرمائیں۔");
  } finally {
    if (sendBtn) sendBtn.disabled = false;
  }
}

function appendChatMessage(role, text) {
  const container = document.getElementById("chat-messages-container");
  if (!container) return;

  const bubble = document.createElement("div");
  bubble.className = `chat-bubble chat-bubble-${role}`;

  if (role === "doctor") {
    bubble.innerHTML = `
      <div>👨‍⚕️ ${text}</div>
      <button class="section-listen-btn" style="align-self: flex-start; margin-top: 4px;" onclick="audioAssistant.speak(\`${escapeQuotes(text)}\`)">
        🔊 ${t("btn_listen_card")}
      </button>
    `;
  } else {
    bubble.innerHTML = `<div>👤 <strong>آپ:</strong> ${text}</div>`;
  }

  container.appendChild(bubble);
  container.scrollTop = container.scrollHeight;
}

async function saveCurrentMedicineToHistory() {
  if (!state.activeMedicine || !state.activeExplanation) return;
  try {
    await api.saveMedicine(state.activeProfileId, state.activeMedicine, state.activeExplanation);
    alert(t("saved_success_toast"));
    navigateTo("history");
  } catch (err) {
    console.error("Save failed:", err);
    alert("محفوظ کرنے میں مسئلہ ہوا۔");
  }
}

// ==========================================================================
// VIEW 5: MEDICINE HISTORY VIEW ("میری دوائیں")
// ==========================================================================

function renderHistoryView() {
  return `
    <div class="scanner-container">
      
      <div class="section-back-bar">
        <button class="back-btn" onclick="navigateTo('home')">
          <span>⬅</span> ${t("back_to_home")}
        </button>
        <h2 class="page-title">${t("action_my_meds_title")}</h2>
      </div>

      <!-- Filter Tabs -->
      <div class="history-filters-bar">
        <button class="filter-tab ${state.historyFilter === 'all' ? 'active' : ''}" onclick="filterMeds('all')">
          ${t("filter_all")}
        </button>
        <button class="filter-tab ${state.historyFilter === 'active' ? 'active' : ''}" onclick="filterMeds('active')">
          ✅ ${t("filter_active")}
        </button>
        <button class="filter-tab ${state.historyFilter === 'discontinued' ? 'active' : ''}" onclick="filterMeds('discontinued')">
          🛑 ${t("filter_discontinued")}
        </button>
      </div>

      <!-- Medicines Cards List Container -->
      <div id="meds-list-container" class="meds-history-grid">
        <div class="loading-pulse-box">
          <div class="pulse-spinner"></div>
          <div>دوائیں لوڈ ہو رہی ہیں...</div>
        </div>
      </div>

    </div>
  `;
}

async function loadHistoryMeds() {
  const container = document.getElementById("meds-list-container");
  if (!container) return;

  try {
    const statusParam = state.historyFilter === "all" ? null : state.historyFilter;
    const meds = await api.getMedicines(state.activeProfileId, statusParam);

    if (!meds || meds.length === 0) {
      container.innerHTML = `
        <div style="text-align: center; padding: 40px 20px; color: var(--color-text-muted);">
          <div style="font-size: 48px; margin-bottom: 12px;">💊</div>
          <div style="font-size: 19px;">${t("empty_meds_msg")}</div>
        </div>
      `;
      return;
    }

    container.innerHTML = meds.map(m => {
      const isDiscontinued = m.status === "discontinued";
      const exp = m.explanation;
      const audioText = exp ? `${m.brand_name}۔ ${exp.purpose}۔ استعمال: ${exp.how_to_take}` : `${m.brand_name} ${m.strength || ''}`;

      return `
        <div class="med-history-card">
          <div class="med-info-left">
            <div class="med-thumb-icon">
              💊
            </div>
            <div class="med-names-wrap">
              <span class="med-card-brand">${m.brand_name} ${m.strength || ''}</span>
              <span class="med-card-generic">${m.generic_name || m.formulation || ''}</span>
              <span class="med-status-badge ${isDiscontinued ? 'badge-discontinued' : 'badge-active'}">
                ${isDiscontinued ? '🛑 ' + t("filter_discontinued") : '✅ ' + t("filter_active")}
              </span>
            </div>
          </div>

          <div class="med-card-actions">
            <button class="section-listen-btn" onclick="audioAssistant.speak(\`${escapeQuotes(audioText)}\`)">
              🔊 ${t("btn_listen_card")}
            </button>
            ${exp ? `
              <button class="back-btn" onclick="reopenExplanation(${m.id})">
                📖 ${t("btn_details_card")}
              </button>
            ` : ""}
            ${!isDiscontinued ? `
              <button class="back-btn" style="color: #991B1B; border-color: #FCA5A5;" onclick="markDiscontinued(${m.id})">
                🛑 ${t("btn_discontinue_card")}
              </button>
            ` : ""}
          </div>
        </div>
      `;
    }).join("");

  } catch (err) {
    console.error("Failed to load history meds:", err);
    container.innerHTML = `<div style="color: red; text-align: center;">دوائیں حاصل نہ ہو سکیں۔</div>`;
  }
}

function filterMeds(filter) {
  state.historyFilter = filter;
  document.querySelectorAll(".filter-tab").forEach(tab => tab.classList.remove("active"));
  event.target.classList.add("active");
  loadHistoryMeds();
}

async function reopenExplanation(medicineId) {
  try {
    const med = await api.getMedicine(medicineId);
    if (med && med.explanation) {
      state.activeMedicine = med;
      state.activeExplanation = med.explanation;
      navigateTo("explain");
    }
  } catch (err) {
    console.error("Failed to fetch medicine:", err);
  }
}

async function markDiscontinued(medicineId) {
  if (confirm(t("discontinue_confirm_msg"))) {
    await api.updateMedicineStatus(medicineId, "discontinued");
    loadHistoryMeds();
  }
}

// ==========================================================================
// HEALTH PROFILE & FAMILY MODAL
// ==========================================================================

function openProfileModal() {
  const modal = document.getElementById("profile-modal");
  if (!modal) return;
  modal.style.display = "flex";
  renderProfileModalContent();
}

function closeModal() {
  const modal = document.getElementById("profile-modal");
  if (modal) modal.style.display = "none";
}

function renderProfileModalContent() {
  const body = document.getElementById("modal-body-content");
  if (!body || !state.activeProfile) return;

  const prof = state.activeProfile;

  body.innerHTML = `
    <!-- Family Switcher Selector -->
    <div style="margin-bottom: 22px; padding-bottom: 18px; border-bottom: 1.5px solid var(--color-card-border);">
      <label style="font-size: 16px; font-weight: 600; color: var(--color-text-muted); display: block; margin-bottom: 8px;">
        👨‍👩‍👧‍👦 ${t("switch_family_member")}
      </label>
      <div style="display: flex; gap: 8px; flex-wrap: wrap;">
        ${state.allProfiles.map(p => `
          <button class="sample-chip ${p.id === prof.id ? 'active' : ''}" style="${p.id === prof.id ? 'background: var(--color-primary); color: #FFF; border-color: var(--color-primary);' : ''}" onclick="switchProfile(${p.id})">
            ${p.name} (${p.relationship || 'فرد'})
          </button>
        `).join("")}
        <button class="sample-chip" onclick="showAddProfileForm()">
          ${t("add_family_member_btn")}
        </button>
      </div>
    </div>

    <!-- Active Profile Details -->
    <div style="margin-bottom: 20px;">
      <h3 style="font-size: 22px; color: var(--color-primary); margin-bottom: 4px;">${prof.name}</h3>
      <div style="font-size: 16px; color: var(--color-text-muted);">
        ${t("profile_age")} ${prof.age || '--'} ${t("profile_years")} • ${prof.relationship || ''}
      </div>
    </div>

    <!-- Conditions Section -->
    <div style="margin-bottom: 22px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <h4 style="font-size: 18px; color: var(--color-text-main);">🏥 ${t("section_conditions")}</h4>
        <button class="back-btn" style="padding: 4px 12px; font-size: 14px;" onclick="showAddConditionPrompt()">
          ${t("add_condition_btn")}
        </button>
      </div>
      <div style="display: flex; flex-wrap: wrap; gap: 8px;">
        ${prof.conditions && prof.conditions.length > 0 ? prof.conditions.map(c => `
          <span style="background: var(--color-primary-light); color: var(--color-primary-dark); padding: 6px 14px; border-radius: 20px; font-size: 15px; display: inline-flex; align-items: center; gap: 6px;">
            ${c.name_ur || c.name_en}
            <button onclick="removeCondition(${c.id})" style="background: none; border: none; cursor: pointer; color: #991B1B;">×</button>
          </span>
        `).join("") : `<span style="color: var(--color-text-muted); font-size: 15px;">کوئی پرانی بیماری درج نہیں</span>`}
      </div>
    </div>

    <!-- Allergies Section -->
    <div style="margin-bottom: 22px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <h4 style="font-size: 18px; color: var(--color-warning);">⚠️ ${t("section_allergies")}</h4>
        <button class="back-btn" style="padding: 4px 12px; font-size: 14px;" onclick="showAddAllergyPrompt()">
          ${t("add_allergy_btn")}
        </button>
      </div>
      <div style="display: flex; flex-wrap: wrap; gap: 8px;">
        ${prof.allergies && prof.allergies.length > 0 ? prof.allergies.map(a => `
          <span style="background: var(--color-warning-light); color: var(--color-warning); border: 1px solid var(--color-warning-border); padding: 6px 14px; border-radius: 20px; font-size: 15px; display: inline-flex; align-items: center; gap: 6px;">
            ${a.allergen_ur || a.allergen_en}
            <button onclick="removeAllergy(${a.id})" style="background: none; border: none; cursor: pointer; color: #991B1B;">×</button>
          </span>
        `).join("") : `<span style="color: var(--color-text-muted); font-size: 15px;">کوئی دوا الرجی درج نہیں</span>`}
      </div>
    </div>

    <!-- Active Medicines List in Profile -->
    <div style="margin-bottom: 10px;">
      <h4 style="font-size: 18px; color: var(--color-text-main); margin-bottom: 8px;">💊 ${t("section_current_meds")}</h4>
      <div style="display: flex; flex-wrap: wrap; gap: 8px;">
        ${prof.medicines && prof.medicines.filter(m => m.status === 'active').length > 0 ? 
          prof.medicines.filter(m => m.status === 'active').map(m => `
            <span style="background: #F1F5F9; color: #334155; padding: 6px 14px; border-radius: 20px; font-size: 15px;">
              ${m.brand_name} (${m.strength || ''})
            </span>
          `).join("") : `<span style="color: var(--color-text-muted); font-size: 15px;">فی الحال کوئی دوا درج نہیں</span>`}
      </div>
    </div>
  `;
}

async function showAddProfileForm() {
  const name = prompt("نئے مریض یا خاندانی فرد کا نام لکھیں:");
  if (!name) return;
  const rel = prompt("رشتہ داری (مثلاً والدہ، والد، بیٹا، بیٹی، خود):", "خود");
  const age = parseInt(prompt("عمر (سال):", "60")) || 60;

  try {
    const res = await api.createProfile({ name, relationship: rel, age, language: getLang() });
    await loadProfiles();
    switchProfile(res.id);
  } catch (err) {
    alert("پروفائل نہ بن سکی۔");
  }
}

async function showAddConditionPrompt() {
  const cond = prompt("بیماری کا نام درج کریں (مثلاً شوگر، بلڈ پریشر، دمہ):");
  if (!cond) return;
  await api.addCondition(state.activeProfileId, { name_ur: cond, name_en: cond });
  state.activeProfile = await api.getProfile(state.activeProfileId);
  renderProfileModalContent();
}

async function removeCondition(id) {
  if (confirm("کیا آپ اس بیماری کو ہٹانا چاہتے ہیں؟")) {
    await api.deleteCondition(id);
    state.activeProfile = await api.getProfile(state.activeProfileId);
    renderProfileModalContent();
  }
}

async function showAddAllergyPrompt() {
  const allergen = prompt("الرجی کی دوا یا چیز کا نام درج کریں (مثلاً پینسلین، ڈسپرین):");
  if (!allergen) return;
  await api.addAllergy(state.activeProfileId, { allergen_ur: allergen, allergen_en: allergen });
  state.activeProfile = await api.getProfile(state.activeProfileId);
  renderProfileModalContent();
}

async function removeAllergy(id) {
  if (confirm("کیا آپ اس الرجی کو ہٹانا چاہتے ہیں؟")) {
    await api.deleteAllergy(id);
    state.activeProfile = await api.getProfile(state.activeProfileId);
    renderProfileModalContent();
  }
}

function escapeQuotes(str) {
  if (!str) return "";
  return str.replace(/"/g, '&quot;').replace(/'/g, "\\'").replace(/\n/g, ' ');
}
