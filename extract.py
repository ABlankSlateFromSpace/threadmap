import os
import json
from google import genai
from google.genai import types

# 1. Initialize the Gemini Client
# (It automatically looks for the GEMINI_API_KEY environment variable)
client = genai.Client()

def extract_opportunities(chat_text):
    """Sends the chat text to Gemini and gets structured JSON back."""
    print("🧠 Analyzing chat log with Gemini AI...")
    
    prompt = f"""
    You are an expert data extraction AI. Analyze the following chat log and extract any business opportunities, freelance gigs, hiring needs, or partnership requests.
    
    Return the data strictly in this JSON format:
    {{
        "data": [
            {{
                "name": "Person's name",
                "role_company": "Their role or company if mentioned, otherwise 'Unknown'",
                "opportunity": "Clear summary of what they are looking for or offering",
                "contact_info": "Email, handle, or contact details mentioned, otherwise 'None'"
            }}
        ]
    }}
    
    Raw Chat Log:
    {chat_text} 
    """
    # ^ Make sure it says {chat_text} right there at the bottom of the prompt!

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        ),
    )
    return response.text

# 2. Test Data
sample_chat = """[1:00 PM] Elon: Looking for a rocket engineer to help build an engine for Mars. Hit me up at elon@spacex.com."""

# 3. Execution
if __name__ == "__main__":
    try:
        # --- NEW CODE: READ FROM THE REAL TEXT FILE ---
        input_filename = "chat_log.txt"
        
        print(f"📂 Reading raw chat logs from '{input_filename}'...")
        with open(input_filename, "r", encoding="utf-8") as file:
            real_chat_data = file.read()
            
        # Pass the file contents to Gemini
        raw_result = extract_opportunities(real_chat_data)
        parsed_json = json.loads(raw_result)
        
        print("\n🔥 SUCCESS! EXTRACTED THREADMAP DATA:")
        print(json.dumps(parsed_json, indent=4))
        
        # Save the results
        output_filename = "results.json"
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(parsed_json, f, indent=4)
            
        print(f"\n💾 Data successfully saved to your project folder as '{output_filename}'!")
        
    except FileNotFoundError:
        print("\n❌ Error: Could not find 'chat_log.txt'. Make sure you created it!")
    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}")