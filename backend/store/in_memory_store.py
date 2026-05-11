from collections import defaultdict

from langchain_core.chat_history import InMemoryChatMessageHistory

store = defaultdict(InMemoryChatMessageHistory)
MAX_HISTORY_MESSAGE = 6


def get_session_history(session_id) -> InMemoryChatMessageHistory:
    return store[session_id]


def remove_session_history(session_id: str):
    history = get_session_history(session_id=session_id)
    history.messages = history.messages[-MAX_HISTORY_MESSAGE:]
