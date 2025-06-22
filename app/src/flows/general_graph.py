from langchain.chat_models import ChatOpenAI
from src.services.chat_service import llm


def chatbot(state):
    response = llm.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}
