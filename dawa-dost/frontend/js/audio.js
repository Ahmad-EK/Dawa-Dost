/**
 * Dawa Dost Audio & Speech Synthesis Engine
 * Provides natural speech playback for Urdu & English with elderly-friendly pacing (0.85x),
 * play/pause/replay/stop controls, section-by-section audio, and UI voice assistance.
 */

class AudioController {
  constructor() {
    this.synth = window.speechSynthesis || null;
    this.currentUtterance = null;
    this.isPlaying = false;
    this.isPaused = false;
    this.currentText = "";
    this.currentElementId = null;
    this.onStatusChange = null;

    // Load available browser voices
    this.voices = [];
    if (this.synth) {
      this.loadVoices();
      if (speechSynthesis.onvoiceschanged !== undefined) {
        speechSynthesis.onvoiceschanged = () => this.loadVoices();
      }
    }
  }

  loadVoices() {
    if (!this.synth) return;
    this.voices = this.synth.getVoices();
  }

  getBestVoice(lang) {
    if (!this.voices || this.voices.length === 0) {
      this.loadVoices();
    }

    if (lang === "ur") {
      // Look for Urdu specific voice first
      const urVoice = this.voices.find(v => v.lang.startsWith("ur") || v.name.toLowerCase().includes("urdu"));
      if (urVoice) return urVoice;

      // Fallback to high quality Arabic or Hindi or Indian English voice that renders phonetic Urdu reasonably
      const arVoice = this.voices.find(v => v.lang.startsWith("ar"));
      if (arVoice) return arVoice;

      const hiVoice = this.voices.find(v => v.lang.startsWith("hi"));
      if (hiVoice) return hiVoice;
    } else {
      // English voice
      const enVoice = this.voices.find(v => v.lang.startsWith("en-US") || v.lang.startsWith("en-GB") || v.lang.startsWith("en"));
      if (enVoice) return enVoice;
    }

    return this.voices[0] || null;
  }

  speak(text, options = {}) {
    if (!this.synth) {
      console.warn("SpeechSynthesis not supported on this browser");
      return;
    }

    this.stop(); // Stop any active speech

    const lang = options.lang || getLang();
    const rate = options.rate || (lang === "ur" ? 0.85 : 0.9); // Comfortable slower pace for elderly
    const pitch = options.pitch || 1.0;
    const highlightElementId = options.highlightElementId || null;

    // Clean text of markdown or special characters
    const cleanText = text.replace(/[*#_~`]/g, " ").replace(/\s+/g, " ").trim();
    if (!cleanText) return;

    this.currentText = cleanText;
    this.currentElementId = highlightElementId;

    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.lang = lang === "ur" ? "ur-PK" : "en-US";
    utterance.rate = rate;
    utterance.pitch = pitch;

    const voice = this.getBestVoice(lang);
    if (voice) {
      utterance.voice = voice;
    }

    utterance.onstart = () => {
      this.isPlaying = true;
      this.isPaused = false;
      this._updateHighlight(true);
      if (this.onStatusChange) this.onStatusChange("playing");
    };

    utterance.onpause = () => {
      this.isPlaying = false;
      this.isPaused = true;
      if (this.onStatusChange) this.onStatusChange("paused");
    };

    utterance.onresume = () => {
      this.isPlaying = true;
      this.isPaused = false;
      if (this.onStatusChange) this.onStatusChange("playing");
    };

    utterance.onend = () => {
      this.isPlaying = false;
      this.isPaused = false;
      this._updateHighlight(false);
      if (this.onStatusChange) this.onStatusChange("stopped");
    };

    utterance.onerror = (e) => {
      console.warn("SpeechSynthesis error:", e);
      this.isPlaying = false;
      this.isPaused = false;
      this._updateHighlight(false);
      if (this.onStatusChange) this.onStatusChange("stopped");
    };

    this.currentUtterance = utterance;
    this.synth.speak(utterance);
  }

  pause() {
    if (this.synth && this.isPlaying) {
      this.synth.pause();
      this.isPlaying = false;
      this.isPaused = true;
      if (this.onStatusChange) this.onStatusChange("paused");
    }
  }

  resume() {
    if (this.synth && this.isPaused) {
      this.synth.resume();
      this.isPlaying = true;
      this.isPaused = false;
      if (this.onStatusChange) this.onStatusChange("playing");
    }
  }

  replay() {
    if (this.currentText) {
      this.speak(this.currentText, {
        lang: getLang(),
        highlightElementId: this.currentElementId
      });
    }
  }

  stop() {
    if (this.synth) {
      this.synth.cancel();
      this.isPlaying = false;
      this.isPaused = false;
      this._updateHighlight(false);
      if (this.onStatusChange) this.onStatusChange("stopped");
    }
  }

  _updateHighlight(active) {
    // Remove active highlight from all cards
    document.querySelectorAll(".speaking-active").forEach(el => {
      el.classList.remove("speaking-active");
    });

    if (active && this.currentElementId) {
      const el = document.getElementById(this.currentElementId);
      if (el) {
        el.classList.add("speaking-active");
        el.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }
    }
  }

  // Voice narration for UI elements (e.g. "نسخے کی تصویر لینے کے لیے یہاں دبائیں")
  narrateUI(key) {
    const phrase = t(key);
    this.speak(phrase, { rate: 0.9 });
  }
}

// Global audio singleton
const audioAssistant = new AudioController();
