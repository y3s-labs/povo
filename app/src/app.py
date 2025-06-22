from .services.classifier import Classifier
from .state import State
from .services.chat_service import ChatService
from .types import Session, User

# from flows.booking import build_booking_graph
# from flows.feedback import build_feedback_graph
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field


class App:
    def __init__(self):
        def classify_intent(state: State):
            last_message = state["messages"][-1]
            intent = Classifier().classify(last_message.content)
            print(f"intent: {intent}")
            return {"intent": intent.intent}

        def router(state: State):
            intent = state.get("intent", "fallback")
            if intent == "logical":
                return {"next": "logical"}
            elif intent == "emotional":
                return {"next": "therapist"}
            else:
                return {"next": END}

        def chatbot(state: State):
            response = ChatService().respond(state["messages"])
            print(f"llm response: {response}")
            return {"messages": [response]}

        app_graph = StateGraph(State)
        app_graph.add_node("classify_intent", classify_intent)
        app_graph.add_node("router", router)
        app_graph.add_node("chatbot", chatbot)
        app_graph.add_edge(start_key=START, end_key="classify_intent")
        app_graph.add_edge(start_key="classify_intent", end_key="router")
        app_graph.add_edge(start_key="router", end_key="chatbot")
        app_graph.add_edge(start_key="chatbot", end_key=END)

        self.graph = app_graph.compile()

    def run(self, user_input: str, session: Session, user: User, next: str | None = None):
        initial_state = {
            "messages": [{"role": "user", "content": user_input}],
            "next": next,
            "session": session,
            "user": user
        }
        return self.graph.invoke(initial_state)
