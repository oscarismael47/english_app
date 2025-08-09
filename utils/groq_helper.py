import json
from pathlib import Path
from groq import Groq
import streamlit as st



class GroqHandler:
    """
    A handler class for interacting with Groq's Speech-to-Text and Text-to-Speech APIs.
    """

    def __init__(self, api_key: str = None):
        """
        Initialize GroqHandler with API key.

        Parameters:
            api_key (str): Groq API key. If None, will try to use Streamlit secrets.
        """
        if api_key is None:
            api_key = st.secrets.get("GROQ_KEY")
        if not api_key:
            raise ValueError("Groq API key not provided and not found in Streamlit secrets.")

        self.client = Groq(api_key=api_key)

    def speech_to_text(
        self,
        audio_file_path: str,
        prompt: str = "IT conversations. Mexican speaker",
        language: str = "en"
    ) -> dict:
        """
        Transcribe an audio file using Groq's Whisper model.

        Parameters:
            audio_file_path (str): Path to the audio file (.m4a, .mp3, etc.)
            prompt (str): Optional prompt to guide the transcription.
            language (str): Language code for transcription.

        Returns:
            dict: Transcription result as dictionary.
        """
        audio_path = Path(audio_file_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        try:
            with audio_path.open("rb") as file:
                response = self.client.audio.transcriptions.create(
                    file=file,
                    model="whisper-large-v3-turbo",
                    prompt=prompt,
                    response_format="verbose_json",
                    timestamp_granularities=["word", "segment"],
                    language=language,
                    temperature=0.0,
                )
                return response.text
        except Exception as e:
            raise RuntimeError(f"Error during transcription: {e}")

    def text_to_speech(
        self,
        text: str,
        output_path: str = "speech.wav",
        model: str = "playai-tts",
        voice: str = "Fritz-PlayAI",
        response_format: str = "wav"
    ) -> Path:
        """
        Convert text into speech using Groq's TTS model.

        Parameters:
            text (str): The text to convert into speech.
            output_path (str): Path where the output audio will be saved.
            model (str): TTS model to use.
            voice (str): Voice name to use.
            response_format (str): Audio format ("wav", "mp3", etc.).

        Returns:
            Path: Path to the generated speech file.
        """
        try:
            response = self.client.audio.speech.create(
                model=model,
                voice=voice,
                input=text,
                response_format=response_format
            )
            output_file = Path(output_path)
            response.write_to_file(output_file)
            return output_file
        except Exception as e:
            raise RuntimeError(f"Error during text-to-speech: {e}")



if __name__ == "__main__":
    groq_handler = GroqHandler()

    # --- Speech to Text ---
    transcription = groq_handler.speech_to_text(r"D:\python_scripts\git_repo\english_app\generated_audio\audio_20250808_114623.mp3")
    print("Transcription:", transcription)

    # --- Text to Speech ---
    tts_path = groq_handler.text_to_speech("Hello! This is a test.")
    print(f"TTS file saved at: {tts_path}")
