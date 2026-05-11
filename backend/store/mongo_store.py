from config.mongo import chat_history_collection
from model.chat import ChatMessage, ChatResponse


async def save_chat(chat_message: list[ChatMessage], session_id: str):
    documents = [
        {**chat.model_dump(), "session_id": session_id} for chat in chat_message
    ]
    await chat_history_collection.insert_many(documents)


async def get_chat(session_id: str, limit=50, skip=0) -> list[ChatResponse]:
    cursor = (
        chat_history_collection.find({session_id: session_id}, {"_id", 0})
        .sort("created_at", 1)
        .skip(skip)
        .limit(limit)
    )

    documents = await cursor.to_list(length=limit)
    return [ChatResponse(**document) for document in documents]
