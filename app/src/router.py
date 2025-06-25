from .state import State
from langgraph.graph import StateGraph, START, END


def router(state: State):
    intent = state.get("intent", "fallback")
    if intent == "love":
        return {"next": "logical"}
    elif intent == "hate":
        return {"next": "therapist"}
    else:
        return {"next": END}
