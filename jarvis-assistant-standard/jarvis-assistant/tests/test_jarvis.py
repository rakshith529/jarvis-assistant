"""
tests/test_jarvis.py - Unit tests for JARVIS core logic.

Run with:
    pytest
"""

import pytest
from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# ask_jarvis
# ---------------------------------------------------------------------------

class TestAskJarvis:
    """Tests for the ask_jarvis() function."""

    def test_returns_string_on_success(self):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Hello, I am JARVIS."

        with patch("src.jarvis.client") as mock_client:
            mock_client.api_key = "fake-key"
            mock_client.chat.completions.create.return_value = mock_response

            from src.jarvis import ask_jarvis
            result = ask_jarvis("Say hello")

        assert result == "Hello, I am JARVIS."

    def test_raises_when_api_key_missing(self):
        with patch("src.jarvis.client") as mock_client:
            mock_client.api_key = None

            from src.jarvis import ask_jarvis
            with pytest.raises(ValueError, match="OPENROUTER_API_KEY"):
                ask_jarvis("Hello")


# ---------------------------------------------------------------------------
# listen
# ---------------------------------------------------------------------------

class TestListen:
    """Tests for the listen() function."""

    def test_returns_recognised_text(self):
        with (
            patch("src.jarvis.sr.Microphone"),
            patch("src.jarvis._recognizer") as mock_rec,
        ):
            mock_rec.listen.return_value = MagicMock()
            mock_rec.recognize_google.return_value = "what time is it"

            from src.jarvis import listen
            result = listen()

        assert result == "what time is it"

    def test_returns_error_string_on_unknown_value(self):
        import speech_recognition as sr

        with (
            patch("src.jarvis.sr.Microphone"),
            patch("src.jarvis._recognizer") as mock_rec,
        ):
            mock_rec.listen.return_value = MagicMock()
            mock_rec.recognize_google.side_effect = sr.UnknownValueError()

            from src.jarvis import listen
            result = listen()

        assert "didn't catch" in result.lower()
