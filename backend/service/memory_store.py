from model.chat import ChatMessage, ChatRecord
import asyncio


async def store_chat_history(chat_record: ChatRecord):
    """This store complete chat history in mongodb"""
    pass


async def store_personalize_message(chat_record: ChatRecord):
    """This store personalize message in vectore db"""
    pass


async def process_chat(chat_record: ChatRecord):
    asyncio.gather(
        store_chat_history(chat_record), store_personalize_message(chat_record)
    )

async def get_relevant_message_by_session_id(session_id, message):
    pass