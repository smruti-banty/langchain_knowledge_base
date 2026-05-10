from langchain_chroma import Chroma

from config.llm_detail import embed_llm

DB_LOCATION = ".chroma"

chroma = Chroma(embedding_function=embed_llm, database=DB_LOCATION)

