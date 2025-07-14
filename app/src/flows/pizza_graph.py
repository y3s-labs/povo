from operator import add
from ..utils.entity_utils import extract_entity_map
from langgraph.graph import StateGraph, END

from ..services.chat_service import ChatService
from ..state import State
from ..utils.session_utils import update_session_data


class PizzaState(State):
    """State for the pizza graph flow."""
    pizza: dict = {}


def _intent_handler(state: PizzaState):

    print(f"Handling intent for pizza state: {state}")

    intent = state.get("intent")
    if intent == "confirm_order":
        return _place_order(state)
    elif intent == "love":
        return _fill_order(state)
    elif intent == "hate":
        return _hate_pizza(state)
    else:  # return to general flow
        return _fill_order(state)


def _place_order(state: PizzaState):
    """Handle the case where the user wants to place an order."""
    pizza = state.get("pizza", {})
    order_status = _validate_order(pizza)

    if order_status == "Complete":
        context = "The user has provided a complete pizza order. Confirm the order and thank them."
        sys_msg = f"""{context}
        
        Current Pizza Order:
        Base: {pizza.get("base")}
        Toppings: {pizza.get("toppings")}
        Size: {pizza.get("size")}
        Sauce: {pizza.get("sauce")}

        Confirm the order, let them know that their pizza is on the way and thank the user.
        """
    else:
        return _fill_order(state)

    return _execute_agent(state, sys_msg)


def _hate_pizza(state: PizzaState):
    """Handle the case where the user hates pizza."""
    context = "The user expressed dislike for pizza. Acknowledge their preference politely and suggest alternatives or say goodbye."
    sys_msg = f"""{context}"""

    return _execute_agent(state, sys_msg)


def _fill_order(state: PizzaState):
    """Ask the user questions until the pizza order is complete."""

    print(f"Filling order for pizza state: {state}")

    pizza = state.get("pizza", {})

    # Handle different pizza-related intents
    context = "The user expressed love for pizza. Ask them about their pizza preferences."

    sys_msg = f"""{context}
    
    Keep asking questions until you have enough information to complete the pizza order.
    
    Current Pizza State:
    Toppings: {pizza.get("toppings")}
    Size: {pizza.get("size")}
    Sauce: {pizza.get("sauce")}
    Base: {pizza.get("base")}

    If order is complete, summarize the order and ask for confirmation.
    """

    return _execute_agent(state, sys_msg)


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
    session = state["session"]

    print(f"Current session: {session}")
    session_data = session.data or {}

    print(f"Current session data: {session_data}")

    current_pizza = {}
    if session_data:
        current_pizza = session_data.get("pizza", {})

    print(f"Current pizza data: {current_pizza}")

    # Access and mutate original session data dict
    state_entities = state.get("entities", {})
    print(f"Current session entities: {state_entities}")

    new_pizza = {}
    entity_map = extract_entity_map(state_entities)

    print(f"Current entity map: {entity_map}")
    if entity_map:
        # Extract pizza-related entities from the state
        new_pizza = {
            "base": entity_map.get("BASE_TYPE"),
            "toppings": entity_map.get("TOPPING_TYPE"),
            "size": entity_map.get("SIZE_TYPE"),
            "sauce": entity_map.get("SAUCE_TYPE"),
        }

    print(f"New pizza data: {new_pizza}")

    pizza = _merge_pizza(current_pizza, new_pizza)

    state["pizza"] = pizza  # Update state with merged pizza data

    return _intent_handler(state)


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
