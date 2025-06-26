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
    sys_msg = """If the user expresses love for pizza, ask them about their favorite topppings. 
    
    If they express hate pizza, let them know that they probably have no friends and say goodbye."""

    print(f"pizza_agent called with state: {state}")

    return _execute_agent(state, sys_msg)
