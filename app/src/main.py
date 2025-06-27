import copy
from .services.classifier import Classifier
from .router import router
from .state import State
from .services.chat_service import ChatService
from .types import Session, User

# from flows.booking import build_booking_graph
# from flows.feedback import build_feedback_graph
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

from .flows.pizza_graph import pizza_agent
from .flows.general_graph import general_agent


class App:
    def __init__(self):
        """Initialize the App with LangGraph components."""
        def classify_intent(state: State):
            """Classify the intent of the user message."""
            last_message = state["messages"][-1]
            intent = Classifier().classify(last_message.content)
            print(f"intent: {intent}")
            return {"intent": intent.intent, "entities": intent.entities}

        # def chatbot(state: State):
        #     """Generate a response using the chat service."""
        #     response = ChatService().respond(state["messages"])
        #     print(f"llm response: {response}")
        #     return {"messages": [response]}

        app_graph = StateGraph(State)

        app_graph.add_node("classify_intent", classify_intent)
        app_graph.add_node("router", router)
        app_graph.add_node("chatbot", general_agent)
        app_graph.add_node("pizza_agent", pizza_agent)

        app_graph.add_edge(start_key=START, end_key="classify_intent")
        # app_graph.add_edge(start_key="classify_intent", end_key="router")

        # Conditional edges based on intent classification
        app_graph.add_conditional_edges("classify_intent", router, {
            "pizza": "pizza_agent",
            "general": "chatbot"
        })
        # app_graph.add_edge(start_key="router", end_key="pizza_agent")

        app_graph.add_edge(start_key="pizza_agent", end_key=END)
        # app_graph.add_edge(start_key="chatbot", end_key=END)

        self.graph = app_graph.compile()

    def run(self, user_input: str, session: Session, user: User, next: str | None = None):
        initial_state = {
            "messages": [{"role": "user", "content": user_input}],
            "next": next,
            "session": session,
            "session_data": copy.deepcopy(session.data),
            "user": user,
            "user_data": copy.deepcopy(user.data),
        }
        return self.graph.invoke(initial_state)
