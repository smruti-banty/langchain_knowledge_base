import os
from pymongo import AsyncMongoClient

client = AsyncMongoClient(os.getenv('MONGO_URL'))

db = client["langchain_knowledge_base"]

chat_history_collection = db['chat_history']