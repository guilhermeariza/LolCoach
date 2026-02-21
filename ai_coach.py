"""
AI Coach module - sends screenshots (and optional questions) to Google Gemini.
"""

import google.generativeai as genai

from config import GEMINI_API_KEY, GEMINI_MODEL, SYSTEM_PROMPT

_model = None


def _get_model():
    global _model
    if _model is None:
        genai.configure(api_key=GEMINI_API_KEY)
        _model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            system_instruction=SYSTEM_PROMPT,
        )
    return _model


def get_general_tip(screenshot_png: bytes) -> str:
    """
    Send a screenshot to Gemini and ask for a quick general tip.
    """
    model = _get_model()

    image_part = {
        "mime_type": "image/png",
        "data": screenshot_png,
    }

    response = model.generate_content(
        [
            image_part,
            "Me dê uma dica rápida do que focar agora na partida (máximo 2 frases).",
        ]
    )
    tip = response.text.strip()
    print(f"[GEMINI] Dica: {tip}")
    return tip


def answer_question(screenshot_png: bytes, question: str) -> str:
    """
    Send a screenshot + the player's question to Gemini.
    """
    model = _get_model()

    image_part = {
        "mime_type": "image/png",
        "data": screenshot_png,
    }

    response = model.generate_content(
        [
            image_part,
            f"Pergunta do jogador: {question}",
        ]
    )
    answer = response.text.strip()
    print(f"[GEMINI] Resposta: {answer}")
    return answer
