"""
Speech-to-Text module - uses OpenAI Whisper API for transcription.
"""

import io

from openai import OpenAI

from config import OPENAI_API_KEY

_client = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client


def transcribe(audio_bytes: bytes) -> str:
    """
    Send WAV audio bytes to OpenAI Whisper and return the transcribed text.
    """
    client = _get_client()

    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = "question.wav"

    response = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        language="pt",
    )
    text = response.text.strip()
    print(f"[STT] Transcrição: {text}")
    return text
