from .state import State
from langgraph.graph import StateGraph, START, END
from typing import Dict, List, Optional


class IntentRouter:
    """A registry-based router for handling multiple intents without complex if-else logic."""

    def __init__(self):
        self._intent_registry: Dict[str, str] = {}
        self._default_flow: str = "general"

    def register_intent(self, intent: str, flow: str) -> None:
        """Register an intent to be routed to a specific flow."""
        self._intent_registry[intent] = flow

    def register_intents(self, intent_mapping: Dict[str, str]) -> None:
        """Register multiple intents at once."""
        self._intent_registry.update(intent_mapping)

    def set_default_flow(self, flow: str) -> None:
        """Set the default flow for unrecognized intents."""
        self._default_flow = flow

    def route(self, intent: Optional[str]) -> str:
        """Route an intent to the appropriate flow."""
        if not intent:
            return self._default_flow
        return self._intent_registry.get(intent, self._default_flow)

    def get_registered_intents(self) -> List[str]:
        """Get all registered intents."""
        return list(self._intent_registry.keys())


# Create global router instance
intent_router = IntentRouter()

# Register intent mappings
intent_router.register_intents({
    "love": "pizza",
    "hate": "pizza",
    # "pizza_order": "pizza",
    # "pizza_craving": "pizza",
    # "food_order": "pizza",
    "general_chat": "general",
    "emotional_support": "general",
    "wellbeing": "general"
})


# Utility functions for dynamic intent management

def add_pizza_intents(*intents: str) -> None:
    """Add new intents that should route to the pizza flow."""
    for intent in intents:
        intent_router.register_intent(intent, "pizza")


def add_general_intents(*intents: str) -> None:
    """Add new intents that should route to the general flow."""
    for intent in intents:
        intent_router.register_intent(intent, "general")


def add_custom_flow_intents(flow_name: str, *intents: str) -> None:
    """Add new intents that should route to a custom flow."""
    for intent in intents:
        intent_router.register_intent(intent, flow_name)


def remove_intent(intent: str) -> bool:
    """Remove an intent from the router. Returns True if removed, False if not found."""
    return intent_router._intent_registry.pop(intent, None) is not None


def get_flow_for_intent(intent: str) -> str:
    """Get the flow that an intent routes to."""
    return intent_router.route(intent)


def router(state: State) -> str:
    """Route based on intent using the registry-based router."""
    intent = state.get("intent", None)
    flow = intent_router.route(intent)

    print(f"Routing intent '{intent}' to flow '{flow}'")
    print(f"Available intents: {intent_router.get_registered_intents()}")

    return flow
