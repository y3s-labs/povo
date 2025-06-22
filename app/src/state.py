from typing import Optional
from typing import Annotated, Literal
from typing_extensions import TypedDict

from langgraph.graph.message import add_messages

from .types import Session, User


class State(TypedDict):
    messages: Annotated[list, add_messages]
    session: Session
    user: User
    intent: str | None
    next: str | None
