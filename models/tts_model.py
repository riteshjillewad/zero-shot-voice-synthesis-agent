# models/tts_model.py

from TTS.api import TTS
from config import MODEL_NAME

# Load model globally (so it doesn't reload every time)
tts_model = TTS(model_name=MODEL_NAME)

def get_tts_model():
    return tts_model
