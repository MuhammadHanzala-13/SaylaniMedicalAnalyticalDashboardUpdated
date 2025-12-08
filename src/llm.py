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
import concurrent.futures
from pathlib import Path
from dotenv import load_dotenv

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
                # List of models to try in order of preference
                candidate_models = [
                    "gemini-2.5-flash",
                    "gemini-2.0-flash",
                    "gemini-2.0-flash-lite-preview-02-05",
                    "gemini-2.0-flash-001"
                ]
                
                selected_model = None
                for model_name in candidate_models:
                    try:
                        # Test if model works
                        test_model = genai.GenerativeModel(model_name)
                        # Quick generation test to fail fast if model not found/supported
                        test_model.generate_content("test") 
                        selected_model = model_name
                        self.model = test_model
                        print(f"Gemini API initialized successfully ({selected_model})")
                        self.api_available = True
                        break
                    except Exception as e:
                        print(f"Model {model_name} failed: {e}")
                        continue
                
                if not self.api_available:
                    print("All Gemini models failed to initialize.")

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
        if context_text is None:
            context_text = ""
        base = f"{query}|{context_text[:500]}"
        return hashlib.md5(base.encode()).hexdigest()

    # -------------------------------------
    # MAIN RESPONSE GENERATION
    # -------------------------------------
    def generate_answer(self, query, context_text):
        if context_text is None:
            context_text = ""
            
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

        # FALLBACK - use knowledge-base extraction
        return self._extract_from_context(query, context_text)

    # -------------------------------------
    # FALLBACK ANALYTICS EXTRACTION
    # -------------------------------------
    def _extract_from_context(self, query, context_text):
        q = query.lower()
        ctx = context_text
        
        relevant_sections = []

        def extract_section(title, next_titles):
            try:
                start = ctx.find(title)
                if start == -1:
                    return None
                
                # Search for the *nearest* next title from the list of possible next titles
                end = len(ctx)
                start_search_pos = start + len(title)
                
                for next_title in next_titles:
                   next_pos = ctx.find(next_title, start_search_pos)
                   if next_pos != -1 and next_pos < end:
                       end = next_pos
                
                return ctx[start:end].strip()
            except Exception as e:
                print(f"Extraction error: {e}")
                return None

        # Define known section headers
        HEADERS = [
            "=== ANALYTICS SUMMARY ===",
            "=== DISEASE TRENDS ===",
            "=== DOCTOR WORKLOAD ===",
            "=== GEOGRAPHIC DISTRIBUTION ==="
        ]

        # 1. SUMMARY
        if any(w in q for w in ["summary", "overview", "total", "stats"]):
            sec = extract_section("=== ANALYTICS SUMMARY ===", HEADERS)
            if sec:
                relevant_sections.append(f"**Executive Summary**\n{sec}")

        # 2. DISEASE
        if any(w in q for w in ["disease", "illness", "common", "prevalent", "top", "trend"]):
            sec = extract_section("=== DISEASE TRENDS ===", HEADERS)
            if sec:
                relevant_sections.append(f"**Disease Analysis**\n{sec}")

        # 3. DOCTOR
        if any(w in q for w in ["doctor", "staff", "workload", "busy", "visit", "schedule"]):
            sec = extract_section("=== DOCTOR WORKLOAD ===", HEADERS)
            if sec:
                relevant_sections.append(f"**Staff Performance**\n{sec}")
        
        # 4. BRANCH / AREA
        if any(w in q for w in ["branch", "area", "location", "city", "geographic"]):
            sec = extract_section("=== GEOGRAPHIC DISTRIBUTION ===", HEADERS)
            if sec:
                relevant_sections.append(f"**Geographic Reach**\n{sec}")

        # If we found relevant sections, join them
        if relevant_sections:
            return "\n\n---\n\n".join(relevant_sections) + "\n\n---\n*Extracted from Analytics Knowledge Base*"

        # DEFAULT FALLBACK: If nothing specific matched, show Summary + Key Insights
        # or if the query is very generic like "explain graphs"
        if "graph" in q or "chart" in q or "data" in q:
             summary = extract_section("=== ANALYTICS SUMMARY ===", HEADERS)
             trends = extract_section("=== DISEASE TRENDS ===", HEADERS)
             if summary and trends:
                 return f"**Overview**\n{summary}\n\n**Trends**\n{trends}\n\n---\n*Extracted from Analytics Knowledge Base*"

        # Ultimate fallback
        summary = extract_section("=== ANALYTICS SUMMARY ===", HEADERS)
        return f"""
**Analytics Information**

I couldn't match your question to a specific category, but here is the general summary of our data:

{summary or "Data not available."}

Try asking about:
- Disease trends
- Doctor workload
- Branch comparison
"""

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
    print(llm.generate_answer("explain me disease treands", context))
