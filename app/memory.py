import os
import json
from datetime import datetime
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.memory import ConversationBufferMemory

CHROMA_DB_PATH = "data/chroma_db"
EMOTION_LOG_FILE = "data/emotion_log.json"

# Use ConversationBufferMemory for compatibility with latest LangChain
buffer_memory = ConversationBufferMemory(
    memory_key="chat_history",
    input_key="user_input"
)

def get_memory():
    return buffer_memory

def clear_memory():
    if os.path.exists(CHROMA_DB_PATH):
        import shutil
        shutil.rmtree(CHROMA_DB_PATH)
    os.makedirs(CHROMA_DB_PATH, exist_ok=True)
    if os.path.exists(EMOTION_LOG_FILE):
        os.remove(EMOTION_LOG_FILE)

def save_to_memory(user_input, emotion=None):
    buffer_memory.save_context(
        {"user_input": user_input},
        {"chat_history": buffer_memory.load_memory_variables({})["chat_history"]}
    )

    log = {
        "timestamp": datetime.now().isoformat(),
        "user_input": user_input,
        "emotion": emotion or "unknown"
    }

    if not os.path.exists(EMOTION_LOG_FILE):
        with open(EMOTION_LOG_FILE, "w") as f:
            json.dump([log], f, indent=2)
    else:
        with open(EMOTION_LOG_FILE, "r") as f:
            data = json.load(f)
        data.append(log)
        with open(EMOTION_LOG_FILE, "w") as f:
            json.dump(data, f, indent=2)

def search_memory(query):
    # ConversationBufferMemory does not have a retriever by default.
    # If you want semantic search, use a vector store memory. Otherwise, do a simple keyword search in the emotion log.
    if not os.path.exists(EMOTION_LOG_FILE):
        return []
    with open(EMOTION_LOG_FILE, "r") as f:
        data = json.load(f)
    formatted_results = []
    for entry in data:
        if query.lower() in entry.get("user_input", "").lower() or query.lower() in entry.get("emotion", "").lower():
            formatted_results.append((entry.get("user_input", ""), entry.get("emotion", "")))
    return formatted_results
