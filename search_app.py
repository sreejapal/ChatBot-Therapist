import gradio as gr
from app.memory import search_memory

def search_chat_history(query):
    results = search_memory(query)
    if not results:
        return "No matching results found."
    return "\n\n".join([f"🧍 {u}\n🤖 {b}" for u, b in results])

with gr.Blocks() as demo:
    gr.Markdown("## Search Your Therapy History")
    search_query = gr.Textbox(placeholder="Search keyword...", show_label=False)
    search_btn = gr.Button("Search")
    search_output = gr.Textbox(label="Search Results", lines=8, interactive=False)
    search_btn.click(search_chat_history, inputs=search_query, outputs=search_output)

demo.launch(server_port=7864) 