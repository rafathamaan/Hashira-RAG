import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import logging, time

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
os.environ["TOKENIZERS_PARALLELISM"] = "false"

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("🔐 API Keys Loaded: %s", {
    "OpenAI": bool(OPENAI_API_KEY),
    "OpenRouter": bool(OPENROUTER_API_KEY),
    "Groq": bool(GROQ_API_KEY)
})

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, prefer_grpc=False)
qdrant = Qdrant(client=client, collection_name="garden_docs", embeddings=embedding_model)

def get_llm():
    try:
        if OPENROUTER_API_KEY:
            logger.info("✅ Using OpenRouter GPT-3.5")
            return ChatOpenAI(
                model="openai/gpt-3.5-turbo",
                api_key=OPENROUTER_API_KEY,
                base_url="https://openrouter.ai/api/v1",
                timeout=90,
            )
    except Exception as e:
        logger.error("❌ OpenRouter failed: %s", e)
    try:
        if GROQ_API_KEY:
            logger.info("✅ Using Groq LLaMA 3.1 70B")
            return ChatGroq(model="llama3-70b-8192", api_key=GROQ_API_KEY, timeout=90)
    except Exception as e:
        logger.error("❌ Groq failed: %s", e)
    raise RuntimeError("No valid LLM available. Please check your API keys.")

llm = get_llm()

system_prompt = (
    "You are an expert assistant for the Garden SDK React Quickstart. "
    "Using the following documentation context, answer the user's question in detail, including all code blocks, multi-step instructions, and important notes relevant to the question. "
    "If this is a follow-up, use previous questions and answers too. "
    "Format your answer using markdown. If the answer requires a sequence, enumerate the steps. "
    "If an answer can't be formed from the documentation, return amessage stating you dont know the answer and show link to https://docs.garden.finance/ . Don't try to make up an answer. \n\n"
    "Context:\n{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}")
])

stuff_chain = create_stuff_documents_chain(llm, prompt)


retriever = qdrant.as_retriever(search_kwargs={"k": 10})

qa_chain = create_retrieval_chain(retriever, stuff_chain)

def answer_question(query: str, chat_history=None):
    try:
        logger.info("Qdrant search started")
        t0 = time.time()
        
        message_input = query
        if chat_history and isinstance(chat_history, list):
            history_text = ""
            for turn in chat_history:
                if "user" in turn:
                    history_text += f"User: {turn['user']}\n"
                if "assistant" in turn:
                    history_text += f"Assistant: {turn['assistant']}\n"
            message_input = history_text + "User: " + query

        response = qa_chain.invoke({"input": message_input})
        logger.info(f"QA chain done in {time.time() - t0:.1f}s.")

        answer = response.get("answer", "")
        docs = retriever.get_relevant_documents(query)
        sources = [d.page_content for d in docs]

        return {"answer": answer.strip(), "sources": sources}
    except Exception as e:
        logger.error("Error during QA answering:", exc_info=True)
        return {"answer": f"❌ Error: {e}", "sources": []}

@app.post("/ask")
async def ask(request: Request):
    try:
        data = await request.json()
    except Exception:
        return {"answer": "❌ Invalid JSON request.", "sources": []}
    question = data.get("question") or data.get("query")
    chat_history = data.get("history", None)  
    if not question:
        return {"answer": "❌ Missing 'question' or 'query' field.", "sources": []}
    result = answer_question(question, chat_history=chat_history)
    return result
