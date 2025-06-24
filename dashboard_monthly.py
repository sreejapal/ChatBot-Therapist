import gradio as gr
from assets.dashboard import generate_monthly_summary

def show_monthly_summary():
    summary, img = generate_monthly_summary()
    return summary, img or None

with gr.Blocks() as demo:
    summary, img = show_monthly_summary()
    gr.Markdown("## Monthly Summary")
    gr.Textbox(value=summary, label="", lines=5, interactive=False)
    if img:
        gr.Image(img)

demo.launch(server_port=7862) 