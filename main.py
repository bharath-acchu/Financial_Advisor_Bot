import os
from dotenv import load_dotenv
from agent.graph import build_graph
from llm.gemini import gemini_llm

load_dotenv()

def main():
    graph = build_graph()
    while True:
        query = input("\nAsk your financial advisor: ")
        if query.lower() in ["exit", "quit"]:
            break
        result = graph.invoke({"input": query})
        print(result["output"])
    """while True:
        query = input("\nAsk your financial advisor: ")
        if query.lower() in ["exit", "quit"]:
            break
        print(gemini_llm(query))"""

if __name__ == "__main__":
    main()
