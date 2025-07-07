from .state import State
from langgraph.graph import StateGraph, START, END


def router(state: State):
    intent = state.get("intent", "fallback")
    print(f"Routing based on state: {state}")
    if intent == "love":
        return "pizza"
    elif intent == "hate":
        return "pizza"
    else:
        return "general"
