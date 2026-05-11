import asyncio

from langchain_core.runnables import RunnableWithMessageHistory

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
)

from langchain.messages import SystemMessage

from model.chat import Item, ChatMessage, ChatRecord
from store.memory_store import process_chat
from config.llm_detail import main_llm
from util.prompt import main_chat_prompt
from store.in_memory_store import remove_session_history, get_session_history
from agent.tool import retrieve_memory

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=main_chat_prompt),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}"),
    ]
)

main_llm_with_tool = main_llm.bind_tools([retrieve_memory])

base_chain = prompt | main_llm_with_tool
chain = RunnableWithMessageHistory(
    runnable=base_chain,
    get_session_history=get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)


async def generate(item: Item):
    full_message = ""
    async for chunk in chain.astream(
        item.message, {"configurable": {"session_id": item.session_id}}
    ):
        if chunk.content:
            full_message += chunk.content
            yield chunk.content

    remove_session_history(item.session_id)

    user_message = ChatMessage(item.session_id, "human", item.message)
    ai_message = ChatMessage(item.session_id, "ai", full_message)

    asyncio.create_task(
        process_chat(ChatRecord(item.session_id, user_message, ai_message))
    )
