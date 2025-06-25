import json
import os
from pathlib import Path
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel


class NLUResponse(BaseModel):
    intent: str
    entities: dict


class Classifier:
    def __init__(self, model: str = "gpt-4o"):
        api_key = "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"

        self.model = ChatOpenAI(
            model=model, temperature=0, api_key=api_key)
        self.intent_data = self._load_model()

        self.parser = PydanticOutputParser(pydantic_object=NLUResponse)
        self.prompt_template = PromptTemplate(
            template="{prompt}",
            input_variables=["prompt"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()}
        )

    def _load_model(self) -> dict:
        base_path = Path(__file__).resolve().parent.parent
        path = base_path / "model" / "en.json"
        with open(path, "r") as f:
            return json.load(f)

    def _build_prompt(self, message: str) -> str:
        prompt = "You are an intent classification and entity extraction model.\n\n"
        prompt += "Classify the user input into one of these intents and associated entities. If no matching intent is found in list, return 'fallback' as intent:\n"

        if "intents" in self.intent_data:
            for intent, data in self.intent_data["intents"].items():
                phrases = data.get("phrases", [])
                entities = data.get("entities", {})

                example_phrases = ", ".join(phrases) if phrases else ""
                prompt += f'Intent Name: {intent} (e.g., {example_phrases})\n'

                if entities:
                    for key, entity_info in entities.items():
                        entity_type = entity_info.get("type", "string")
                        prompt += f"Entity name: {key}, Entity type: {entity_type}\n"
        else:
            print("No intents found in model")

        prompt += "\n\n"

        if "entityTypes" in self.intent_data:
            for entity, data in self.intent_data["entityTypes"].items():
                values = data.get("values", [])
                example_values = ", ".join(values) if values else ""
                prompt += f"Entity Type: {entity} (e.g., {example_values})\n"

        prompt += (
            "\n\nExtract entities if mentioned and respond ONLY with JSON:\n"
            '{\n  "intent": "IntentName",\n  "entities": { "entityType": "entityValue" }\n}'
            "\n\nRespond strictly in valid JSON format."
        )

        prompt += f"\n\nUser message to classify: {message}"

        return prompt

    def classify(self, message: str) -> NLUResponse:
        prompt_str = self._build_prompt(message)
        # print(f"classify prompt: {prompt_str}")
        chain = self.prompt_template | self.model | self.parser
        return chain.invoke({"prompt": prompt_str})
