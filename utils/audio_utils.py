# utils/audio_utils.py

import librosa
import soundfile as sf
import numpy as np

def modify_audio(file_path, speed=1.0, pitch_steps=0):
    if speed == 1.0 and pitch_steps == 0:
        return file_path

    # Load the generated audio
    y, sr = librosa.load(file_path, sr=None)

    # 🛠️ THE FIX: Force the array to float64 to prevent the Numpy crash
    y = y.astype(np.float64)

    # 1. Apply Time Stretch (Speed)
    if speed != 1.0:
        y = librosa.effects.time_stretch(y, rate=speed)

    # 2. Apply Pitch Shift
    if pitch_steps != 0:
        y = librosa.effects.pitch_shift(y, sr=sr, n_steps=pitch_steps)

    # 🛠️ Cast it back to standard float32 for saving
    y = y.astype(np.float32)

    # Save the modified audio
    modified_path = file_path.replace(".wav", "_modified.wav")
    sf.write(modified_path, y, sr)

    return modified_path
