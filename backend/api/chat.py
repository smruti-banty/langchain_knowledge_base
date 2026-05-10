from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from service.streaming_response import generate
from model.chat import Item

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/")
async def chat(item: Item):
    return StreamingResponse(generate(item), media_type="text/event-stream")
