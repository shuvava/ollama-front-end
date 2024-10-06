#!/usr/bin/env python3
import json
import logging
from typing import List, Dict

from pydantic import BaseModel, Field, validator
from fastapi import FastAPI, Depends, status
from fastapi.responses import JSONResponse
from .auth import get_api_key

from .ai_ollama import chat as ollama_chat

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class ChatRequest(BaseModel):
    model: str = Field(default="llama3")
    messages: List[Dict[str, str]]
    response_format: str = Field(default="json", alias="format", description="Response LLM format")

    @validator('response_format')
    def validate_response_format(cls, v):
        allowed_values = ["text", "json"]
        if v.lower() not in allowed_values:
            raise ValueError(f"Invalid response format. Allowed values are: {', '.join(allowed_values)}")
        return v.lower()

@app.post("/chat")
async def chat(body: ChatRequest, api_key: str = Depends(get_api_key)):
    # Log the request body
    logger.info(f"Request body: {body.json()}")
    
    json_response = body.response_format.lower() == "json"
    
    # Use a semaphore to restrict parallel requests
    async with app.state.semaphore:
        response = ollama_chat(body.messages, body.model, json_response)
    
    return response

# Initialize the semaphore in the app's state
@app.on_event("startup")
async def startup_event():
    import asyncio
    from .config import settings
    max_parallel_requests = settings.max_parallel_requests
    app.state.semaphore = asyncio.Semaphore(max_parallel_requests)

@app.get("/healthz", status_code=status.HTTP_200_OK)
async def liveness_check():
    return JSONResponse(content={"status": "alive"})

@app.get("/ready", status_code=status.HTTP_200_OK)
async def readiness_check():
    # You can add any additional checks here (e.g., database connection)
    return JSONResponse(content={"status": "ready"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
