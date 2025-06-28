---
title: ChatBot-Therapist
app_file: main.py
sdk: flask
sdk_version: 3.0.0
---
# 🧠 ChatBot-Therapist: Your Offline AI Mental Health Companion

ChatBot-Therapist is a privacy-first, offline AI-powered mental health assistant that helps users reflect on their emotions, gain insights, and receive healing guidance—without needing the internet or cloud access.

Built using **LangChain**, **ChromaDB**, **Ollama**, and **Flask**, this app runs entirely on your local machine using powerful open-source language models like **Mistral**.

---

## ✨ Features

### 🧘‍♀️ **Enhanced Therapy Sessions**
- **Session Management**: Start new sessions, view session info, and track conversation history
- **Emotionally Supportive Conversations**: Reflects user input in a warm, empathetic tone
- **Thoughtful Follow-up Questions**: Asks 2-3 open-ended questions to encourage deeper reflection
- **Evidence-Based Suggestions**: Offers clinically proven coping strategies and healing activities

### 📊 **Advanced Session History & Search**
- **Session Summaries**: View first messages from each therapy session for quick overview
- **Full Conversation View**: Click any session to see complete back-and-forth conversations
- **Semantic Search**: Search across all sessions using natural language queries
- **Session Analytics**: Track message counts, emotions, and session duration

### 🎨 **Modern Web Interface**
- **Responsive Design**: Beautiful, modern UI with smooth animations and hover effects
- **Loading Indicators**: Visual feedback during AI processing with pulsing animations
- **Two-Row Button Layout**: Organized session management and dashboard access
- **Modal Dialogs**: Clean popup windows for session details and search results

### 📈 **Enhanced Emotion Tracking**
- **Real-time Emotion Detection**: Detects emotions in user messages (sadness, anger, joy, anxiety, etc.)
- **Sentiment Analysis**: Tracks emotional patterns over time
- **Secure Local Storage**: All data stored locally in JSON files and ChromaDB
- **Visual Summaries**: Weekly, monthly, and overall emotional trend analysis

### 🔍 **Intelligent Memory System**
- **Contextual Memory**: Remembers your past conversations for continuity
- **Vector Search**: Advanced semantic search using ChromaDB embeddings
- **Session Grouping**: Automatically groups related conversations into sessions
- **Fallback Parsing**: Robust regex-based parsing for AI responses

### 🛠️ **Privacy & Performance**
- **100% Offline**: No internet connection required
- **Local Processing**: All AI processing happens on your device
- **Error Handling**: Graceful fallbacks and helpful error messages
- **Session Persistence**: Maintains conversation context across browser sessions

---

## 🧠 Tech Stack

| Tool               | Purpose                                   |
|--------------------|-------------------------------------------|
| LangChain          | Orchestration of LLM + memory + prompts   |
| ChromaDB           | Vector search for memory retrieval        |
| Ollama + Mistral   | Local LLM execution                       |
| Flask              | Web server and API endpoints              |
| HTML/CSS/JS        | Modern responsive frontend                |
| JSON + Matplotlib  | Emotion logging + summary visualization   |

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/sreejapal/ChatBot-Therapist.git
cd ChatBot-Therapist
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate    # or `venv\Scripts\activate` on Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install and start Ollama
```bash
# Install Ollama (if not already installed)
# Visit: https://ollama.ai/download

# Pull the Mistral model
ollama pull mistral

# Start Ollama service (in background)
ollama serve
```

### 5. Run the app
```bash
python main.py
```

### 6. Open your browser
The app will automatically open at: **http://127.0.0.1:5000**

---

## 🎯 How to Use

### **Starting a Therapy Session**
1. Type your message in the chat input
2. Press **Enter** or wait for the AI to respond
3. Receive reflection, questions, and suggestions
4. Continue the conversation naturally

### **Managing Sessions**
- **🆕 New Session**: Start a fresh therapy session
- **ℹ️ Session Info**: View current session details
- **🧹 Clear All**: Reset everything (use with caution)

### **Exploring Your History**
- **🔍 Search**: Find specific conversations or topics
- **📜 History**: Browse all your therapy sessions
- **📅 Dashboards**: View emotional trends and summaries

### **Session Features**
- **Click any session** to view the full conversation
- **Search across sessions** using natural language
- **Track your progress** with emotion and sentiment analysis

---

## 🔧 Advanced Features

### **Session Management**
- **Automatic Session Detection**: Groups related conversations
- **Manual Session Control**: Start new sessions anytime
- **Session Persistence**: Maintains context across browser sessions

### **Enhanced Search**
- **Semantic Search**: Find conversations by meaning, not just keywords
- **Session-Based Results**: See which sessions contain relevant content
- **Quick Preview**: View first messages before diving into full conversations

### **Error Recovery**
- **Graceful Fallbacks**: Helpful responses when AI processing fails
- **Robust Parsing**: Multiple methods to extract AI responses
- **User-Friendly Errors**: Clear messages when something goes wrong

---

## 🛡️ Privacy & Security

- **100% Local**: All processing happens on your device
- **No Data Sharing**: Nothing is sent to external servers
- **Secure Storage**: Data encrypted and stored locally
- **Session Isolation**: Each browser session is independent

---

## 🚨 Disclaimer

This AI is a support tool, not a replacement for licensed therapists. Always consult a professional for serious mental health concerns. The app is designed to complement, not replace, professional mental health care.

---

## 👩‍💻 Author

Made with 💙 by Sreeja Pal

Built to promote emotional independence, healing, and tech-driven well-being.

---

## 🔄 Recent Updates

### **v2.0 - Enhanced Session Management**
- ✨ New session management system
- 🎨 Modern web interface with responsive design
- 🔍 Advanced search with session summaries
- 📊 Improved emotion tracking and analytics
- 🛡️ Better error handling and user experience
- 🎯 Two-row button layout for better organization

