from operator import add
from typing import Annotated
from langgraph.graph import StateGraph, END

from ..services.chat_service import ChatService
from ..state import State


class PizzaState(State):
    """State for the pizza graph flow."""
    # pizza_type: str = None
    toppings: list = []
    # size: str = None
    # quantity: int = 1


def _execute_agent(state: PizzaState, sys_msg: str):
    """Execute the agent with the given state and system message."""

    response = ChatService(system_prompt=sys_msg).respond(state["messages"])

    return {"messages": [response], "currentFlow": "pizza"}

# defining activity node


def pizza_agent(state: PizzaState):
    """Handle pizza-related intents and pizza ordering process."""
    pizza_toppings = state["entities"].get("topping", None)
    pizza_size = state["entities"].get("size", None)
    pizza_sauce = state["entities"].get("sauce", None)
    pizza_base = state["entities"].get("base", None)
    intent = state.get("intent", None)

    print(f"pizza_agent called with intent: {intent}")
    print(f"pizza_toppings: {pizza_toppings}")
    print(f"pizza_size: {pizza_size}")
    print(f"pizza_sauce: {pizza_sauce}")
    print(f"pizza_base: {pizza_base}")

    # Handle different pizza-related intents
    if intent == "love":
        context = "The user expressed love for pizza. Ask them about their pizza preferences."
    elif intent == "hate":
        context = "The user expressed hate for pizza. Acknowledge their preference politely and suggest alternatives or say goodbye."
    elif intent in ["pizza_order", "pizza_craving", "food_order"]:
        context = "The user wants to order pizza or is craving pizza. Help them build their ideal pizza order."
    else:
        context = "This is a pizza-related conversation. Help the user with their pizza needs."

    sys_msg = f"""{context}
    
    Keep asking questions until you have enough information to complete the pizza order.
    
    Current Pizza State:
    Toppings: {pizza_toppings}
    Size: {pizza_size}
    Sauce: {pizza_sauce}
    Base: {pizza_base}
    
    If all required information is collected, summarize the order and ask for confirmation.
    """

    print(f"pizza_agent called with state: {state}")

    return _execute_agent(state, sys_msg)
