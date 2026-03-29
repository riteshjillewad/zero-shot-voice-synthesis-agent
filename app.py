######################################################################################################
## Name:        app.py
## Description: Project source code
## Date:        29-03-2026
## Author:      Ritesh Jillewad
######################################################################################################


# Importing important libraries
import gradio as gr
import os
import shutil
from inference import generate_voice


# Voice profies
VOICE_DIR = "voice_profiles"


# Language dictionary
SUPPORTED_LANGUAGES = {
    "English": "en", "Hindi": "hi", "French": "fr", "German": "de",
    "Spanish": "es", "Italian": "it"
}


# Processing logic
def process(text, audio, consent_given, language_name, selected_profile, save_name):

    # Security check
    if not consent_given:
        return None, None, "Consent required"

    # Basic input validation
    if not text:
        return None, None, "Enter text"

    lang_code = SUPPORTED_LANGUAGES.get(language_name, "en")

    # Select voice
    if selected_profile != "Upload New":
        profile_path = os.path.join(VOICE_DIR, selected_profile)
    else:
        if not audio:
            return None, None, "Upload voice"

        profile_path = audio

        # Save user voice
        if save_name:
            save_path = os.path.join(VOICE_DIR, "user", f"{save_name}.wav")
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            shutil.copy(audio, save_path)

    try:
        output_path = generate_voice(
            text=text,
            speaker_wav=profile_path,
            lang_code=lang_code
        )
        return output_path, output_path, "Voice generated!"

    except Exception as e:
        return None, None, f"Error: {str(e)}"


# UI logic
with gr.Blocks() as demo:

    gr.Markdown("# 🎤 VoxAgent - Voice Cloning System")

    with gr.Row():

        with gr.Column():
            text_input = gr.Textbox(label="Enter Text", lines=4)

            audio_input = gr.Audio(type="filepath", label="Upload Voice")

            language_dropdown = gr.Dropdown(
                choices=list(SUPPORTED_LANGUAGES.keys()),
                value="English",
                label="Language"
            )

            profile_dropdown = gr.Dropdown(
                choices=[
                    "predefined/male.wav",
                    "predefined/female.wav",
                    "predefined/child.wav",
                    "Upload New"
                ],
                value="Upload New",
                label="🎤 Voice Profile"
            )

            save_name_input = gr.Textbox(
                label="Save Voice As (optional)"
            )

            consent_checkbox = gr.Checkbox(label="I confirm I have rights to use this voice")

            generate_btn = gr.Button("Generate Voice", variant="primary")

            clear_btn = gr.ClearButton(
                [text_input, audio_input, save_name_input]
            )

        with gr.Column():
            output_audio = gr.Audio(label="Output")

            download_btn = gr.File(label="Download")

            status = gr.Textbox(label="Status")

    generate_btn.click(
        fn=process,
        inputs=[
            text_input,
            audio_input,
            consent_checkbox,
            language_dropdown,
            profile_dropdown,
            save_name_input
        ],
        outputs=[output_audio, download_btn, status],
        show_progress=True
    )

demo.launch(theme=gr.themes.Soft())
