import gradio as gr
import discourse as d

# set a custom theme
theme = gr.themes.Default().set(
    body_background_fill="#000000",
)

with gr.Blocks(theme=theme) as ui:
    with gr.Row():
        with gr.Column(scale=1):
            message = gr.Audio(source="microphone", type="filepath")
            btn1 = gr.Button("Respond")
        with gr.Column(scale=1):
            audio_response = gr.Audio()
    with gr.Row():
        text_response = gr.Textbox(label="Transcript", max_lines=10)
        btn2 = gr.Button("Save Conversation")

    btn1.click(fn=d.respond, inputs=message, outputs=[audio_response, text_response])
    btn2.click(fn=d.memory)

ui.launch()
