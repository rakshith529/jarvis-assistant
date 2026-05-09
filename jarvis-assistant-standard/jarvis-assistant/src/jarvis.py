"""
jarvis.py - Core logic for JARVIS Voice Assistant.

Handles:
- Text-to-speech (pyttsx3)
- Speech recognition (SpeechRecognition + Google STT)
- AI response generation via OpenRouter API
"""

import os
import speech_recognition as sr
import pyttsx3
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Clients & engines
# ---------------------------------------------------------------------------

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

_engine = pyttsx3.init()
_recognizer = sr.Recognizer()

SYSTEM_PROMPT = os.getenv(
    "JARVIS_SYSTEM_PROMPT",
    "You are JARVIS, a concise and helpful AI assistant.",
)
MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")


# ---------------------------------------------------------------------------
# Speech utilities
# ---------------------------------------------------------------------------

def speak(text: str) -> None:
    """Convert *text* to speech using the local TTS engine."""
    _engine.say(text)
    _engine.runAndWait()


def listen(timeout: int = 5) -> str:
    """
    Capture audio from the default microphone and transcribe it.

    Returns the recognised string, or an error message on failure.
    """
    with sr.Microphone() as source:
        print("🎤  Listening …")
        _recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = _recognizer.listen(source, timeout=timeout)
        except sr.WaitTimeoutError:
            return "I didn't hear anything."

    try:
        text = _recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        return "Sorry, I didn't catch that."
    except sr.RequestError as exc:
        return f"Speech recognition service error: {exc}"


# ---------------------------------------------------------------------------
# AI response
# ---------------------------------------------------------------------------

def ask_jarvis(prompt: str) -> str:
    """
    Send *prompt* to the configured model and return the assistant reply.

    Raises ``ValueError`` if OPENROUTER_API_KEY is not set.
    """
    if not client.api_key:
        raise ValueError(
            "OPENROUTER_API_KEY is not set. "
            "Add it to your .env file or environment."
        )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": prompt},
        ],
    )
    return response.choices[0].message.content


# ---------------------------------------------------------------------------
# CLI entry-point
# ---------------------------------------------------------------------------

def main() -> None:
    """Run JARVIS in a voice-driven REPL loop."""
    speak("JARVIS online. How can I help you?")
    print('Say "exit" or "quit" to stop.\n')

    while True:
        user_input = listen()

        if not user_input:
            continue

        if any(word in user_input.lower() for word in ("exit", "quit", "bye")):
            speak("Goodbye!")
            break

        try:
            reply = ask_jarvis(user_input)
        except Exception as exc:  # noqa: BLE001
            reply = f"I encountered an error: {exc}"

        print(f"JARVIS: {reply}\n")
        speak(reply)


if __name__ == "__main__":
    main()
