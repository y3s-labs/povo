import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY not found in environment.")


class ChatService:
    def __init__(self, model_name="gpt-4o", temperature=0.7, system_prompt=None):
        self.model_name = model_name
        self.temperature = temperature
        self.prompt = system_prompt or "You are a helpful assistant."

    def respond(self, messages):
        # Choose which system prompt to apply
        prompt_to_use = self.prompt

        # Convert messages to the format expected by ChatOpenAI
        formatted_messages = []

        # Check if there's already a system message
        has_system_message = any(isinstance(m, SystemMessage)
                                 for m in messages)

        # Add system message if not present
        if not has_system_message:
            formatted_messages.append(SystemMessage(content=prompt_to_use))

        # Add all other messages
        for message in messages:
            if isinstance(message, (HumanMessage, AIMessage, SystemMessage)):
                formatted_messages.append(message)
            elif isinstance(message, dict):
                # Handle dictionary format as fallback
                if message.get("role") == "system":
                    formatted_messages.append(
                        SystemMessage(content=message["content"]))
                elif message.get("role") == "user":
                    formatted_messages.append(
                        HumanMessage(content=message["content"]))
                elif message.get("role") == "assistant":
                    formatted_messages.append(
                        AIMessage(content=message["content"]))

        llm = ChatOpenAI(
            model=self.model_name,
            temperature=self.temperature
        )

        return llm.invoke(formatted_messages)
