import copy
from .services.classifier import Classifier
from .router import router
from .state import State
from .services.chat_service import ChatService
from .types import Session, User
from .intent_config import configure_intent_routing, print_routing_summary, get_available_flows

# Import all available flow agents
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

from .flows.pizza_graph import pizza_agent
from .flows.general_graph import general_agent
from .flows.booking_graph import booking_agent


class App:
    def __init__(self):
        """Initialize the App with LangGraph components."""
        # Ensure intent routing is configured
        configure_intent_routing()

        def classify_intent(state: State):
            """Classify the intent of the user message."""
            last_message = state["messages"][-1]
            intent = Classifier().classify(last_message.content)
            print(f"intent: {intent}")
            return {"intent": intent.intent, "entities": intent.entities}

        app_graph = StateGraph(State)

        # Add the classification and routing nodes
        app_graph.add_node("classify_intent", classify_intent)
        app_graph.add_node("router", router)

        # Add all available flow agents
        app_graph.add_node("general_agent", general_agent)
        app_graph.add_node("pizza_agent", pizza_agent)
        app_graph.add_node("booking_agent", booking_agent)

        # Set up the graph flow
        app_graph.add_edge(start_key=START, end_key="classify_intent")

        # Get all available flows and create dynamic conditional edges
        available_flows = get_available_flows()
        print("******** Available Flows:", available_flows)
        flow_mapping = {}

        for flow in available_flows:
            flow_mapping[flow] = f"{flow}_agent"
            # Add edge from each agent to END
            app_graph.add_edge(start_key=f"{flow}_agent", end_key=END)

        print("******Flow Mapping:", flow_mapping)

        # Add conditional edges based on intent classification with dynamic flow mapping
        app_graph.add_conditional_edges(
            "classify_intent", router, flow_mapping)

        self.graph = app_graph.compile()

        # Print routing summary for debugging
        print_routing_summary()

    def run(self, user_input: str, session: Session, user: User):
        initial_state = {
            "messages": [{"role": "user", "content": user_input}],
            "session": session,
            "session_data": copy.deepcopy(session.data),
            "user": user,
            "user_data": copy.deepcopy(user.data),
        }
        return self.graph.invoke(initial_state)

    def debug_routing(self):
        """Print routing information for debugging purposes."""
        print_routing_summary()
