from nodes.newsstate import NewsState
from langgraph.types import Command,interrupt

# Decision node for interrupt
def approve_decision(state: NewsState) -> NewsState:
    response = interrupt(f"Do you approve this script?")
    if response in ["yes", "approve", "approved"]:
        state['script_approved'] = "yes"
    else:
        state['script_approved'] = "no"
    return state

def final_decision(state: NewsState)->str:
    # Final decision based on script approval
    if state.get('script_approved') == "yes":
        return "get_metadata"
    return "scrape_and_return"