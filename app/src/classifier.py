import json
from pathlib import Path
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel


class Intent(BaseModel):
    intent: str


class Classifier:
    def __init__(self, model: str = "gpt-4o"):
        self.model = ChatOpenAI(model=model, temperature=0)
        self.intent_data = self._load_model()
        self.parser = PydanticOutputParser(pydantic_object=Intent)
        self.prompt_template = PromptTemplate(
            template="{prompt}\n\n{format_instructions}",
            input_variables=["prompt"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()}
        )

    def _load_model(self) -> dict:
        base_path = Path(__file__).resolve().parent
        path = base_path / "model" / "en.json"
        with open(path, "r") as f:
            return json.load(f)["intents"]

    def _build_prompt(self, message: str) -> str:
        """Dynamically build a prompt using the intents and examples from en.json"""
        sorted_intents = sorted(self.intent_data.items()
                                )  # ensure deterministic ordering

        # Descriptions
        intent_descriptions = "\n".join(
            f'- "{intent_name}": {intent_def["description"]}'
            for intent_name, intent_def in sorted_intents
        )

        # Few-shot examples
        example_lines = []
        for intent_name, intent_def in sorted_intents:
            for example in intent_def.get("examples", []):
                example_lines.append(
                    f'Message: "{example}" → Intent: "{intent_name}"')

        example_block = "\n".join(example_lines)

        # Final prompt
        return f"""You are an intent classifier. Classify the user's message into one of the following intents:

{intent_descriptions}

Here are some examples:
{example_block}

Now classify this message:
Message: "{message}"

Respond in this JSON format:
{{ "intent": "<intent_name_from_above>" }}
"""

    def classify(self, message: str) -> Intent:
        prompt_str = self._build_prompt(message)
        chain = self.prompt_template | self.model | self.parser
        return chain.invoke({"prompt": prompt_str})
