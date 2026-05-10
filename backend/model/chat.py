from pydantic import BaseModel, Field
from typing import Literal, Optional, Dict, Any
from datetime import datetime


class ChatMessage(BaseModel):

    role: Literal["human", "ai", "system"]

    content: str

    created_at: datetime = Field(default_factory=datetime.now())

    # Optional extracted semantic memory
    memory: Optional[str] = None

    # Optional metadata
    metadata: Optional[Dict[str, Any]] = None


class ChatRecord(BaseModel):
    session_id: str

    user_message: ChatMessage

    ai_message: ChatMessage


class Item(BaseModel):
    message: str
    session_id: str