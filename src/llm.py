"""
Refactored LLM Generator with JSON KB Support
- Supports JSON/Markdown knowledge base
- Smart API fallback
- Analytics-driven responses
"""
import os
import json
import hashlib
import time
import random
from pathlib import Path
from dotenv import load_dotenv
import concurrent.futures

# Load env variables
load_dotenv()

# Check Gemini API availability
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

try:
    if GEMINI_API_KEY:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        GENAI_AVAILABLE = True
    else:
        GENAI_AVAILABLE = False
except Exception:
    GENAI_AVAILABLE = False


class LLMGenerator:
    def __init__(self):
        self.cache_dir = Path("data/cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / "llm_cache.json"
        self.cache = self._load_cache()

        # Initialize Gemini model if available
        self.api_available = False
        self.model = None
        self.rate_limited_until = None

        if GENAI_AVAILABLE:
            try:
                self.model = genai.GenerativeModel("gemini-2.0-flash")
                print("Gemini API initialized successfully (gemini-2.0-flash)")
                self.api_available = True
            except Exception as e:
                print(f"Gemini initialization failed: {e}")
                self.api_available = False
        else:
            print("Gemini API not available - using fallback extraction")

        self.system_prompt = """
You are an expert AI Analytics Assistant for the Saylani Medical Help Desk.

Your job is to interpret medical analytics data and explain visualizations to administrators.

RULES:
- Use exact numbers from context (never generate new ones)
- Interpret trends, patterns, peaks, changes
- Use percentages & numeric comparisons where relevant
- Professional, clear tone
- No medical advice
- Only explain analytics that exist in the data

FORMAT:
- Bullets for lists
- Bold important metrics
- End with a 1-2 line insight summary
"""

    # -------------------------------------
    # CACHE HELPERS
    # -------------------------------------
    def _load_cache(self):
        if self.cache_file.exists():
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_cache(self):
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self.cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Cache save failed: {e}")

    def _get_cache_key(self, query, context_text):
        base = f"{query}|{context_text[:500]}"
        return hashlib.md5(base.encode()).hexdigest()

    # -------------------------------------
    # MAIN RESPONSE GENERATION
    # -------------------------------------
    def generate_answer(self, query, context_text):
        cache_key = self._get_cache_key(query, context_text)

        # Serve from cache
        if cache_key in self.cache:
            print("Using cached response")
            return self.cache[cache_key]

        # TRY GEMINI API FIRST - respect rate-limit and user model selection
        now = time.time()
        if self.rate_limited_until and now < self.rate_limited_until:
            print("Gemini API currently rate-limited; using fallback KB extraction")
        elif self.api_available and self.model:
            try:
                prompt = f"""
{self.system_prompt}

=== ANALYTICS DATA START ===
{context_text}
=== ANALYTICS DATA END ===

ADMIN QUESTION:
{query}

ANSWER (interpret analytics only):
"""

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(self.model.generate_content, prompt)
                    response = future.result(timeout=8)

                answer = response.text

                # Cache
                self.cache[cache_key] = answer
                self._save_cache()

                print("Gemini Response Generated")
                return answer

            except concurrent.futures.TimeoutError:
                print("API Timeout - using fallback KB extraction")
            except Exception as e:
                # Detect 429 (resource exhausted) and set a cooldown
                if "429" in str(e) or "Resource exhausted" in str(e):
                    self.rate_limited_until = time.time() + 300  # 5-minute pause
                    print("API Failure: 429 Resource exhausted - entering cooldown (5 min)")
                else:
                    print(f"API Failure: {e}")

if __name__ == "__main__":
    llm = LLMGenerator()
    context = """
=== ANALYTICS SUMMARY ===
Total Patients: 200
Total Doctors: 15

=== DISEASE TRENDS ===
- Dengue: 21 cases
- Flu: 15 cases

=== DOCTOR WORKLOAD ===
Dr Ali: 20 visits
Dr Sara: 17 visits

=== GEOGRAPHIC DISTRIBUTION ===
Gulshan: 80 visits
Korangi: 50 visits
"""
    print(llm.generate_answer("What is the most common disease?", context))
