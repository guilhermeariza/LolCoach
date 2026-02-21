"""
Utility script to generate simple beep WAV files for audio feedback.
Run once: python generate_beeps.py
"""

import os
import struct
import wave
import math

SOUNDS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds")


def generate_beep(filename: str, freq: float, duration: float, volume: float = 0.5):
    """Generate a simple sine-wave beep and save as WAV."""
    sample_rate = 44100
    n_samples = int(sample_rate * duration)

    os.makedirs(SOUNDS_DIR, exist_ok=True)
    filepath = os.path.join(SOUNDS_DIR, filename)

    with wave.open(filepath, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)

        for i in range(n_samples):
            t = i / sample_rate
            # Apply a short fade-in/fade-out to avoid clicks
            envelope = 1.0
            fade_samples = int(0.01 * sample_rate)
            if i < fade_samples:
                envelope = i / fade_samples
            elif i > n_samples - fade_samples:
                envelope = (n_samples - i) / fade_samples

            sample = volume * envelope * math.sin(2.0 * math.pi * freq * t)
            wf.writeframes(struct.pack("<h", int(sample * 32767)))

    print(f"[OK] Gerado: {filepath}")


if __name__ == "__main__":
    # General tip beep: short, higher pitch (friendly "ding")
    generate_beep("beep_general.wav", freq=880.0, duration=0.15, volume=0.4)

    # Question beep: two-tone, lower pitch (acknowledging "boop-boop")
    # We generate two short beeps concatenated
    sample_rate = 44100
    os.makedirs(SOUNDS_DIR, exist_ok=True)
    filepath = os.path.join(SOUNDS_DIR, "beep_question.wav")

    with wave.open(filepath, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)

        for tone_freq in [660.0, 880.0]:
            tone_duration = 0.1
            n_samples = int(sample_rate * tone_duration)
            fade_samples = int(0.005 * sample_rate)
            for i in range(n_samples):
                t = i / sample_rate
                envelope = 1.0
                if i < fade_samples:
                    envelope = i / fade_samples
                elif i > n_samples - fade_samples:
                    envelope = (n_samples - i) / fade_samples
                sample = 0.4 * envelope * math.sin(2.0 * math.pi * tone_freq * t)
                wf.writeframes(struct.pack("<h", int(sample * 32767)))

            # Small silence gap between tones
            gap_samples = int(sample_rate * 0.05)
            for _ in range(gap_samples):
                wf.writeframes(struct.pack("<h", 0))

    print(f"[OK] Gerado: {filepath}")
    print("\nBeeps gerados com sucesso! Pasta: sounds/")
