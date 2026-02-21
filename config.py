"""
Configuration module - loads environment variables and defines constants.
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv()

# --- API Keys ---
PICOVOICE_ACCESS_KEY = os.getenv("PICOVOICE_ACCESS_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# --- Wake Words ---
# Built-in Porcupine keywords (free tier)
WAKE_WORD_GENERAL = "computer"
WAKE_WORD_QUESTION = "jarvis"

# --- Audio Recording ---
RECORD_SECONDS = 6  # Duration to record after "Jarvis" wake word
SAMPLE_RATE = 16000  # 16kHz for Whisper compatibility

# --- Gemini ---
GEMINI_MODEL = "gemini-2.5-flash"
SYSTEM_PROMPT = (
    "Você é um técnico Challenger de League of Legends focado em macro gaming "
    "e tomada de decisão rápida. Você receberá imagens da tela do jogador. "
    "Suas respostas devem ser extremamente curtas, diretas e no idioma "
    "Português (Brasil). Não explique o porquê detalhadamente, apenas diga o "
    "que o jogador deve fazer com base na imagem, minimapa, tempo de jogo e "
    "status dos campeões. Fale como se estivesse na call do Discord com o "
    "jogador durante uma partida."
)

# --- OpenAI TTS ---
TTS_MODEL = "tts-1"
TTS_VOICE = "onyx"  # Deep voice, good for coaching

# --- Paths ---
SOUNDS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds")


def validate_keys():
    """Check that all required API keys are set."""
    missing = []
    if not PICOVOICE_ACCESS_KEY:
        missing.append("PICOVOICE_ACCESS_KEY")
    if not GEMINI_API_KEY:
        missing.append("GEMINI_API_KEY")
    if not OPENAI_API_KEY:
        missing.append("OPENAI_API_KEY")

    if missing:
        print(f"[ERRO] Chaves de API faltando no .env: {', '.join(missing)}")
        print("Consulte o README.md para instruções de configuração.")
        sys.exit(1)
