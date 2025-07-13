from operator import add
from typing import Annotated
from langgraph.graph import StateGraph, END

from ..services.chat_service import ChatService
from ..state import State


class GeneralState(State):
    """State for the general graph flow."""
    currentFlow = "general"


def _execute_agent(state: GeneralState, sys_msg: str):
    """Execute the agent with the given state and system message."""

    response = ChatService(system_prompt=sys_msg).respond(state["messages"])

    return {"messages": [response]}

# defining activity node


def general_agent(state: GeneralState):

    sys_msg = """You are a an emotionally intelligent assistant who cares deeply about the user's emotional and physical well-being.
    
    You are given a message from a user.
    
    You need to respond to the user in a way that is emotionally intelligent and helpful.
    
    You will continue to engage with the user by asking them questions.
    
    You need to respond in a way that is helpful and engaging.
    """

    print(f"general_agent called with state: {state}")

    state["currentFlow"] = "general"

    return _execute_agent(state, sys_msg)
