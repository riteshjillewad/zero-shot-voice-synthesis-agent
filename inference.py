# inference.py

import os
import uuid
import re
import soundfile as sf
import numpy as np
from models.tts_model import get_tts_model
from config import OUTPUT_DIR
from utils.audio_utils import modify_audio

def split_text_into_chunks(text):
    """
    Splits a large block of text into individual sentences.
    Uses RegEx to look for periods, exclamation marks, or question marks 
    followed by a space, keeping the punctuation attached to the sentence.
    """
    # Split by punctuation (. ! ?)
    chunks = re.split(r'(?<=[.!?]) +', text.strip())
    
    # Filter out any empty strings or purely whitespace chunks
    return [chunk.strip() for chunk in chunks if chunk.strip()]

def generate_voice(text, speaker_wav, speed=1.0, pitch=0.0, lang_code="en"):

    # Ensure valid language
    if not lang_code:
        lang_code = "en"

    tts = get_tts_model()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 1. Split the text into manageable chunks
    chunks = split_text_into_chunks(text)
    chunk_files = []
    
    # 2. Generate temporary audio for each chunk
    for i, chunk in enumerate(chunks):
        # Skip chunks that are too small (e.g., a stray punctuation mark)
        if len(chunk) < 2: 
            continue
            
        # Create a unique temporary filename for this specific chunk
        temp_filename = os.path.join(OUTPUT_DIR, f"temp_{uuid.uuid4().hex}_{i}.wav")
        
        tts.tts_to_file(
            text=chunk,
            speaker_wav=speaker_wav,
            language=lang_code,
            file_path=temp_filename
        )
        chunk_files.append(temp_filename)
        
    # 3. Read and concatenate all chunk audio arrays
    combined_audio = []
    sample_rate = None
    
    for file in chunk_files:
        # Read the raw float32 audio data from the temp file
        audio_data, sr = sf.read(file)
        combined_audio.append(audio_data)
        sample_rate = sr 
        
        # System cleanup: Delete the temp file immediately to save disk space
        os.remove(file)
        
    # 4. Save the combined raw audio
    if not combined_audio:
        raise ValueError("No audio was generated. Please ensure your text contains valid sentences.")
        
    unique_filename = f"voice_{uuid.uuid4().hex}.wav"
    raw_output_path = os.path.join(OUTPUT_DIR, unique_filename)
    
    # Use numpy to stitch all the audio data arrays together seamlessly
    final_audio = np.concatenate(combined_audio)
    sf.write(raw_output_path, final_audio, sample_rate)

    # 5. Apply speed and pitch modifications to the final concatenated file
    final_output_path = modify_audio(raw_output_path, speed=speed, pitch_steps=pitch)

    return final_output_path
