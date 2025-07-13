from operator import add
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
        "session": update_session_data(state, "pizza")
    }


def pizza_agent(state: PizzaState):
    """Handle pizza-related intents and pizza ordering process."""

    print(f"pizza_agent called pizza state: {state}")

    # Ensure we work with a copy of the pizza state
    session_data = dict(state["session"]).get("data", {})

    current_pizza = {}
    if session_data is not {}:
        current_pizza = session_data.get("pizza", {})

    # Access and mutate original session data dict
    new_pizza = {
        "base": state["entities"].get("BASE_TYPE"),
        "toppings": state["entities"].get("TOPPING_TYPE"),
        "size": state["entities"].get("SIZE_TYPE"),
        "sauce": state["entities"].get("SAUCE_TYPE"),
    }

    pizza = _merge_pizza(current_pizza, new_pizza)

    intent = state.get("intent")
    state["pizza"] = pizza  # Update state with merged pizza data

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

    If order is complete, summarize the order and ask for confirmation.
    """

    if _validate_order(pizza) == "Complete":
        return _execute_agent(state, sys_msg)
    else:
        return placeOrder(pizza)


def _validate_order(pizza: dict) -> str:
    """Validate the pizza order to ensure all fields have valid entries."""
    required_fields = ["base", "toppings", "size", "sauce"]
    missing_fields = [
        field for field in required_fields if not pizza.get(field)]

    if missing_fields:
        return "Incomplete"

    return "Complete"


def _merge_pizza(current_pizza, new_pizza):
    """Merge the current pizza with the new pizza data."""
    print("Merging pizza data...", new_pizza, current_pizza)
    # Merge: only update missing or None values
    for key, value in dict(new_pizza).items():
        if value is not None:
            current_pizza[key] = value

    print("Merged pizza data:", current_pizza)
    return current_pizza
