"""
LolCoach - AI Voice Coach for League of Legends
================================================
Hands-free, Vanguard-safe coaching assistant.

Usage:
    python main.py

Say "Computer" for a quick general tip.
Say "Jarvis" followed by a question for specific advice.
"""

import threading
import signal
import sys

from config import validate_keys
from wake_word import WakeWordListener
from screen_capture import capture_screen
from audio_recorder import record_question
from stt import transcribe
from ai_coach import get_general_tip, answer_question
from tts import play_beep, speak


def handle_general_tip():
    """
    Flow 1: "Computer" detected.
    Screenshot -> Gemini -> TTS -> Play audio.
    """

    def _process():
        try:
            play_beep("general")
            print("[FLOW] Capturando tela...")
            screenshot = capture_screen()
            print("[FLOW] Enviando para Gemini...")
            tip = get_general_tip(screenshot)
            print("[FLOW] Gerando áudio...")
            speak(tip)
            print("[FLOW] Dica reproduzida com sucesso.")
        except Exception as e:
            print(f"[ERRO] Falha no fluxo de dica geral: {e}")

    thread = threading.Thread(target=_process, daemon=True)
    thread.start()


def handle_question():
    """
    Flow 2: "Jarvis" detected.
    Beep -> Record question -> Screenshot -> Whisper STT -> Gemini -> TTS -> Play.
    """

    def _process():
        try:
            play_beep("question")

            # Record the player's question
            print("[FLOW] Gravando pergunta...")
            audio_bytes = record_question()

            # Capture screen right after recording
            print("[FLOW] Capturando tela...")
            screenshot = capture_screen()

            # Transcribe the question
            print("[FLOW] Transcrevendo áudio...")
            question_text = transcribe(audio_bytes)

            if not question_text:
                print("[FLOW] Nenhuma pergunta detectada, ignorando.")
                return

            # Send screenshot + question to Gemini
            print("[FLOW] Enviando para Gemini...")
            answer_text = answer_question(screenshot, question_text)

            # Convert answer to speech and play
            print("[FLOW] Gerando áudio da resposta...")
            speak(answer_text)
            print("[FLOW] Resposta reproduzida com sucesso.")
        except Exception as e:
            print(f"[ERRO] Falha no fluxo de pergunta: {e}")

    thread = threading.Thread(target=_process, daemon=True)
    thread.start()


def main():
    print("=" * 55)
    print("  LolCoach - AI Voice Coach para League of Legends")
    print("=" * 55)
    print()

    # Validate API keys before starting
    validate_keys()

    # Create the wake word listener
    listener = WakeWordListener(
        on_general_tip=handle_general_tip,
        on_question=handle_question,
    )

    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print("\n[EXIT] Encerrando LolCoach...")
        listener.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    print('  Diga "Computer" para uma dica rápida.')
    print('  Diga "Jarvis" + sua pergunta para análise específica.')
    print("  Pressione Ctrl+C para sair.")
    print()

    # Start the blocking listen loop
    listener.listen()


if __name__ == "__main__":
    main()
