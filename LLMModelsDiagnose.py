import os
import sys
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

def diagnose_llm():
    print("="*50)
    print("🏥 SAYLANI MED BOT DIAGNOSTICS")
    print("="*50)

    # 1. Check API Key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY not found!")
        print("   -> In local dev: Make sure you have a .env file with GEMINI_API_KEY=AIza...")
        print("   -> In Streamlit Cloud: Add it to 'Secrets' in the dashboard settings.")
        print("   -> Result: faster but 'dumber' fallback mode will be used (Rule-based extraction).")
    else:
        print("✅ API Key found: " + api_key[:5] + "..." + api_key[-4:])
        
        # 2. Check Google Generative AI Library
        try:
            import google.generativeai as genai
            print("✅ google-generativeai library installed.")
            
            # 3. Test Connection
            print("\n🔄 Testing connection to Gemini API...")
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash") # Using a standard stable model
            try:
                response = model.generate_content("Say 'Hello, I am working!' at the start of your sentence.")
                print("✅ CONNECTION SUCCESSFUL!")
                print(f"🤖 AI Reponse: {response.text.strip()}")
            except Exception as e:
                print(f"❌ Connection Failed: {e}")
                print("   -> Your API Key might be invalid or quota exceeded.")
        except ImportError:
            print("❌ 'google-generativeai' library missing.")
            print("   -> Run: pip install google-generativeai")

    print("\n" + "="*50)
    print("🧠 ALL LOGIC TEST")
    print("="*50)
    
    try:
        from src.llm import LLMGenerator
        llm = LLMGenerator()
        
        dummy_context = """
=== ANALYTICS SUMMARY ===
Total Patients: 500
=== DISEASE TRENDS ===
Most common: Fever (50 cases)
"""
        print("Testing Generator with dummy data...")
        answer = llm.generate_answer("What is the common disease?", dummy_context)
        print("\n📝 FINAL ANSWER OUTPUT:")
        print("-" * 20)
        print(answer)
        print("-" * 20)
        
        if "Extracted from" in answer and api_key:
             print("\n⚠️ NOTICE: The system fell back to Extraction Mode despite having a key.")
             print("   This might mean the API call timed out or failed silently.")
        elif "Extracted from" in answer:
             print("\nℹ️ MODE: Extraction Mode (Expected since no API key is active)")
        else:
             print("\n✅ MODE: Full AI Generation (Perfect!)")
             
    except Exception as e:
        print(f"❌ LOGIC CRASHED: {e}")

if __name__ == "__main__":
    diagnose_llm()
