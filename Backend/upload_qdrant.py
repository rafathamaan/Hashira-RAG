from langchain_qdrant import Qdrant
from langchain.embeddings import HuggingFaceEmbeddings
import os

chunks = []
with open('embedded_chunks.txt', 'r', encoding='utf-8') as f:
    current_chunk = []
    for line in f:
        if line.strip().startswith('---Chunk'):
            if current_chunk:
                chunks.append(''.join(current_chunk).strip())
                current_chunk = []
        else:
            current_chunk.append(line)
    if current_chunk:
        chunks.append(''.join(current_chunk).strip())

print(f"Loaded {len(chunks)} chunks")
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Qdrant.from_texts(
    texts=chunks,
    embedding=embedding_model,
    url=os.getenv("QDRANT_URL"), 
    api_key=os.getenv("QDRANT_API_KEY"),
    collection_name="garden_docs"
)
print(f"Uploaded {len(chunks)} chunks to Qdrant Cloud successfully.")
