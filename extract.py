import os
import json
from google import genai
from google.genai import types

# 1. Initialize the Gemini Client
# (It automatically looks for the GEMINI_API_KEY environment variable)
client = genai.Client()

def extract_opportunities(chat_text):
    print("🧠 Analyzing chat log with Gemini AI...")
    
    prompt = f"""
    You are an expert networking and business intelligence assistant.
    Analyze the following chat transcript and extract all people mentioned, 
    along with any professional opportunities, projects, or help they need.

    Format the output as a strict JSON object with a single key "data" containing a list of objects.
    Each object must have:
    - "name": Name of the person
    - "role_company": Their role or company (if known, else "Unknown")
    - "opportunity": What they are looking for, offering, or working on
    - "contact_info": Any handles or email mentioned (else "None")

    Chat Transcript:
    \"\"\"
    {chat_text}
    \"\"\"
    """

    # Using gemini-3.5-flash (Google's blindingly fast, free-tier model)
    response = client.models.generate_content(
        model='gemini-3.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"  # Forces Gemini to return valid JSON
        ),
    )
    
    return response.text

# 2. Test Data
sample_chat = """
[10:00 AM] Alex (DevOps @ TechCorp): Hey everyone! We are looking for a freelance React dev to help us redesign our frontend landing page. HMU if interested or email alex@techcorp.io.
[10:15 AM] Sarah Jenkins: Just joined! I'm an AI researcher working on a new LLM wrapper for productivity. Looking for co-founders.
[10:32 AM] David: Anyone know a good mobile dev? I have a client looking to build an iOS app.
"""

# 3. Execution
if __name__ == "__main__":
    try:
        raw_result = extract_opportunities(sample_chat)
        
        # Pretty print the JSON output
        parsed_json = json.loads(raw_result)
        print("\n🔥 SUCCESS! EXTRACTED THREADMAP DATA:")
        print(json.dumps(parsed_json, indent=4))
        
    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}")