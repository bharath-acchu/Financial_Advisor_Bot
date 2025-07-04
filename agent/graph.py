from langgraph.graph import StateGraph, END
from agent.tools import get_stock_price, calculate_budget, suggest_investment_plan
from agent.intentClassifier import detect_intent
from llm.gemini import gemini_llm
from typing import TypedDict

#define state schema
class AdvisorState(TypedDict):
    input: str
    output:str

# Tool wrappers for each node
def handle_stock(state):
    query = state["input"]
    return {"output": get_stock_price(query)}

def handle_budget(state:AdvisorState):
    query = state["input"]
    # Example: "income=5000, expenses=rent:2000, food:1000"
    try:
        parts = query.split("expenses=")
        income = float(parts[0].split("income=")[-1].strip().rstrip(","))
        expenses_raw = parts[1]
        expense_pairs = [e.strip().split(":") for e in expenses_raw.split(",")]
        expenses = {k: float(v) for k, v in expense_pairs}
    except:
        return {"output": "Couldn't parse income/expenses. Format: income=5000, expenses=rent:2000, food:1000"}
    return {"output": calculate_budget(income, expenses)}

def handle_advice(state:AdvisorState):
    query = state["input"]
    risk = "medium"
    if "low" in query:
        risk = "low"
    elif "high" in query:
        risk = "high"
    return {"output": suggest_investment_plan(risk)}

# Intent detection node
def detect_intent_node(state:AdvisorState):
    user_input = state["input"]
    intent = detect_intent(user_input)
    return {"input": state["input"], "output": intent} # stock / budget / advice

def build_graph():
    builder = StateGraph(AdvisorState)
    
    # Add intent routing node
    builder.add_node("detect_intent", detect_intent_node)
    builder.set_entry_point("detect_intent")

    # Add branches
    builder.add_node("stock", handle_stock)
    builder.add_node("budget", handle_budget)
    builder.add_node("advice", handle_advice)

    # Branching logic
    builder.add_conditional_edges(
        "detect_intent", 
        lambda state: state["output"],  # read the intent set by previous node  
        {
        "stock": "stock",
        "budget": "budget",
        "advice": "advice"
        }
        )

    # All branches go to END
    builder.add_edge("stock", END)
    builder.add_edge("budget", END)
    builder.add_edge("advice", END)

    return builder.compile()
