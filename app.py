# app.py

import gradio as gr
from inference import generate_voice

def process(text, audio):
    if not text:
        return None, None, "Please enter text"

    if not audio:
        return None, None, "Please upload a reference voice"

    output_path = generate_voice(text, audio)

    if isinstance(output_path, str) and output_path.startswith("Error"):
        return None, None, output_path

    return output_path, output_path, "Voice generated successfully!"

with gr.Blocks(theme=gr.themes.Soft()) as demo:

    gr.Markdown("""
    # VoxAgent - Voice Cloning System
    Generate speech using your own voice sample
    """)

    with gr.Row():

        with gr.Column():
            text_input = gr.Textbox(
                label="Enter Text",
                placeholder="Type what you want the AI to say...",
                lines=4
            )

            audio_input = gr.Audio(
                type="filepath",
                label="Upload Voice Sample (Drag & Drop Supported)"
            )

            # 🚀 Colored button
            generate_btn = gr.Button("Generate Voice", variant="primary")

            # 🧹 Clear button
            clear_btn = gr.ClearButton(
                components=[text_input, audio_input],
                value="🧹 Clear Input"
            )

        with gr.Column():
            output_audio = gr.Audio(label="Generated Voice")

            download_btn = gr.File(label="⬇Download Audio")

            status = gr.Textbox(label="Status")

    # Generate action with loading animation
    generate_btn.click(
        fn=process,
        inputs=[text_input, audio_input],
        outputs=[output_audio, download_btn, status],
        show_progress=True
    )

demo.launch()
