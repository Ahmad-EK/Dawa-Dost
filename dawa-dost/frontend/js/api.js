/**
 * Dawa Dost API Client
 * Clean asynchronous wrappers for backend REST services.
 */

const API_BASE = ""; // Relative to server root

const api = {
  async getHealth() {
    const res = await fetch(`${API_BASE}/api/health`);
    return await res.json();
  },

  async getProfiles() {
    const res = await fetch(`${API_BASE}/api/profiles`);
    return await res.json();
  },

  async getProfile(id) {
    const res = await fetch(`${API_BASE}/api/profiles/${id}`);
    if (!res.ok) throw new Error("Profile not found");
    return await res.json();
  },

  async createProfile(data) {
    const res = await fetch(`${API_BASE}/api/profiles`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: jsonStringify(data)
    });
    return await res.json();
  },

  async addCondition(profileId, data) {
    const res = await fetch(`${API_BASE}/api/profiles/${profileId}/conditions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: jsonStringify(data)
    });
    return await res.json();
  },

  async deleteCondition(id) {
    const res = await fetch(`${API_BASE}/api/conditions/${id}`, { method: "DELETE" });
    return await res.json();
  },

  async addAllergy(profileId, data) {
    const res = await fetch(`${API_BASE}/api/profiles/${profileId}/allergies`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: jsonStringify(data)
    });
    return await res.json();
  },

  async deleteAllergy(id) {
    const res = await fetch(`${API_BASE}/api/allergies/${id}`, { method: "DELETE" });
    return await res.json();
  },

  async getMedicines(profileId, status = null) {
    let url = `${API_BASE}/api/medicines?profile_id=${profileId}`;
    if (status) url += `&status=${status}`;
    const res = await fetch(url);
    return await res.json();
  },

  async getMedicine(id) {
    const res = await fetch(`${API_BASE}/api/medicines/${id}`);
    return await res.json();
  },

  async scanImage(payload) {
    const res = await fetch(`${API_BASE}/api/scan`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: jsonStringify(payload)
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.error || "Image scan failed");
    }
    return await res.json();
  },

  async getExplanation(medicine, profileId, language) {
    const res = await fetch(`${API_BASE}/api/explain`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: jsonStringify({
        medicine,
        profile_id: profileId,
        language
      })
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.error || "Explanation failed");
    }
    return await res.json();
  },

  async askFollowupQuestion(sessionId, profileId, medicineName, question, language) {
    const res = await fetch(`${API_BASE}/api/chat/followup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: jsonStringify({
        session_id: sessionId,
        profile_id: profileId,
        medicine_name: medicineName,
        question: question,
        language: language
      })
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.error || "Followup question failed");
    }
    return await res.json();
  },

  async searchKnowledge(query) {
    const res = await fetch(`${API_BASE}/api/knowledge/medicines?q=${encodeURIComponent(query)}`);
    return await res.json();
  },

  async saveMedicine(profileId, medicine, explanation) {
    const res = await fetch(`${API_BASE}/api/medicines`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: jsonStringify({
        profile_id: profileId,
        medicine,
        explanation
      })
    });
    return await res.json();
  },

  async updateMedicineStatus(id, status) {
    const res = await fetch(`${API_BASE}/api/medicines/${id}/status`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: jsonStringify({ status })
    });
    return await res.json();
  },

  async getSamples() {
    const res = await fetch(`${API_BASE}/api/samples`);
    return await res.json();
  }
};

function jsonStringify(obj) {
  return JSON.stringify(obj);
}
