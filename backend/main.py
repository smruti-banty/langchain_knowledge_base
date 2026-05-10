from dotenv import load_dotenv
from fastapi import FastAPI

from config.fastapi_setup import cors_setup_fastapi
from api.chat import router as chat_router

load_dotenv()

app = FastAPI()

cors_setup_fastapi(app)

app.include_router(chat_router)

@app.get("/")
async def health_check():
    return {"status": "running"}
