import gradio as gr
import requests
import webbrowser
import subprocess
import sys
import time
from app.logic import process_user_input
from app.memory import clear_memory, search_memory
from assets.dashboard import (
    generate_weekly_summary,
    generate_monthly_summary,
    generate_overall_summary
)

session_history = []

# Backend trigger functions
BACKEND_URL = "http://localhost:5000/launch_dashboard"
DASHBOARD_URLS = {
    'weekly':  'http://localhost:7861',
    'monthly': 'http://localhost:7862',
    'overall': 'http://localhost:7863',
    'search':  'http://localhost:7864',
}

def launch_dashboard(dashboard):
    try:
        requests.post(BACKEND_URL, json={'dashboard': dashboard}, timeout=1)
    except Exception:
        pass  # Ignore errors (dashboard may already be running)
    time.sleep(2)  # Give the dashboard time to start
    webbrowser.open_new(DASHBOARD_URLS[dashboard])
    return None

def chat(user_input):
    from app.logic import process_user_input
    global session_history
    result = process_user_input(user_input, session_history)  
    session_history.append([user_input, result["reflection"]])  
    questions_output = "\n".join(result.get("questions", [])) or "No questions."
    suggestions_output = "\n".join(result.get("suggestions", [])) or "No suggestions."
    return result["reflection"], questions_output, suggestions_output, "" 

def reset_all():
    global session_history
    session_history = []
    clear_memory()
    return "", "", "", ""

def show_weekly_summary():
    summary, img = generate_weekly_summary()
    return summary, img or None

def show_monthly_summary():
    summary, img = generate_monthly_summary()
    return summary, img or None

def show_overall_summary():
    summary, img = generate_overall_summary()
    return summary, img or None

def search_chat_history(query):
    results = search_memory(query)
    if not results:
        return "No matching results found."
    return "\n\n".join([f"🧍 {u}\n🤖 {b}" for u, b in results])

def chatbot_ui():
    custom_theme = gr.themes.Base(
        primary_hue="orange",
        secondary_hue="teal",
        neutral_hue="slate",
        font=["Inter", "Segoe UI", "sans-serif"],
        font_mono=["Fira Mono", "Consolas", "monospace"]
    )
    with gr.Blocks(theme=custom_theme, css="""
        body { background: linear-gradient(135deg, #f8fafc 0%, #fbeee6 100%); }
        .gr-box, .gr-textbox, .gr-button { box-shadow: 0 2px 8px rgba(0,0,0,0.04); border-radius: 10px; }
        .gr-textbox { border: 1.5px solid #fbbf24; }
        .gr-button { font-weight: 600; }
        .gr-markdown { font-size: 1.1em; }
    """) as demo:
        gr.Markdown("""
        <div style='display: flex; align-items: center; gap: 12px;'>
            <span style='font-size:2.2em;'>🤖</span>
            <span style='font-family: Fira Mono, monospace; font-size: 1.7em; color: #f59e42;'>ChatbotTherapy</span>
        </div>
        <div style='margin-top: 0.5em; color: #334155; font-size: 1.1em;'>
            Welcome! This is your <b>offline AI therapist</b>.<br>
            <span style='color:#0d9488;'>Reflect, heal, grow</span> — with a touch of <span style='font-family: Fira Mono, monospace; color: #6366f1;'>AI</span>.
        </div>
        """, elem_id="header")

        with gr.Row():
            clear_btn = gr.Button("🧹 Clear All (Memory + Logs)")
            weekly_btn = gr.Button("📅 Weekly Summary")
            monthly_btn = gr.Button("📆 Monthly Summary")
            overall_btn = gr.Button("📊 Overall Summary")
            search_btn = gr.Button("🔍 Search History")

        with gr.Row():
            with gr.Column():
                reflection_output = gr.Textbox(label="🪞 Reflection", lines=4, interactive=False, elem_id="reflection_box")
                questions_output = gr.Textbox(label="❓ Follow-up Questions", lines=3, interactive=False, elem_id="questions_box")
                suggestions_output = gr.Textbox(label="💡 Suggestions", lines=3, interactive=False, elem_id="suggestions_box")
                user_input = gr.Textbox(placeholder="Type your message and press Enter", show_label=False, elem_id="user_input_box")

        # Events
        user_input.submit(chat, inputs=user_input, outputs=[reflection_output, questions_output, suggestions_output, user_input])
        clear_btn.click(reset_all, outputs=[reflection_output, questions_output, suggestions_output, user_input])
        weekly_btn.click(lambda: launch_dashboard('weekly'), outputs=None)
        monthly_btn.click(lambda: launch_dashboard('monthly'), outputs=None)
        overall_btn.click(lambda: launch_dashboard('overall'), outputs=None)
        search_btn.click(lambda: launch_dashboard('search'), outputs=None)

    return demo

if __name__ == "__main__":
    # Launch the launcher_api.py Flask server as a subprocess
    subprocess.Popen([sys.executable, "launcher_api.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Wait a moment to ensure the Flask server is up
    time.sleep(2)
    chatbot_ui().launch(inbrowser=True, share=True)
