import asyncio

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory

from model.chat import Item, ChatMessage, ChatRecord
from service.memory_store import process_chat
from config.llm_detail import main_llm

store = {}


def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()

    return store[session_id]


chain = RunnableWithMessageHistory(main_llm, get_session_history)


async def generate(item: Item):
    full_message = ""
    async for chunk in chain.astream(
        item.message, {"configurable": {"session_id": item.session_id}}
    ):
        if chunk.content:
            full_message += chunk.content
            yield chunk.content

    user_message = ChatMessage(item.session_id, "human", item.message)
    ai_message = ChatMessage(item.session_id, "ai", full_message)

    asyncio.add_task(
        process_chat, ChatRecord(item.session_id, user_message, ai_message)
    )
