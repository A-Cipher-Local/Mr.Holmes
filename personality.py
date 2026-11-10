#!/usr/bin/env python3
# ==============================================================================
# Advanced OSINT Behavioral Telemetry & Personality Engine (`personality.py`)
# ==============================================================================

import os
import json

PROFILE_JSON_PATH = "GUI/Reports/tammy_profile_schema.json"
MATRIX_JSON_PATH = "GUI/Reports/directional_edge_matrix.json"

class PersonalityEngine:
    def __init__(self):
        self.profile = self._load_json(PROFILE_JSON_PATH)
        self.matrix = self._load_json(MATRIX_JSON_PATH)

    def _load_json(self, path):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def calculate_rhetorical_ratios(self) -> dict:
        """Computes normalized behavioral metrics for precise prompt guidance."""
        heuristics = self.profile.get("behavioral_heuristics", {})
        total_events = max(self.profile.get("metrics", {}).get("total_events", 1), 1)
        
        return {
            "question_rate": round(heuristics.get("interrogative_probing", 0) / total_events, 2),
            "caps_emphasis_rate": round(heuristics.get("caps_emphasis", 0) / total_events, 2),
            "exclamation_rate": round(heuristics.get("exclamation_intensity", 0) / total_events, 2),
            "hesitation_rate": round(heuristics.get("hesitation_ellipsis", 0) / total_events, 2)
        }

    def generate_system_prompt_injection(self) -> str:
        """Generates structured behavioral context for LLM system prompts with strict pacing rules."""
        if not self.profile:
            return "[!] Profile schema missing. Run build_persona_graph.py."

        subject = self.profile.get("subject", "tammybusagi")
        heuristics = self.profile.get("behavioral_heuristics", {})
        cultural = self.profile.get("cultural_ecosystem_alignment", {})
        lexicon = self.profile.get("dominant_vocabulary", [])
        metrics = self.profile.get("metrics", {})
        ratios = self.calculate_rhetorical_ratios()

        prompt = f"""[SYSTEM BEHAVIORAL PROFILE INJECTION: @{subject}]
CORE DIRECTIVE: You are simulating the rhetorical heuristics, conversational pacing, and structural habits extracted from telemetry for @{subject}.

1. STRUCTURAL & PACING RULES:
- Target Post Length: Keep responses concise, averaging ~{metrics.get('avg_words_per_event', 13.15)} words per output block.
- Broadcast vs. Direct: Lean heavily into observation and broadcast statements, reserving direct replies for specific engagement triggers.

2. RHETORICAL SIGNATURE (Normalized Ratios):
- Interrogative Probing: Active question bias ({ratios['question_rate']} per statement). Use questions to drive engagement.
- Emphasis Style: Frequent uppercase formatting for emphasis ({ratios['caps_emphasis_rate']} per statement).
- Punctuation Rhythm: Controlled exclamation intensity ({ratios['exclamation_rate']}) balanced with hesitation pauses ({ratios['hesitation_rate']}).

3. LEXICAL ANCHORS & DOMAIN VECTORS:
- Primary Ecosystem Focus: Video and commentary streams ({dict(cultural)}).
- Mandatory Vocabulary Tokens: Integrate natural usage of core anchors: {', '.join(lexicon)}.

4. NETWORK AWARENESS:
- Maintain awareness of primary ecosystem nodes and interaction targets (@wonderosa, @sanjthompson, @ninarazzipr, @og_grim, @hikkipedia) when discussing community events or media.
""".strip()
        return prompt

    def get_character_card(self) -> dict:
        """Returns structured metadata for local LLM character generation."""
        return {
            "name": self.profile.get("subject", "tammybusagi"),
            "system_prompt": self.generate_system_prompt_injection(),
            "heuristics": self.profile.get("behavioral_heuristics", {}),
            "ratios": self.calculate_rhetorical_ratios(),
            "lexicon": self.profile.get("dominant_vocabulary", [])
        }

    def export_modelfile_system_prompt(self, output_path="GUI/Reports/modelfile_system.txt"):
        """Exports system prompt formatted specifically for Ollama/llama.cpp Modelfiles."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        content = f'SYSTEM """\n{self.generate_system_prompt_injection()}\n"""'
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[+] Advanced Modelfile format saved to {output_path}")

if __name__ == "__main__":
    engine = PersonalityEngine()
    card = engine.get_character_card()
    print("[*] Successfully compiled advanced personality module.")
    engine.export_modelfile_system_prompt()
