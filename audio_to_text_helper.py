import json
from pathlib import Path
from groq import Groq
import streamlit as st

GROQ_API = st.secrets["GROQ_API"]
client = Groq(api_key=GROQ_API)


def transcribe_audio_with_groq(audio_file_path: str, prompt: str = "IT conversations. Mexican speaker") -> dict:
    """
    Transcribe an audio file using Groq's Whisper model.
    
    Parameters:
        audio_file_path (str): Path to the audio file (.m4a, .mp3, etc.)
        prompt (str): Optional prompt to guide the transcription

    Returns:
        dict: Transcription response as a dictionary, or raises exception on failure.
    """

    
    # --- Validate file path ---
    audio_path = Path(audio_file_path)
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    # --- Transcribe ---
    try:
        with audio_path.open("rb") as file:
            response = client.audio.transcriptions.create(
                file=file,
                model="whisper-large-v3-turbo",
                prompt=prompt,
                response_format="verbose_json",
                timestamp_granularities=["word", "segment"],
                language="en",
                temperature=0.0,
            )
            return response.text
    except Exception as e:
        raise RuntimeError(f"Error during transcription: {e}")


