# app.py

import gradio as gr
from inference import generate_voice

def process(text, audio):
    if not text:
        return None, "Please enter text"

    if not audio:
        return None, "Please upload a reference voice"

    output_path = generate_voice(text, audio)

    if isinstance(output_path, str) and output_path.startswith("Error"):
        return None, output_path

    return output_path, "Voice generated successfully!"

interface = gr.Interface(
    fn=process,
    inputs=[
        gr.Textbox(label="Enter Text"),
        gr.Audio(type="filepath", label="Upload Reference Voice")
    ],
    outputs=[
        gr.Audio(label="Generated Voice"),
        gr.Textbox(label="Status")
    ],
    title="🎤 VoxAgent - Voice Cloning System",
    description="Generate speech using your own voice sample"
)

if __name__ == "__main__":
    interface.launch()