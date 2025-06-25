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
    with open("frontend/styles.css", "r") as f:
        custom_css = f.read()
    custom_theme = gr.themes.Base(
        primary_hue="green",
        secondary_hue="teal",
        neutral_hue="slate",
        font=["Inter", "Segoe UI", "sans-serif"],
        font_mono=["Fira Mono", "Consolas", "monospace"]
    )
    with gr.Blocks(theme=custom_theme, css=custom_css) as demo:
        # Falling leaves animation container and script
        gr.HTML("""
        <div id='leaves-container'></div>
        <script>
        function randomBetween(a, b) { return a + Math.random() * (b - a); }
        function createLeaf(i) {
            var leaf = document.createElement('div');
            leaf.className = 'leaf';
            leaf.style.left = randomBetween(0, 98) + 'vw';
            leaf.style.animationDelay = randomBetween(0, 8) + 's';
            leaf.style.animationDuration = randomBetween(6, 12) + 's';
            leaf.style.transform = 'rotate(' + randomBetween(0, 360) + 'deg)';
            document.getElementById('leaves-container').appendChild(leaf);
        }
        if (typeof window !== 'undefined' && document.getElementById('leaves-container')) {
            for (var i = 0; i < 16; i++) createLeaf(i);
        }
        </script>
        """)
        gr.Markdown("""
        <div style='display: flex; align-items: center; gap: 12px;'>
            <span style='font-size:2.2em;'>🤖</span>
            <span style='font-family: Fira Mono, monospace; font-size: 1.7em; color: #388e3c;'>ChatbotTherapy</span>
        </div>
        <div style='margin-top: 0.5em; color: #234c2e; font-size: 1.1em;'>
            Welcome! This is your <b>offline AI therapist</b>.<br>
            <span style='color:#388e3c;'>Reflect, heal, grow</span> — with a touch of <span style='font-family: Fira Mono, monospace; color: #388e3c;'>AI</span>.
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
