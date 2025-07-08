"""
Test the new intent router system.
"""
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.router import intent_router, get_flow_for_intent
from src.intent_config import print_routing_summary, get_intents_for_flow


def test_router():
    """Test the router functionality."""
    print("Testing Intent Router System")
    print("=" * 40)
    
    # Test some intents
    test_intents = [
        "love",
        "pizza_order", 
        "general_chat",
        "reservation",
        "unknown_intent"
    ]
    
    for intent in test_intents:
        flow = get_flow_for_intent(intent)
        print(f"Intent: '{intent}' -> Flow: '{flow}'")
    
    print("\n")
    print_routing_summary()
    
    print("\nTesting specific flow intents:")
    pizza_intents = get_intents_for_flow("pizza")
    print(f"Pizza flow handles: {pizza_intents}")
    
    general_intents = get_intents_for_flow("general")  
    print(f"General flow handles: {general_intents}")


if __name__ == "__main__":
    test_router()
