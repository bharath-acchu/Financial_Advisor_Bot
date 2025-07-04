from llm.gemini import gemini_llm

def detect_intent(user_input: str) -> str:
    prompt = f"""
Classify the user's intent from the following types:
- "stock" (if asking about stock or crypto prices)
- "budget" (if calculating income/expenses/savings)
- "advice" (if asking for investment suggestions)

Respond with only one word: stock, budget, or advice.

User input: "{user_input}"
"""
    return gemini_llm(prompt).lower()
