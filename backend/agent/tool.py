from langchain.tools import tool

from store.vector_store import retriver_memory_context
from store.in_memory_store import get_session_history
from model.chat import ChatMessage


@tool
async def retrieve_memory(query: str, session_id: str) -> str:
    """
    Retrieve relevant long-term semantic memories about the user.

    Use this when:
    - user asks about previous discussions
    - user asks about projects
    - user asks about preferences
    - user asks about personal context
    """

    return retriver_memory_context(query=query, session_id=session_id)


@tool
def retrieve_recent_history(session_id: str) -> list[ChatMessage]:
    """
    Retrieve recent conversation history.
    Use this when current user message depends on previous conversational context.
    """

    history = get_session_history(session_id=session_id)

    return [
        ChatMessage(role=message.type, content=message.content)
        for message in history.messages
    ]
