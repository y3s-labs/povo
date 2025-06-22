from services.classifier import Classifier
from state import State
from services.llm import llm
# from flows.booking import build_booking_graph
# from flows.feedback import build_feedback_graph
from langgraph.graph import StateGraph, START, END

from langgraph.graph.message import add_messages

from pydantic import BaseModel, Field

# Build individual subgraphs
# booking_graph = build_booking_graph()
# feedback_graph = build_feedback_graph()

# Compose into main graph
app_graph = StateGraph(State)


def classify_intent(state: State):
    print(state["messages"][-1].content)
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
    return {"messages": [llm.invoke(state["messages"])]}


# Define a simple LLM function
app_graph.add_node("classify_intent", classify_intent)
app_graph.add_node("router", router)
app_graph.add_node("chatbot", chatbot)

app_graph.add_edge(start_key=START, end_key="classify_intent")
app_graph.add_edge(start_key="classify_intent", end_key="router")
app_graph.add_edge(start_key="router", end_key="chatbot")
app_graph.add_edge(start_key="chatbot", end_key=END)

graph = app_graph.compile()

user_input = input("Enter your message: ")
state = graph.invoke({"messages": [{"role": "user", "content": user_input}]})

print(state["messages"][-1].content)
print(f"{state}")

# app_graph.include_subgraph("booking", booking_graph)
# app_graph.include_subgraph("feedback", feedback_graph)

# app_graph.set_entry_point("booking/ask_booking_date")
# app_graph.set_finish_point("feedback/ask_feedback_comment")

# runnable = app_graph.compile()
# state = AppState()

# # Simulated user interaction flow
# steps = [
#     ("booking/ask_booking_date", "June 30"),
#     ("booking/ask_booking_time", "3 PM"),
#     ("booking/confirm_booking", "yes"),
#     ("feedback/ask_feedback_rating", "5"),
#     ("feedback/ask_feedback_comment", "Great service!")
# ]

# for node, user_input in steps:
#     state, next_node = runnable.invoke(node, state, user_input)
#     print(f"Next: {next_node}, State: {state.__dict__}")
