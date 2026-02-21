"""
Audio recorder module - records microphone input after wake word detection.
Uses sounddevice + scipy for recording.
"""

import io
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav

from config import RECORD_SECONDS, SAMPLE_RATE


def record_question(duration: int = RECORD_SECONDS) -> bytes:
    """
    Record audio from the default microphone for the given duration.
    Returns WAV file bytes ready for the Whisper API.
    """
    print(f"[MIC] Gravando por {duration}s...")
    audio_data = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16",
    )
    sd.wait()  # Block until recording is done
    print("[MIC] Gravação concluída.")

    # Write to in-memory WAV buffer
    buffer = io.BytesIO()
    wav.write(buffer, SAMPLE_RATE, audio_data)
    buffer.seek(0)
    return buffer.read()
