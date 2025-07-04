import yfinance as yf
import pandas as pd
import re

def get_stock_price(user_input: str) -> str:
    print("📈 Inside get_stock_price")

    # Try to extract a valid symbol (assuming UPPERCASE letters and numbers, e.g., TSLA, AAPL)
    match = re.search(r"\b[A-Z]{1,5}\b", user_input.upper())

    if not match:
        return "❌ Couldn't find a valid stock symbol in your message. Try like: 'price of TSLA'."

    symbol = match.group(0)
    
    try:
        stock = yf.Ticker(symbol)
        price_data = stock.history(period="1d")
        if price_data.empty:
            return f"❌ No price data found for {symbol} (possibly delisted or invalid)."

        price = price_data["Close"].iloc[-1]
        return f"The current price of {symbol} is ${price:.2f}"
    except Exception as e:
        return f"❌ Error retrieving stock price: {str(e)}"

def calculate_budget(income: float, expenses: dict) -> str:
    total_expense = sum(expenses.values())
    savings = income - total_expense
    if(savings < 0):
        return f"Please work on your savings!!"
    else:
        return f"Your total monthly savings is ${savings:.2f}."

def suggest_investment_plan(risk_level: str) -> str:
    plans = {
        "low": "60% bonds, 30% large-cap stocks, 10% gold.",
        "medium": "40% stocks, 30% ETFs, 20% bonds, 10% crypto.",
        "high": "70% stocks, 20% crypto, 10% startups."
    }
    return plans.get(risk_level.lower(), "Please specify risk as low, medium, or high.")
