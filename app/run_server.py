#!/usr/bin/env python3
"""
FastAPI launcher for the Povo Chatbot
"""
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph.message import add_messages
# from state import State
# from services.chat_service import ChatService
# from services.classifier import Classifier
import uvicorn
from typing import List, Optional
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
import sys
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


class Message(BaseModel):
    text: str


class User(BaseModel):
    id: str
    data: dict


class Session(BaseModel):
    id: str
    new: bool
    data: dict


class ChatRequestBody(BaseModel):
    message: Message
    session: Session
    user: User


class ChatRequest(BaseModel):
    body: ChatRequestBody


class ChatResponse(BaseModel):
    response: str
    intent: Optional[str] = None
    session_id: Optional[str] = None


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
        user_id = request.body.user.userId
        session_id = request.body.session.id

        print(f"Received message: {message_text}")
        print(f"User ID: {user_id}")
        print(f"Session ID: {session_id}")

        # Invoke the graph
        # result_state = graph.invoke(initial_state)

        return {"message": "hello"}

    except Exception as e:
        print(f"Error processing chat: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error processing chat: {str(e)}") from e

if __name__ == "__main__":
    print("Starting Povo Chatbot API server...")
    print("API will be available at: http://localhost:8000")
    print("API documentation at: http://localhost:8000/docs")
    uvicorn.run("run_server:app", host="0.0.0.0", port=8000, reload=True)
