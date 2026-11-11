"""
Dawa Dost Backend Server (Expanded Architecture)
A zero-external-dependency, threaded HTTP/REST server powering Dawa Dost.
Serves API endpoints, Gemini AI intelligence engine, medical knowledge retrieval,
clinical condition cross-checks, multi-turn follow-up dialogue, and frontend assets.
"""

import os
import sys
import json
import base64
import mimetypes
import urllib.parse
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from datetime import datetime

# Add current directory to path
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURR_DIR)
if CURR_DIR not in sys.path:
    sys.path.insert(0, CURR_DIR)

import database
from gemini_service import GeminiService, get_api_key, get_configured_model
from medicine_knowledge_service import MedicineKnowledgeService
from medical_condition_service import MedicalConditionService
from drug_interaction_service import DrugInteractionService
from medical_source_service import MedicalSourceService
from patient_context_service import PatientContextService

FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")
SAMPLES_DIR = os.path.join(PROJECT_ROOT, "samples")
UPLOADS_DIR = os.path.join(PROJECT_ROOT, "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)


class DawaDostRequestHandler(BaseHTTPRequestHandler):
    """Handles all API and static file requests."""

    def _set_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def do_OPTIONS(self):
        self.send_response(204)
        self._set_cors_headers()
        self.end_headers()

    def _send_json(self, data, status_code=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._set_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def _send_error(self, message, status_code=400, detail=""):
        self._send_json({"error": message, "detail": detail}, status_code=status_code)

    def _read_json_body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            return {}
        raw = self.rfile.read(content_length).decode("utf-8")
        return json.loads(raw)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        try:
            # --- API ROUTES ---
            if path == "/api/health":
                api_key = get_api_key()
                self._send_json({
                    "status": "healthy",
                    "gemini_active": bool(api_key),
                    "gemini_model": get_configured_model(),
                    "gemini_mode": "cloud_ai_connected" if api_key else "local_clinical_formulary_fallback",
                    "database": "sqlite_connected",
                    "knowledge_entries": len(MedicineKnowledgeService.get_all_medicines()),
                    "conditions_count": len(MedicalConditionService.get_all_conditions()),
                    "time": datetime.now().isoformat()
                })
                return

            if path == "/api/profiles":
                profiles = database.get_all_profiles()
                self._send_json(profiles)
                return

            if path.startswith("/api/profiles/"):
                parts = path.strip("/").split("/")
                profile_id = int(parts[2])
                profile = database.get_profile_by_id(profile_id)
                if not profile:
                    self._send_error("Profile not found", 404)
                else:
                    self._send_json(profile)
                return

            # Medical Knowledge Medicines Search
            if path == "/api/knowledge/medicines":
                search_q = query.get("q", [""])[0].strip()
                if search_q:
                    res = MedicineKnowledgeService.search_medicines(search_q, limit=6)
                    self._send_json(res)
                else:
                    all_meds = MedicineKnowledgeService.get_all_medicines()
                    self._send_json({"total": len(all_meds), "medicines": all_meds})
                return

            # Medical Conditions Directory
            if path == "/api/knowledge/conditions":
                conditions = MedicalConditionService.get_all_conditions()
                self._send_json(conditions)
                return

            # Medical Sources Directory
            if path == "/api/knowledge/sources":
                sources = MedicalSourceService.get_sources()
                self._send_json(sources)
                return

            # Conversation History for multi-turn dialogues
            if path == "/api/chat/history":
                session_id = query.get("session_id", [""])[0].strip()
                if not session_id:
                    self._send_error("session_id parameter required", 400)
                else:
                    history = database.get_conversation_history(session_id)
                    self._send_json(history)
                return

            if path == "/api/medicines":
                profile_id = int(query.get("profile_id", [1])[0])
                status = query.get("status", [None])[0]
                meds = database.get_medicines_by_profile(profile_id, status_filter=status)
                self._send_json(meds)
                return

            if path.startswith("/api/medicines/"):
                parts = path.strip("/").split("/")
                med_id = int(parts[2])
                med = database.get_medicine_with_explanation(med_id)
                if not med:
                    self._send_error("Medicine not found", 404)
                else:
                    self._send_json(med)
                return

            if path == "/api/samples":
                manifest_path = os.path.join(SAMPLES_DIR, "manifest.json")
                if os.path.exists(manifest_path):
                    with open(manifest_path, "r", encoding="utf-8") as f:
                        samples = json.load(f)
                    self._send_json(samples)
                else:
                    self._send_json([])
                return

            if path.startswith("/api/samples/"):
                filename = os.path.basename(path)
                sample_file = os.path.join(SAMPLES_DIR, filename)
                if os.path.exists(sample_file):
                    self._serve_file(sample_file)
                else:
                    self._send_error("Sample not found", 404)
                return

            if path.startswith("/uploads/"):
                filename = os.path.basename(path)
                upload_file = os.path.join(UPLOADS_DIR, filename)
                if os.path.exists(upload_file):
                    self._serve_file(upload_file)
                else:
                    self._send_error("File not found", 404)
                return

            # --- STATIC FRONTEND FILES ---
            clean_path = path.lstrip("/")
            if not clean_path or clean_path == "index.html":
                filepath = os.path.join(FRONTEND_DIR, "index.html")
            else:
                filepath = os.path.join(FRONTEND_DIR, clean_path)

            if os.path.exists(filepath) and os.path.isfile(filepath):
                self._serve_file(filepath)
            else:
                index_path = os.path.join(FRONTEND_DIR, "index.html")
                if os.path.exists(index_path):
                    self._serve_file(index_path)
                else:
                    self._send_error("Not found", 404)

        except Exception as e:
            self._send_error("Internal server error", 500, str(e))

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        try:
            body = self._read_json_body()

            if path == "/api/profiles":
                name = body.get("name", "").strip()
                if not name:
                    return self._send_error("Profile name is required", 400)
                pid = database.create_profile(
                    name=name,
                    relationship=body.get("relationship", "خود"),
                    age=body.get("age"),
                    gender=body.get("gender"),
                    language=body.get("language", "ur"),
                    notes=body.get("notes", "")
                )
                return self._send_json({"id": pid, "message": "Profile created successfully"}, 201)

            if path.startswith("/api/profiles/") and path.endswith("/conditions"):
                parts = path.strip("/").split("/")
                profile_id = int(parts[2])
                name_ur = body.get("name_ur", "").strip()
                name_en = body.get("name_en", "").strip()
                if not name_ur and not name_en:
                    return self._send_error("Condition name is required", 400)
                cid = database.add_condition(
                    profile_id=profile_id,
                    name_ur=name_ur or name_en,
                    name_en=name_en or name_ur,
                    diagnosed_year=body.get("diagnosed_year", ""),
                    notes=body.get("notes", "")
                )
                return self._send_json({"id": cid, "message": "Condition added"}, 201)

            if path.startswith("/api/profiles/") and path.endswith("/allergies"):
                parts = path.strip("/").split("/")
                profile_id = int(parts[2])
                allergen_ur = body.get("allergen_ur", "").strip()
                allergen_en = body.get("allergen_en", "").strip()
                if not allergen_ur and not allergen_en:
                    return self._send_error("Allergen name is required", 400)
                aid = database.add_allergy(
                    profile_id=profile_id,
                    allergen_ur=allergen_ur or allergen_en,
                    allergen_en=allergen_en or allergen_ur,
                    severity=body.get("severity", "high"),
                    reaction=body.get("reaction", "")
                )
                return self._send_json({"id": aid, "message": "Allergy added"}, 201)

            if path == "/api/scan":
                # Multimodal vision scan (image base64 or sample filename)
                image_b64 = body.get("image_b64", "")
                sample_filename = body.get("sample_filename", "")
                mime_type = body.get("mime_type", "image/jpeg")

                if sample_filename:
                    sample_path = os.path.join(SAMPLES_DIR, sample_filename)
                    if os.path.exists(sample_path):
                        with open(sample_path, "rb") as f:
                            raw_bytes = f.read()
                            image_b64 = base64.b64encode(raw_bytes).decode("utf-8")
                            if sample_filename.endswith(".svg"):
                                mime_type = "image/svg+xml"
                            elif sample_filename.endswith(".png"):
                                mime_type = "image/png"

                if not image_b64:
                    return self._send_error("Image data is required", 400)

                saved_image_path = ""
                if not sample_filename:
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    ext = "png" if "png" in mime_type else "jpg"
                    fn = f"scan_{ts}.{ext}"
                    filepath = os.path.join(UPLOADS_DIR, fn)
                    try:
                        clean_b64 = image_b64.split(",", 1)[-1] if "," in image_b64 else image_b64
                        with open(filepath, "wb") as f:
                            f.write(base64.b64decode(clean_b64))
                        saved_image_path = f"/uploads/{fn}"
                    except Exception as e:
                        print(f"Could not save upload: {e}")
                else:
                    saved_image_path = f"/api/samples/{sample_filename}"

                # Central Gemini Vision Analysis
                extracted = GeminiService.analyze_medicine_image(
                    image_b64=image_b64,
                    mime_type=mime_type,
                    image_filename=sample_filename
                )
                extracted["image_path"] = saved_image_path
                return self._send_json(extracted)

            if path == "/api/explain":
                medicine_data = body.get("medicine", {})
                profile_id = int(body.get("profile_id", 1))
                language = body.get("language", "ur")

                # Central Grounded RAG Explanation
                explanation = GeminiService.generate_rag_doctor_explanation(
                    medicine_data=medicine_data,
                    profile_id=profile_id,
                    language=language
                )
                return self._send_json(explanation)

            if path == "/api/chat/followup":
                # Multi-turn conversational medical assistant
                session_id = body.get("session_id", "").strip() or f"sess_{int(datetime.now().timestamp())}"
                profile_id = int(body.get("profile_id", 1))
                medicine_name = body.get("medicine_name", "").strip()
                question = body.get("question", "").strip()
                language = body.get("language", "ur")

                if not question:
                    return self._send_error("Question text is required", 400)

                answer_data = GeminiService.answer_followup_question(
                    session_id=session_id,
                    profile_id=profile_id,
                    medicine_name=medicine_name,
                    question=question,
                    language=language
                )
                return self._send_json(answer_data)

            if path == "/api/medicines":
                profile_id = int(body.get("profile_id", 1))
                med_data = body.get("medicine", {})
                exp_data = body.get("explanation", {})

                med_id = database.save_medicine(
                    profile_id=profile_id,
                    brand_name=med_data.get("brand_name", "Unknown Medicine"),
                    generic_name=med_data.get("generic_name", ""),
                    strength=med_data.get("strength", ""),
                    formulation=med_data.get("formulation", "Tablet"),
                    instructions=med_data.get("instructions", ""),
                    instructions_ur=med_data.get("instructions_ur", ""),
                    status=med_data.get("status", "active"),
                    image_path=med_data.get("image_path", "")
                )

                if exp_data:
                    database.save_explanation(
                        medicine_id=med_id,
                        language=exp_data.get("language", "ur"),
                        purpose=exp_data.get("purpose", ""),
                        how_to_take=exp_data.get("how_to_take", ""),
                        precautions=exp_data.get("precautions", ""),
                        side_effects=exp_data.get("side_effects", ""),
                        special_care=exp_data.get("special_care", ""),
                        doctor_advisory=exp_data.get("doctor_advisory", ""),
                        emergency_warning=exp_data.get("emergency_warning", ""),
                        personalized_warnings=exp_data.get("personalized_warnings", [])
                    )

                return self._send_json({"id": med_id, "message": "Medicine saved successfully"}, 201)

            if path == "/api/check-interactions":
                candidate_med = body.get("medicine_name", "")
                profile_id = int(body.get("profile_id", 1))

                profile = database.get_profile_by_id(profile_id)
                if not profile:
                    return self._send_error("Profile not found", 404)

                res = DrugInteractionService.check_interactions(candidate_med, profile.get("medicines", []))
                return self._send_json({"interactions": res, "total": len(res)})

            self._send_error("Not found", 404)

        except Exception as e:
            self._send_error("Internal server error", 500, str(e))

    def do_PUT(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        try:
            body = self._read_json_body()

            if path.startswith("/api/profiles/"):
                parts = path.strip("/").split("/")
                profile_id = int(parts[2])
                database.update_profile(
                    profile_id=profile_id,
                    name=body.get("name", ""),
                    relationship=body.get("relationship", "خود"),
                    age=body.get("age"),
                    gender=body.get("gender"),
                    language=body.get("language", "ur"),
                    notes=body.get("notes", "")
                )
                return self._send_json({"message": "Profile updated"})

            if path.startswith("/api/medicines/") and path.endswith("/status"):
                parts = path.strip("/").split("/")
                med_id = int(parts[2])
                status = body.get("status", "active")
                database.update_medicine_status(med_id, status)
                return self._send_json({"message": f"Medicine marked as {status}"})

            self._send_error("Not found", 404)
        except Exception as e:
            self._send_error("Internal server error", 500, str(e))

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        try:
            if path.startswith("/api/profiles/"):
                parts = path.strip("/").split("/")
                profile_id = int(parts[2])
                database.delete_profile(profile_id)
                return self._send_json({"message": "Profile deleted"})

            if path.startswith("/api/conditions/"):
                parts = path.strip("/").split("/")
                cond_id = int(parts[2])
                database.delete_condition(cond_id)
                return self._send_json({"message": "Condition deleted"})

            if path.startswith("/api/allergies/"):
                parts = path.strip("/").split("/")
                allergy_id = int(parts[2])
                database.delete_allergy(allergy_id)
                return self._send_json({"message": "Allergy deleted"})

            if path.startswith("/api/medicines/"):
                parts = path.strip("/").split("/")
                med_id = int(parts[2])
                database.delete_medicine(med_id)
                return self._send_json({"message": "Medicine deleted"})

            self._send_error("Not found", 404)
        except Exception as e:
            self._send_error("Internal server error", 500, str(e))

    def _serve_file(self, filepath):
        try:
            mimetype, _ = mimetypes.guess_type(filepath)
            if not mimetype:
                if filepath.endswith(".svg"):
                    mimetype = "image/svg+xml"
                else:
                    mimetype = "application/octet-stream"

            with open(filepath, "rb") as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-Type", f"{mimetype}; charset=utf-8" if "text" in mimetype or "javascript" in mimetype or "json" in mimetype else mimetype)
            self.send_header("Content-Length", str(len(content)))
            self._set_cors_headers()
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self._send_error("File read error", 500, str(e))


def run_server(port=8080):
    database.init_db()
    
    ports_to_try = [port, 8000, 8081, 5000, 3000]
    httpd = None
    selected_port = port

    for p in ports_to_try:
        try:
            server_address = ("0.0.0.0", p)
            httpd = ThreadingHTTPServer(server_address, DawaDostRequestHandler)
            selected_port = p
            break
        except OSError:
            continue

    if not httpd:
        server_address = ("127.0.0.1", port)
        httpd = ThreadingHTTPServer(server_address, DawaDostRequestHandler)
        selected_port = port

    print(f"==================================================")
    print(f"   DAWA DOST (دوا دوست) SERVER RUNNING")
    print(f"   Open in browser: http://localhost:{selected_port}")
    print(f"   Alternative:    http://127.0.0.1:{selected_port}")
    print(f"   Database:       Initialized and connected")
    api_key = get_api_key()
    model = get_configured_model()
    if api_key:
        print(f"   Gemini AI Mode: Cloud Multimodal Active (Model: {model})")
    else:
        print(f"   Gemini AI Mode: Local Clinical Formulary (Set GEMINI_API_KEY in .env for Cloud)")
    print(f"==================================================")
    print(f"   Press Ctrl+C to stop the server at any time.\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Dawa Dost server... Goodbye!")
        httpd.server_close()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    run_server(port)
