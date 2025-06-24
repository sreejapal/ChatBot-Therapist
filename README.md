# 🧠 ChatBot-Therapist: Your Offline AI Mental Health Companion

ChatBot-Therapist is a privacy-first, offline AI-powered mental health assistant that helps users reflect on their emotions, gain insights, and receive healing guidance—without needing the internet or cloud access.

Built using **LangChain**, **ChromaDB**, **Ollama**, and **Gradio**, this app runs entirely on your local machine using powerful open-source language models like **Mistral**.

---

## ✨ Features

- 🧘‍♀️ **Emotionally Supportive Conversations**
  - Reflects user input in a warm, empathetic tone
  - Asks thoughtful follow-up questions
  - Offers helpful suggestions like journaling or breathing exercises

- 📈 **Emotion Tracking**
  - Detects emotions in user messages (e.g., sadness, anger, joy)
  - Logs them securely in local JSON files
  - Creates weekly, monthly, and overall emotional summaries

- 🔍 **Searchable Memory (via ChromaDB)**
  - Remembers your past chats contextually
  - Allows you to search past conversations by keyword or feeling

- 🛠️ **Offline & Private**
  - No internet needed
  - All data stays on your device
  - Powered by Ollama and open-source LLMs

- 🎛️ **Minimal UI with Gradio**
  - Clean input field, press "Enter" to send
  - Click buttons for summaries, logs, and clearing history

---

## 🧠 Tech Stack

| Tool               | Purpose                                   |
|--------------------|-------------------------------------------|
| LangChain          | Orchestration of LLM + memory + prompts   |
| ChromaDB           | Vector search for memory retrieval        |
| Ollama + Mistral   | Local LLM execution                       |
| Gradio             | User interface (frontend)                 |
| JSON + Matplotlib  | Emotion logging + summary visualization   |

---

## 🚀 Getting Started

### 1. Clone the repo
git clone https://github.com/sreejapal/ChatBot-Therapist.git
cd ChatBot-Therapist

### 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate    # or `venv\Scripts\activate` on Windows

### 3. Install dependencies
pip install -r requirements.txt

### 4. Make sure Ollama is installed and Mistral is pulled
ollama run mistral

### 5. Run the app
python main.py
Then open: http://127.0.0.1:7860

#### 🛡️ Disclaimer
This AI is a support tool, not a replacement for licensed therapists. Always consult a professional for serious mental health concerns.

#### 👩‍💻 Author
Made with 💙 by Sreeja Pal
Built to promote emotional independence, healing, and tech-driven well-being.

