from langchain.text_splitter import RecursiveCharacterTextSplitter

# Read the docs file
with open('total_docs.md', 'r', encoding='utf-8') as f:
    full_text = f.read()

# Initialize the splitter (adjust chunk size/overlap as needed)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Each chunk ~1000 characters
    chunk_overlap=200     # 200 character overlap for better query context
)

chunks = text_splitter.split_text(full_text)

print(f"Total chunks: {len(chunks)}")

# Save chunks for embedding
with open('doc_chunks.txt', 'w', encoding='utf-8') as f:
    for i, chunk in enumerate(chunks):
        f.write(f"---Chunk {i+1}---\n{chunk}\n\n")
