from operator import add
from typing import Annotated
from langgraph.graph import StateGraph, END

from ..services.chat_service import ChatService
from ..state import State
from ..utils.session_utils import update_session_data


class PizzaState(State):
    """State for the pizza graph flow."""
    pizza: dict = {}


def _execute_agent(state: PizzaState, sys_msg: str):
    """Execute the agent with the given state and system message."""

    response = ChatService(system_prompt=sys_msg).respond(state["messages"])

    return {
        "messages": [response],
        "currentFlow": "pizza",
        "session": update_session_data(state, "pizza", state.get("pizza"))
    }


def pizza_agent(state: PizzaState):
    """Handle pizza-related intents and pizza ordering process."""

    # Access and mutate original session data dict
    pizza = {
        "base": state["entities"].get("BASE_TYPE"),
        "toppings": state["entities"].get("TOPPING_TYPE"),
        "size": state["entities"].get("SIZE_TYPE"),
        "sauce": state["entities"].get("SAUCE_TYPE"),
    }

    intent = state.get("intent")
    state["pizza"] = pizza  # Update the pizza state in the session
    # state["session"]["data"] = pizza

    print(f"pizza_agent called with intent: {intent} and pizza state: {pizza}")

    # Handle different pizza-related intents
    if intent == "love":
        context = "The user expressed love for pizza. Ask them about their pizza preferences."
    else:
        context = "The user expressed dislike for pizza. Acknowledge their preference politely and suggest alternatives or say goodbye."

    sys_msg = f"""{context}
    
    Keep asking questions until you have enough information to complete the pizza order.
    
    Current Pizza State:
    Toppings: {pizza.get("toppings")}
    Size: {pizza.get("size")}
    Sauce: {pizza.get("sauce")}
    Base: {pizza.get("base")}
    
    If all required information is collected, summarize the order and ask for confirmation.
    """

    return _execute_agent(state, sys_msg)
