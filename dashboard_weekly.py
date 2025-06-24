import gradio as gr
from assets.dashboard import generate_weekly_summary

def show_weekly_summary():
    summary, img = generate_weekly_summary()
    return summary, img or None

with gr.Blocks() as demo:
    summary, img = show_weekly_summary()
    gr.Markdown("## Weekly Summary")
    gr.Textbox(value=summary, label="", lines=5, interactive=False)
    if img:
        gr.Image(img)

demo.launch(server_port=7861) 