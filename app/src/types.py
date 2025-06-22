from pydantic import BaseModel


class Message(BaseModel):
    text: str


class User(BaseModel):
    id: str
    data: dict


class Session(BaseModel):
    id: str
    new: bool
    data: dict
