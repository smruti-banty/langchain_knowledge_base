import os

from langchain_ollama import OllamaEmbeddings, ChatOllama

BASE_URL = os.getenv("LLM_BASE_URL")

# llm = ChatNVIDIA(model="mistralai/mistral-medium-3.5-128b", temperature=0.5)
main_llm = ChatOllama(model="gemma4", temperature=0.5, base_url=BASE_URL)

embed_llm = OllamaEmbeddings(model="nomic-embed-text", base_url=BASE_URL)

summarize_llm = ChatOllama(model='phi4', base_url=BASE_URL, temperature=0)