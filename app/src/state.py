from typing import Optional
from typing import Annotated, Literal
from typing_extensions import TypedDict

from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]
    intent: str | None
    next: str | None
