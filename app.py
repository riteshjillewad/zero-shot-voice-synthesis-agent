# app.py

import gradio as gr
from inference import generate_voice

# Add the dictionary here
SUPPORTED_LANGUAGES = {
    "English": "en", "Spanish": "es", "French": "fr", "German": "de", 
    "Italian": "it", "Portuguese": "pt", "Hindi": "hi", "Japanese": "ja", 
    "Chinese": "zh-cn", "Arabic": "ar", "Russian": "ru", "Korean": "ko"
}

def process(text, audio, speed, pitch, consent_given, language_name):
    # 1. Security & Compliance Check
    if not consent_given:
        return None, None, "Error: You must confirm you have the right to use this voice."

    # 2. Basic input validation
    if not text:
        return None, None, "Please enter text"

    if not audio:
        return None, None, "Please upload a reference voice"
    
    # Look up the correct code (e.g., "Hindi" -> "hi")
    lang_code = SUPPORTED_LANGUAGES.get(language_name, "en")

    # 3. Model Execution with Error Handling
    try:
        output_path = generate_voice(
            text=text, 
            speaker_wav=audio, 
            speed=speed, 
            pitch=pitch,
            lang_code=lang_code
        )
        return output_path, output_path, f"Voice generated successfully in {language_name}!"
        
    except Exception as e:
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
            
            # 🌍 ADDED: The Language Dropdown UI Component
            language_dropdown = gr.Dropdown(
                choices=list(SUPPORTED_LANGUAGES.keys()),
                value="English",
                label="Target Language",
                info="Select the language of the text you entered."
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

            # 🛡️ Mandatory Consent Checkbox
            consent_checkbox = gr.Checkbox(
                label="I confirm I have the right to use this voice and consent to it being processed.",
                value=False
            )

            # 🚀 Colored button
            generate_btn = gr.Button("Generate Voice", variant="primary")

            # 🧹 Clear button (clears inputs, sliders, checkbox, and dropdown)
            clear_btn = gr.ClearButton(
                components=[text_input, audio_input, language_dropdown, speed_slider, pitch_slider, consent_checkbox],
                value="🧹 Clear Input"
            )

        with gr.Column():
            output_audio = gr.Audio(label="Generated Voice")

            download_btn = gr.File(label="⬇ Download Audio")

            status = gr.Textbox(label="Status")

    # ADDED: language_dropdown to the inputs array so it passes the 6th argument to process()
    generate_btn.click(
        fn=process,
        inputs=[text_input, audio_input, speed_slider, pitch_slider, consent_checkbox, language_dropdown],
        outputs=[output_audio, download_btn, status],
        show_progress=True
    )

if __name__ == "__main__":
    demo.launch()
