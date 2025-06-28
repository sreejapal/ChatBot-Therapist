import os
import json
from datetime import datetime
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.memory import ConversationBufferMemory
import uuid
from models.ollama_runner import load_llm
from app.utils import detect_emotion

CHROMA_DB_PATH = "data/chroma_db"
EMOTION_LOG_FILE = "data/emotion_log.json"
chroma_collection = None
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

def get_last_session_id():
    if not os.path.exists(EMOTION_LOG_FILE):
        return None
    with open(EMOTION_LOG_FILE, "r") as f:
        data = json.load(f)
    if not data:
        return None
    return data[-1].get("session_id")

def start_new_session():
    return str(uuid.uuid4())

def get_chroma_collection():
    global chroma_collection
    if chroma_collection is None:
        os.makedirs(CHROMA_DB_PATH, exist_ok=True)
        chroma_collection = Chroma(
            persist_directory=CHROMA_DB_PATH,
            embedding_function=OllamaEmbeddings(model="mistral")
        )
    return chroma_collection

def save_to_memory(user_input, emotion=None, session_id=None, sentiment_score=None, message_type="user"):
    buffer_memory.save_context(
        {"user_input": user_input},
        {"chat_history": buffer_memory.load_memory_variables({})["chat_history"]}
    )

    log = {
        "timestamp": datetime.now().isoformat(),
        "user_input": user_input,
        "emotion": emotion or "unknown",
        "session_id": session_id or get_last_session_id() or start_new_session(),
        "sentiment_score": sentiment_score,
        "message_type": message_type
    }

    if message_type == "user":
        collection = get_chroma_collection()
        meta = log.copy()
        collection.add_texts([user_input], metadatas=[meta])

    if not os.path.exists(EMOTION_LOG_FILE):
        with open(EMOTION_LOG_FILE, "w") as f:
            json.dump([log], f, indent=2)
    else:
        with open(EMOTION_LOG_FILE, "r") as f:
            data = json.load(f)
        data.append(log)
        with open(EMOTION_LOG_FILE, "w") as f:
            json.dump(data, f, indent=2)

def search_memory(query, k=5):
    results = semantic_search_memory(query, k=k)
    if results:
        return [
            (r["user_input"], r["metadata"].get("emotion", "unknown"))
            for r in results
        ]
    if not os.path.exists(EMOTION_LOG_FILE):
        return []
    with open(EMOTION_LOG_FILE, "r") as f:
        data = json.load(f)
    formatted_results = []
    for entry in data:
        if query.lower() in entry.get("user_input", "").lower() or query.lower() in entry.get("emotion", "").lower():
            formatted_results.append((entry.get("user_input", ""), entry.get("emotion", "")))
    return formatted_results

def get_session_logs(session_id):
    if not os.path.exists(EMOTION_LOG_FILE):
        return []
    with open(EMOTION_LOG_FILE, "r") as f:
        data = json.load(f)
    return [entry for entry in data if entry.get("session_id") == session_id]

def get_all_sessions():
    if not os.path.exists(EMOTION_LOG_FILE):
        return []
    with open(EMOTION_LOG_FILE, "r") as f:
        data = json.load(f)
    sessions = {}
    for entry in data:
        sid = entry.get("session_id")
        if sid not in sessions:
            sessions[sid] = []
        sessions[sid].append(entry)
    return sessions

def semantic_search_memory(query, k=5):
    collection = get_chroma_collection()
    results = collection.similarity_search_with_score(query, k=k)
    return [
        {
            "user_input": r[0].page_content,
            "score": r[1],
            "metadata": r[0].metadata
        }
        for r in results
    ]

def analyze_history_with_langchain(question, session_id=None, days=None, k=20):
    """
    Use LangChain LLM to answer a question about the user's chat history.
    - If session_id is given, restrict to that session.
    - If days is given, restrict to recent days.
    - Otherwise, use semantic search to get k relevant messages.
    """
    llm = load_llm()
    logs = []
    if session_id:
        logs = get_session_logs(session_id)
    elif days:
        from datetime import datetime, timedelta
        cutoff = datetime.now() - timedelta(days=days)
        if not os.path.exists(EMOTION_LOG_FILE):
            return "No data."
        with open(EMOTION_LOG_FILE, "r") as f:
            all_logs = json.load(f)
        logs = [log for log in all_logs if datetime.fromisoformat(log["timestamp"]) >= cutoff]
    else:
        # Use semantic search to get k relevant messages
        results = semantic_search_memory(question, k=k)
        logs = [r["metadata"] for r in results]
    if not logs:
        return "No relevant chat history found."
    # Build a context string
    context = "\n".join([
        f"[{log['timestamp']}] {log.get('user_input', '')} (Emotion: {log.get('emotion', 'unknown')}, Sentiment: {log.get('sentiment_score', 'N/A')})"
        for log in logs if log.get('user_input')
    ])
    prompt = f"""
You are a highly skilled, deeply empathetic therapy assistant AI. Here is the user's chat history:
{context}

Now answer the following question about the user's history:
{question}

In your answer, always try to:
- Identify likely triggers and causes of emotional issues
- Point out any signs of deep-seated trauma or subconscious problems
- Highlight hidden patterns, repeated themes, or underlying issues
- Reference specific messages or emotional trends
- Be detailed, insightful, and compassionate

Respond with a thorough, personalized analysis. If you see no evidence for trauma or subconscious issues, say so gently.
"""
    response = llm.generate([prompt.strip()])
    return response.generations[0][0].text.strip()
