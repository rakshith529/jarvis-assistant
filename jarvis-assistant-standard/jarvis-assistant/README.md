# 🤖 JARVIS Voice Assistant

A voice-enabled AI assistant powered by [OpenRouter](https://openrouter.ai) with both a CLI mode and a Streamlit web UI.

---

## Features

- 🎤 **Voice input** via your microphone (Google Speech Recognition)
- 🔊 **Text-to-speech** replies using pyttsx3
- 🌐 **Web UI** built with Streamlit (chat history, no mic required)
- 🔁 **CLI loop** for a fully hands-free terminal experience
- ⚙️ **Configurable** model, system prompt, and API key via `.env`

---

## Project Structure

```
jarvis-assistant/
├── app.py                 # Streamlit web UI entry-point
├── src/
│   ├── __init__.py
│   └── jarvis.py          # Core logic: TTS, STT, AI response
├── tests/
│   ├── __init__.py
│   └── test_jarvis.py     # Unit tests (pytest)
├── .env.example           # Environment variable template
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Quick Start

### 1. Clone & install

```bash
git clone https://github.com/your-username/jarvis-assistant.git
cd jarvis-assistant
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

> **Note – PyAudio on Windows/macOS:**  
> If `pip install pyaudio` fails, install the binary wheel:  
> - Windows: `pip install pipwin && pipwin install pyaudio`  
> - macOS: `brew install portaudio && pip install pyaudio`

### 2. Configure environment

```bash
cp .env.example .env
# Open .env and set OPENROUTER_API_KEY
```

| Variable | Required | Default | Description |
|---|---|---|---|
| `OPENROUTER_API_KEY` | ✅ | — | Your OpenRouter API key |
| `OPENROUTER_MODEL` | ❌ | `openai/gpt-4o-mini` | Any model available on OpenRouter |
| `JARVIS_SYSTEM_PROMPT` | ❌ | Built-in | Custom system prompt |

### 3. Run

**Web UI (recommended)**
```bash
streamlit run app.py
```

**CLI voice loop**
```bash
python -m src.jarvis
```

---

## Running Tests

```bash
pip install pytest
pytest tests/ -v
```

---

## Security Notes

- **Never** commit your `.env` file — it is listed in `.gitignore`.
- Rotate your API key immediately if you believe it has been exposed.
- The `.env.example` file is safe to commit; it contains no real secrets.

---

## License

MIT
