#!/usr/bin/env python3
"""
FastAPI launcher for the Povo Chatbot
"""
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph.message import add_messages
# from state import State
# from services.chat_service import ChatService
# from services.classifier import Classifier
from src.main import App
import uvicorn
from typing import List, Optional
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException

from src.types import Message, User, Session

import os

app = FastAPI(
    title="Povo Chatbot API",
    description="A conversational AI chatbot with intent classification",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for the new request format


class ChatRequestBody(BaseModel):
    message: Message
    session: Session
    user: User


class ChatRequest(BaseModel):
    body: ChatRequestBody


class ChatResponse(BaseModel):
    response: str
    intent: str
    session: Optional[Session] = None
    user: Optional[User] = None


@app.get("/")
async def root():
    return {"message": "Povo Chatbot API is running!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send a message to the chatbot and get a response.
    Expected request format:
    {
      "body": {
        "message": {
          "text": "Hi, I'm feeling anxious today",
        },
        "session": {
          "id": "session-abc",
          "flow": "general",
          "new": true
          "data": {}
        },
        "user": {
            "id": "user-123",
            "data": {}
        },
      }
    }
    """
    try:
        # Extract the message text from the nested structure
        message_text = request.body.message.text
        user = request.body.user
        session = request.body.session

        print(f"Received message: {message_text}")
        print(f"User ID: {user.id}")
        print(f"Session ID: {session.id}")

        # Invoke the graph
        state = App().run(message_text, session, user)

        print(f"<<final state>>: {state}")

        return ChatResponse(
            response=state["messages"][-1].content,
            intent=state["intent"],
            session=state["session"],
            user=state["user"],
        )

    except Exception as e:
        print(f"Error processing chat: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error processing chat: {str(e)}") from e
