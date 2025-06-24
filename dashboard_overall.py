import gradio as gr
from assets.dashboard import generate_overall_summary

def show_overall_summary():
    summary, img = generate_overall_summary()
    return summary, img or None

with gr.Blocks() as demo:
    summary, img = show_overall_summary()
    gr.Markdown("## Overall Summary")
    gr.Textbox(value=summary, label="", lines=5, interactive=False)
    if img:
        gr.Image(img)

demo.launch(server_port=7863) 