# Intent Router System

This document explains how to use the new registry-based intent router system that replaces complex if-else logic with a clean, extensible approach.

## Overview

The intent router system provides:
- **Registry-based routing**: No more if-else chains
- **Easy extensibility**: Add new intents and flows without touching core router logic
- **Centralized configuration**: Manage all routing rules in one place
- **Dynamic management**: Add/remove intents at runtime
- **Debugging utilities**: Inspect routing configuration easily

## Core Components

### 1. IntentRouter Class (`router.py`)
The main router class that manages intent-to-flow mappings:

```python
from src.router import intent_router

# Register a single intent
intent_router.register_intent("pizza_craving", "pizza")

# Register multiple intents
intent_router.register_intents({
    "weather_forecast": "weather",
    "news_update": "news"
})

# Route an intent
flow = intent_router.route("pizza_order")  # Returns "pizza"
```

### 2. Intent Configuration (`intent_config.py`)
Centralized configuration file where all routing rules are defined:

```python
# Add pizza-related intents
add_pizza_intents("pizza_order", "italian_food", "cheese_craving")

# Add general conversation intents  
add_general_intents("greeting", "goodbye", "help")

# Add custom flow intents
add_custom_flow_intents("booking", "reservation", "table_booking")
```

### 3. Flow Graphs
Each flow handles specific types of intents:
- `pizza_graph.py`: Handles pizza-related intents
- `general_graph.py`: Handles general conversation
- `booking_graph.py`: Handles reservation intents (example)

## Adding a New Flow

### Step 1: Create the Flow Graph
Create a new file `app/src/flows/your_flow_graph.py`:

```python
from ..services.chat_service import ChatService
from ..state import State

class YourFlowState(State):
    """State for your custom flow."""
    # Add flow-specific state fields
    pass

def your_flow_agent(state: YourFlowState):
    """Handle intents for your flow."""
    intent = state.get("intent", None)
    
    # Handle different intents within your flow
    sys_msg = f"Handle {intent} intent appropriately..."
    
    response = ChatService(system_prompt=sys_msg).respond(state["messages"])
    state["currentFlow"] = "your_flow"
    
    return {"messages": [response]}
```

### Step 2: Register Intents
Add your intents to `intent_config.py`:

```python
def configure_intent_routing():
    # ... existing code ...
    
    # Add your custom flow intents
    add_custom_flow_intents(
        "your_flow",
        "intent1",
        "intent2", 
        "intent3"
    )
```

### Step 3: Add to Main Graph
Update `main.py` to include your flow:

```python
# Add your flow node
app_graph.add_node("your_flow_agent", your_flow_agent)

# Add to conditional edges
app_graph.add_conditional_edges("classify_intent", router, {
    "pizza": "pizza_agent",
    "general": "general_agent",
    "your_flow": "your_flow_agent"  # Add this line
})

# Add edge to END
app_graph.add_edge(start_key="your_flow_agent", end_key=END)
```

## Usage Examples

### Basic Routing
```python
from src.router import router
from src.state import State

state = {"intent": "pizza_order", "messages": [...]}
flow = router(state)  # Returns "pizza"
```

### Dynamic Intent Management
```python
from src.router import add_pizza_intents, remove_intent

# Add new pizza intents at runtime
add_pizza_intents("pizza_special", "deep_dish")

# Remove an intent
remove_intent("old_intent")

# Check where an intent routes
flow = get_flow_for_intent("pizza_special")  # Returns "pizza"
```

### Debugging
```python
from src.intent_config import print_routing_summary
from src.main import App

# Print all routing rules
print_routing_summary()

# Use app debug method
app = App()
app.debug_routing()
```

## Benefits

1. **No More If-Else Chains**: Replace complex conditional logic with simple registry lookups
2. **Easy to Extend**: Add new intents by just calling a function
3. **Centralized Management**: All routing rules in one configuration file
4. **Runtime Flexibility**: Modify routing behavior without restarting
5. **Better Testing**: Each flow can be tested independently
6. **Clear Separation**: Each flow focuses on its specific domain

## Testing

Run the router tests:
```bash
cd app
python tests/test_router.py
```

This will show you how intents are routed to different flows and print a summary of all routing rules.
