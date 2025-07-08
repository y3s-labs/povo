from operator import add
from typing import Annotated
from langgraph.graph import StateGraph, END

from ..services.chat_service import ChatService
from ..state import State


class BookingState(State):
    """State for the booking graph flow."""
    restaurant_name: str = None
    date: str = None
    time: str = None
    party_size: int = None


def _execute_agent(state: BookingState, sys_msg: str):
    """Execute the agent with the given state and system message."""

    response = ChatService(system_prompt=sys_msg).respond(state["messages"])

    # Store current flow in the state
    state["currentFlow"] = "booking"

    return {"messages": [response]}


def booking_agent(state: BookingState):
    """Handle booking-related intents and reservation process."""
    restaurant = state["entities"].get("restaurant", None)
    date = state["entities"].get("date", None)
    time = state["entities"].get("time", None)
    party_size = state["entities"].get("party_size", None)
    intent = state.get("intent", None)

    print(f"booking_agent called with intent: {intent}")
    print(f"restaurant: {restaurant}")
    print(f"date: {date}")
    print(f"time: {time}")
    print(f"party_size: {party_size}")

    sys_msg = f"""You are helping the user make a restaurant reservation.
    
    Collect the following information if not already provided:
    - Restaurant name or type of cuisine
    - Date for the reservation
    - Time preference
    - Number of people (party size)
    
    Current Booking State:
    Restaurant: {restaurant}
    Date: {date}
    Time: {time}
    Party Size: {party_size}
    
    Once all information is collected, confirm the reservation details with the user.
    Be helpful and suggest alternatives if their preferred time/date is not available.
    """

    print(f"booking_agent called with state: {state}")

    return _execute_agent(state, sys_msg)
