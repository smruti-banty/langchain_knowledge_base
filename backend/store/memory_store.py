from model.chat import ChatRecord
import asyncio

from store.mongo_store import save_chat
from store.vector_store import save_personalized_message, retriver_memory_context


async def store_chat_history(chat_record: ChatRecord):
    """This store complete chat history in mongodb"""
    await save_chat(
        [chat_record.user_message, chat_record.ai_message], chat_record.session_id
    )


async def store_personalize_message(chat_record: ChatRecord):
    """This store personalize message in vectore db"""
    await save_personalized_message(chat_record)


async def process_chat(chat_record: ChatRecord):
    await asyncio.gather(
        store_chat_history(chat_record), store_personalize_message(chat_record)
    )


async def get_relevant_message_by_session_id(session_id, message):
    return retriver_memory_context(message=message, session_id=session_id)
