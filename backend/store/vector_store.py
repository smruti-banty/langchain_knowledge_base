from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_chroma import Chroma

from config.llm_detail import embed_llm, summarize_llm
from model.chat import ChatRecord, MemoryExtraction
from util.prompt import memory_extraction_prompt

SIMILARITY_THRESHOLD = 0.15

chroma = Chroma(
    collection_name="semantic_memory",
    embedding_function=embed_llm,
    persist_directory="./.chroma_db",
)

# splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)

structured_llm = summarize_llm.with_structured_output(MemoryExtraction)


async def summarize_conversation(chat: ChatRecord) -> MemoryExtraction:
    messages = [
        SystemMessage(content=memory_extraction_prompt),
        HumanMessage(content=chat.user_message.content),
        AIMessage(content=chat.ai_message.content),
    ]

    response = await structured_llm.ainvoke(messages)

    return response


def is_duplicate_memory(memory: str, session_id: str) -> bool:
    """
    Check whether semantic memory already exists.

    Uses vector similarity search instead of exact matching
    """

    results = chroma.similarity_search_with_score(
        query=memory, k=1, filter={"session_id": session_id}
    )

    if not results:
        return False

    _, score = results[0]

    return score <= SIMILARITY_THRESHOLD


async def save_personalized_message(chat_record: ChatRecord):
    summarize_memory_response = await summarize_conversation(chat_record)
    if not summarize_memory_response.should_store:
        return

    if is_duplicate_memory(summarize_memory_response.memory, chat_record.session_id):
        print("Duplicate entry")
        return

    chroma.add_texts(
        texts=[summarize_memory_response.memory],
        metadatas=[
            {
                "session_id": chat_record.session_id,
                "memory_type": summarize_memory_response.memory_type,
            }
        ],
    )

    print("Data stored")


async def retriver_memory_context(query: str, session_id: str, k: int = 3) -> str:
    """
    Retrieve top matching semantic memories

    from ChromaDB and return formatted context.
    """
    responses = chroma.similarity_search_with_score(
        query=query, k=k, filter={"session_id": session_id}
    )

    if not responses:
        return ""

    return "\n".join(
        f"- {document.page_content}"
        for document, score in responses
        if score <= SIMILARITY_THRESHOLD
    )
