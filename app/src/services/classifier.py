import json
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel


class NLUResponse(BaseModel):
    intent: str
    entities: dict


class Classifier:
    def __init__(self, model_name: str = "gpt-4o", temperature: float = 0):
        load_dotenv()
        # if not os.environ.get("OPENAI_API_KEY"):
        #     raise RuntimeError("OPENAI_API_KEY not found in environment.")
        if not os.environ.get("GOOGLE_API_KEY"):
            raise RuntimeError("GOOGLE_API_KEY not found in environment.")

        # self.model = ChatOpenAI(model=model_name, temperature=temperature)
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            # other params...
        )

        self.intent_data = self._load_model()
        self.parser = PydanticOutputParser(pydantic_object=NLUResponse)

        # Set static system prompt
        self.system_prompt = self._build_system_prompt()

    def _load_model(self) -> dict:
        base_path = Path(__file__).resolve().parent.parent
        path = base_path / "model" / "en.json"
        with open(path, "r") as f:
            return json.load(f)

    def _build_system_prompt(self) -> str:
        prompt = "You are an intent classification and entity extraction model.\n\n"
        prompt += "Classify the user input into one of these intents and associated entities. If no matching intent is found in list, return 'fallback' as intent:\n"

        if "intents" in self.intent_data:
            for intent, data in self.intent_data["intents"].items():
                phrases = ", ".join(data.get("phrases", []))
                prompt += f'Intent Name: {intent} (e.g., {phrases})\n'

                for key, entity_info in data.get("entities", {}).items():
                    entity_type = entity_info.get("type", "string")
                    prompt += f"Entity name: {key}, Entity type: {entity_type}\n"
        else:
            prompt += "No predefined intents.\n"

        if "entityTypes" in self.intent_data:
            prompt += "\n\nEntity types and values:\n"
            for entity, data in self.intent_data["entityTypes"].items():
                values = ", ".join(data.get("values", []))
                prompt += f"Entity Type: {entity} (e.g., {values})\n"

        prompt += (
            "\n\nExtract entities if mentioned and respond ONLY with JSON:\n"
            '{\n  "intent": "IntentName",\n  "entities": { "entityType": "entityValue" }\n}'
            "\n\nRespond strictly in valid JSON format."
        )
        return prompt

    def classify(self, user_message: str) -> NLUResponse:
        # print(f"classify user message: {self.system_prompt}")
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"User message to classify: {user_message}")
        ]
        output = self.model.invoke(messages)

        return self.parser.invoke(output.content)
