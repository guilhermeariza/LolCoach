"""
Wake word detection module - uses Picovoice Porcupine for offline keyword spotting.
Listens continuously on the microphone and triggers callbacks.
"""

import struct

import pvporcupine
import pyaudio

from config import PICOVOICE_ACCESS_KEY, WAKE_WORD_GENERAL, WAKE_WORD_QUESTION


class WakeWordListener:
    """
    Continuously listens for wake words using Porcupine.
    Calls the appropriate callback when a keyword is detected.
    """

    def __init__(self, on_general_tip, on_question):
        """
        Args:
            on_general_tip: callable invoked when WAKE_WORD_GENERAL is detected.
            on_question: callable invoked when WAKE_WORD_QUESTION is detected.
        """
        self.on_general_tip = on_general_tip
        self.on_question = on_question
        self._running = False

        self._porcupine = pvporcupine.create(
            access_key=PICOVOICE_ACCESS_KEY,
            keywords=[WAKE_WORD_GENERAL, WAKE_WORD_QUESTION],
            sensitivities=[0.6, 0.6],
        )

        self._pa = pyaudio.PyAudio()
        self._stream = self._pa.open(
            rate=self._porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self._porcupine.frame_length,
        )

    def listen(self):
        """
        Blocking loop that listens for wake words until stop() is called.
        """
        self._running = True
        print("[WAKE] Escutando wake words... (Diga 'Computer' ou 'Jarvis')")

        while self._running:
            try:
                pcm = self._stream.read(
                    self._porcupine.frame_length, exception_on_overflow=False
                )
                pcm_unpacked = struct.unpack_from(
                    "h" * self._porcupine.frame_length, pcm
                )

                keyword_index = self._porcupine.process(pcm_unpacked)

                if keyword_index == 0:
                    print(f'[WAKE] Detectado: "{WAKE_WORD_GENERAL}"')
                    self.on_general_tip()
                elif keyword_index == 1:
                    print(f'[WAKE] Detectado: "{WAKE_WORD_QUESTION}"')
                    self.on_question()

            except Exception as e:
                if self._running:
                    print(f"[WAKE] Erro no loop de escuta: {e}")

    def stop(self):
        """Stop listening and release resources."""
        self._running = False
        if self._stream is not None:
            self._stream.close()
        if self._pa is not None:
            self._pa.terminate()
        if self._porcupine is not None:
            self._porcupine.delete()
        print("[WAKE] Listener encerrado.")
