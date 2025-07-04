import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()  # Load GEMINI_API_KEY from .env

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

def gemini_llm(user_input: str) -> str:
    print("🔮 Inside Gemini LLM call")

    prompt = f"""
Classify the user's intent from the following types:
- "stock" (if asking about stock or crypto prices)
- "budget" (if calculating income/expenses/savings)
- "advice" (if asking for investment suggestions)

Respond with only one word: stock, budget, or advice.

User input: "{user_input}"
"""
    try:
        response = model.generate_content(prompt)
        intent = response.text.strip().lower()
        print(f"✅ Detected intent: {intent}")
        return intent
    except Exception as e:
        print("❌ Gemini API error:", e)
        return "unknown"
