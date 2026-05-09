"""
app.py - Streamlit web interface for JARVIS Voice Assistant.

Run with:
    streamlit run app.py
"""

import streamlit as st
from src.jarvis import ask_jarvis, speak

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="JARVIS Assistant",
    page_icon="🤖",
    layout="centered",
)

# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

st.title("🤖 JARVIS Voice Assistant")
st.markdown(
    "Powered by [OpenRouter](https://openrouter.ai) · "
    "Type a question and let JARVIS respond."
)
st.divider()

# Chat history stored in session state so it persists across reruns
if "messages" not in st.session_state:
    st.session_state.messages: list[dict] = []

# Render existing conversation
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input area
user_input = st.chat_input("Ask JARVIS …")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get & show JARVIS reply
    with st.chat_message("assistant"):
        with st.spinner("Thinking …"):
            try:
                reply = ask_jarvis(user_input)
            except ValueError as exc:
                reply = f"⚠️ Configuration error: {exc}"
            except Exception as exc:  # noqa: BLE001
                reply = f"⚠️ Unexpected error: {exc}"

        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

    # Speak the reply (non-blocking best-effort)
    try:
        speak(reply)
    except Exception:  # noqa: BLE001
        pass  # TTS is optional in a web context
