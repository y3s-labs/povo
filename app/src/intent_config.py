"""
Intent configuration for the router system.

This file centralizes all intent-to-flow mappings, making it easy to manage
and modify routing behavior without touching the core router logic.
"""

from .router import intent_router, add_pizza_intents, add_general_intents, add_custom_flow_intents


def configure_intent_routing():
    """Configure all intent routing rules."""

    # Pizza-related intents
    add_pizza_intents(
        "love",
        "hate",
        "pizza_order",
        "pizza_craving",
        "food_order",
        "italian_food",
        "cheese_craving",
        "pizza_delivery",
        "pizza_menu",
        "pizza_special"
    )

    # General conversation intents
    add_general_intents(
        "general_chat",
        "emotional_support",
        "wellbeing",
        "greeting",
        "goodbye",
        "help",
        "thanks",
        "small_talk",
        "mood_check"
    )

    # Booking/reservation intents (if you implement the booking flow)
    add_custom_flow_intents(
        "booking",
        "reservation",
        "table_booking",
        "restaurant_booking",
        "make_reservation",
        "book_table",
        "dining_reservation"
    )

    # You can easily add more flows here:
    # add_custom_flow_intents("weather", "weather_forecast", "temperature", "rain")
    # add_custom_flow_intents("news", "latest_news", "headlines", "current_events")


def get_available_flows():
    """Get all available flows in the system."""
    return list(set(intent_router._intent_registry.values()))


def get_intents_for_flow(flow_name: str):
    """Get all intents that route to a specific flow."""
    return [intent for intent, flow in intent_router._intent_registry.items() if flow == flow_name]


def print_routing_summary():
    """Print a summary of all routing rules for debugging."""
    print("=== Intent Routing Summary ===")
    for flow in get_available_flows():
        intents = get_intents_for_flow(flow)
        print(f"{flow.upper()} Flow: {', '.join(intents)}")
    print(f"Default Flow: {intent_router._default_flow}")
    print("===============================")


# Initialize routing configuration
configure_intent_routing()
