from .state import State


def router(state: State):
    intent = state.get("intent", "fallback")
    if intent == "logical":
        return {"next": "logical"}
    elif intent == "emotional":
        return {"next": "therapist"}
    else:
        return {"next": END}
