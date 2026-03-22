# inference.py

import os
from models.tts_model import get_tts_model
from config import OUTPUT_AUDIO_PATH

def generate_voice(text, speaker_wav):
    tts = get_tts_model()

    tts.tts_to_file(
        text=text,
        speaker_wav=speaker_wav,
        language="en",   # IMPORTANT
        file_path="output/output.wav"
    )

    return "output/output.wav"