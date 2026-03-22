# app.py

import gradio as gr
from inference import generate_voice

def process(text, audio, speed, pitch):
    # Basic input validation
    if not text:
        return None, None, "Please enter text"

    if not audio:
        return None, None, "Please upload a reference voice"

    # Wrap the generation in a try-except block for better error handling
    try:
        # Pass the new speed and pitch parameters to your updated inference function
        output_path = generate_voice(
            text=text, 
            speaker_wav=audio, 
            speed=speed, 
            pitch=pitch
        )
        return output_path, output_path, "Voice generated successfully!"
        
    except Exception as e:
        # If the model runs out of memory or a file is missing, it returns the error safely
        return None, None, f"Error generating voice: {str(e)}"

with gr.Blocks(theme=gr.themes.Soft()) as demo:

    gr.Markdown("""
    # VoxAgent - Voice Cloning System
    Generate speech using your own voice sample.
    
    🎭 **Pro-Tip for Emotion Control:** The AI copies the exact tone of your uploaded audio. 
    To force an emotion, upload a reference voice speaking in that tone, and use punctuation in your text (e.g., use `!!!` for shouting or `...` for hesitance/sadness).
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
            
            # 🎛️ Advanced Settings for Speed and Pitch
            with gr.Accordion("Advanced Audio Settings", open=False):
                speed_slider = gr.Slider(
                    minimum=0.5, maximum=2.0, value=1.0, step=0.1, 
                    label="Speech Speed (1.0 is normal)"
                )
                pitch_slider = gr.Slider(
                    minimum=-5.0, maximum=5.0, value=0.0, step=0.5, 
                    label="Pitch (Negative = Deep, Positive = High)"
                )

            # 🚀 Colored button
            generate_btn = gr.Button("Generate Voice", variant="primary")

            # 🧹 Clear button (updated to clear the sliders as well)
            clear_btn = gr.ClearButton(
                components=[text_input, audio_input, speed_slider, pitch_slider],
                value="🧹 Clear Input"
            )

        with gr.Column():
            output_audio = gr.Audio(label="Generated Voice")

            download_btn = gr.File(label="⬇ Download Audio")

            status = gr.Textbox(label="Status")

    # Generate action with loading animation (wiring the new inputs)
    generate_btn.click(
        fn=process,
        inputs=[text_input, audio_input, speed_slider, pitch_slider],
        outputs=[output_audio, download_btn, status],
        show_progress=True
    )

if __name__ == "__main__":
    demo.launch()
