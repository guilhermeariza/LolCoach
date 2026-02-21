"""
TTS and audio playback module.
Uses OpenAI TTS API for speech synthesis and pygame for playback.
"""

import io
import os
import tempfile

import pygame
from openai import OpenAI

from config import OPENAI_API_KEY, TTS_MODEL, TTS_VOICE, SOUNDS_DIR

_client = None
_mixer_initialized = False


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client


def _ensure_mixer():
    global _mixer_initialized
    if not _mixer_initialized:
        pygame.mixer.init(frequency=24000, size=-16, channels=1)
        _mixer_initialized = True


def play_beep(beep_name: str):
    """
    Play a short feedback beep sound.
    beep_name: 'general' or 'question'
    """
    _ensure_mixer()
    beep_path = os.path.join(SOUNDS_DIR, f"beep_{beep_name}.wav")
    if not os.path.exists(beep_path):
        print(f"[AUDIO] Arquivo de beep não encontrado: {beep_path}")
        return
    try:
        sound = pygame.mixer.Sound(beep_path)
        sound.play()
        pygame.time.wait(int(sound.get_length() * 1000) + 50)
    except Exception as e:
        print(f"[AUDIO] Erro ao tocar beep: {e}")


def speak(text: str):
    """
    Convert text to speech using OpenAI TTS and play it through pygame.
    """
    _ensure_mixer()
    client = _get_client()

    response = client.audio.speech.create(
        model=TTS_MODEL,
        voice=TTS_VOICE,
        input=text,
        response_format="mp3",
    )

    # Write to a temp file for pygame playback
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp.write(response.content)
        tmp_path = tmp.name

    try:
        pygame.mixer.music.load(tmp_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
    finally:
        pygame.mixer.music.unload()
        os.unlink(tmp_path)
