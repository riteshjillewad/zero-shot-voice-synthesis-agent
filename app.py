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
from utils.moderation import is_safe_text   # 🔥 Added Hybrid Safety System

# Voice profiles directory
VOICE_DIR = "voice_profiles"

# Language dictionary
SUPPORTED_LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Italian": "it"
}

# 🔹 Load voice profiles dynamically
def load_voice_profiles():
    profiles = []

    predefined_path = os.path.join(VOICE_DIR, "predefined")
    if os.path.exists(predefined_path):
        for f in os.listdir(predefined_path):
            if f.endswith(".wav"):
                profiles.append(f"predefined/{f}")

    user_path = os.path.join(VOICE_DIR, "user")
    if os.path.exists(user_path):
        for f in os.listdir(user_path):
            if f.endswith(".wav"):
                profiles.append(f"user/{f}")

    return profiles


# 🔹 Load history
def load_history():
    history = []
    output_dir = "output"

    if os.path.exists(output_dir):
        files = sorted(os.listdir(output_dir), reverse=True)
        for f in files:
            if f.endswith(".wav"):
                history.append(os.path.join(output_dir, f))

    return history


# 🔹 Processing logic
def process(text, audio, consent_given, language_name, selected_profile, save_name):

    # Consent Check
    if not consent_given:
        return None, None, "❌ Consent required", gr.update()

    # Text Validation
    if not text:
        return None, None, "❌ Enter text", gr.update()

    # 🔥 Hybrid Safety Moderation Check
    safe, msg = is_safe_text(text)

    if not safe:
        return None, None, f"❌ {msg}", gr.update()

    lang_code = SUPPORTED_LANGUAGES.get(language_name, "en")

    # 🎤 Voice selection
    if selected_profile != "Upload New":
        profile_path = os.path.join(VOICE_DIR, selected_profile)

    else:
        if not audio:
            return None, None, "❌ Upload voice", gr.update()

        profile_path = audio

        # 💾 Save user voice
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

        # Refresh history dropdown
        new_history = load_history()

        return (
            output_path,
            output_path,
            "✅ Voice generated!",
            gr.update(choices=new_history, value=output_path)
        )

    except Exception as e:
        return None, None, f"❌ Error: {str(e)}", gr.update()


# 🎨 UI
with gr.Blocks(analytics_enabled=False) as demo:

    # Header
    gr.Markdown("""
    <h1 style='text-align: center;'>🎤 VoxAgent</h1>
    <p style='text-align: center;'>AI Voice Cloning & Multilingual Speech System</p>
    """)

    with gr.Row():

        # 📌 SIDEBAR
        with gr.Column(scale=1, min_width=300):

            gr.Markdown("## ⚙️ Controls")

            text_input = gr.Textbox(label="📝 Enter Text", lines=4)

            audio_input = gr.Audio(type="filepath", label="🎧 Upload Voice")

            language_dropdown = gr.Dropdown(
                choices=list(SUPPORTED_LANGUAGES.keys()),
                value="English",
                label="🌍 Language"
            )

            profile_dropdown = gr.Dropdown(
                choices=load_voice_profiles() + ["Upload New"],
                value="Upload New",
                label="🎤 Voice Profile"
            )

            save_name_input = gr.Textbox(label="💾 Save Voice As")

            consent_checkbox = gr.Checkbox(
                label="I confirm I have rights to use this voice"
            )

            generate_btn = gr.Button("🚀 Generate Voice", variant="primary")

            clear_btn = gr.Button("🧹 Clear")

        # 📊 MAIN PANEL
        with gr.Column(scale=2):

            with gr.Tabs():

                # 🔊 OUTPUT TAB
                with gr.Tab("🔊 Output"):
                    output_audio = gr.Audio(label="Generated Audio")
                    download_btn = gr.File(label="⬇️ Download")
                    status = gr.Textbox(label="Status")

                # 📜 HISTORY TAB
                with gr.Tab("📜 History"):
                    history_list = gr.Dropdown(
                        choices=load_history(),
                        label="Select Previous Audio"
                    )
                    history_audio = gr.Audio(label="▶️ Play Selected")

    # 🧹 Clear function
    def clear_all():
        return "", None, "", "Upload New", "", False

    clear_btn.click(
        fn=clear_all,
        inputs=[],
        outputs=[
            text_input,
            audio_input,
            save_name_input,
            profile_dropdown,
            status,
            consent_checkbox
        ]
    )

    # 🎧 History playback
    def load_selected_audio(file_path):
        return file_path

    history_list.change(
        fn=load_selected_audio,
        inputs=history_list,
        outputs=history_audio
    )

    # 🚀 Generate
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
        outputs=[output_audio, download_btn, status, history_list],
        show_progress=True
    )

# Launch
demo.launch(theme=gr.themes.Soft())
