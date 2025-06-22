import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv


load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    print("Please set the OPENAI_API_KEY environment variable.")
    os._exit(1)

llm = init_chat_model(
    "gpt-3.5-turbo",
)
