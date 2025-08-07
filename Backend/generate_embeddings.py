from langchain.embeddings import HuggingFaceEmbeddings

chunks = []
with open('doc_chunks.txt', 'r', encoding='utf-8') as f:
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
embeddings = embedding_model.embed_documents(chunks)

print(f"Generated embeddings for {len(embeddings)} chunks")
