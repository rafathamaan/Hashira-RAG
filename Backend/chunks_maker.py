from langchain.text_splitter import RecursiveCharacterTextSplitter
with open('total_docs.md', 'r', encoding='utf-8') as f:
    full_text = f.read()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,    
    chunk_overlap=200    
)

chunks = text_splitter.split_text(full_text)

print(f"Total chunks: {len(chunks)}")

with open('doc_chunks.txt', 'w', encoding='utf-8') as f:
    for i, chunk in enumerate(chunks):
        f.write(f"---Chunk {i+1}---\n{chunk}\n\n")
