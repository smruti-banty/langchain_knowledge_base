from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_ollama import ChatOllama
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from fastapi_setup import app

load_dotenv()

store = {}

def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()

    return store[session_id]


# llm = ChatNVIDIA(model="mistralai/mistral-medium-3.5-128b", temperature=0.5)
llm = ChatOllama(model="gemma4", temperature=0.5)
chain = RunnableWithMessageHistory(llm, get_session_history)

class Item(BaseModel):
    message: str
    session_id: str

@app.post("/")
async def main(item: Item):
    
    async def generate():
        async for chunk in chain.astream(item.message, {
            "configurable": {
                "session_id": item.session_id
            }
        }):
            if chunk.content:
                yield chunk.content
    
    return StreamingResponse(generate(), media_type="text/event-stream")


if __name__ == "__main__":
    main()
