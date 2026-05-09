import speech_recognition as sr
import pyttsx3
from openai import OpenAI

# OpenRouter client
client = OpenAI(
    api_key="your key",
    base_url="https://openrouter.ai/api/v1"
)

engine = pyttsx3.init()
recognizer = sr.Recognizer()


def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except:
        return "Sorry, I didn't catch that."


def ask_jarvis(prompt):
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are JARVIS, a helpful AI assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    speak("JARVIS online. How can I help you?")

    while True:
        user_input = listen()

        if "exit" in user_input.lower():
            speak("Goodbye!")
            break

        reply = ask_jarvis(user_input)
        print("JARVIS:", reply)
        speak(reply)