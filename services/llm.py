import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
load_dotenv()

# Setup - usually you'd put this in a .env file
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")
async def extract_receipt(ocr_text: str) -> dict:
    prompt = f"""
    Extract the following details from this receipt OCR text:
    - store_name: Name of business
    - total (as a float)
    - date: The date of the transaction (Format: YYYY-MM-DD if possible)
    - tax
    - items (list of objects with 'name' and 'price')
    
    OCR TEXT:
    {ocr_text}
    """
    
    # Generate content with JSON constraint
    response = model.generate_content(
        prompt,
        generation_config={
            "response_mime_type": "application/json"
        }
    )
    
    # Convert the string response back into a Python dict for your pipeline
    return json.loads(response.text)
