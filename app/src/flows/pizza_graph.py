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

    return {"messages": [response]}

# defining activity node


def pizza_agent(state: PizzaState):
    pizza_toppings = state["entities"].get("topping", None)
    pizza_size = state["entities"].get("size", None)
    pizza_sauce = state["entities"].get("sauce", None)
    pizza_base = state["entities"].get("base", None)

    print(f"pizza_toppings: {pizza_toppings}")
    print(f"pizza_size: {pizza_size}")
    print(f"pizza_sauce: {pizza_sauce}")
    print(f"pizza_base: {pizza_base}")

    sys_msg = f"""If the user expresses love for pizza, ask them questions about the kind of pizza they want.
    
    If they express hate pizza, let them know that you love pizza and say goodbye.
    
    Keep asking questions until the pizza state is complete.
    
    Current Pizza State:
    Toppings: {pizza_toppings}
    Size: {pizza_size}
    Sauce: {pizza_sauce}
    Base: {pizza_base}
    """

    print(f"pizza_agent called with state: {state}")

    return _execute_agent(state, sys_msg)
