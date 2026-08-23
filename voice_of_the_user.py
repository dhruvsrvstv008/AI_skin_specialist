import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


load_dotenv(Path(__file__).parent / ".env")


def speech_to_text(audio_filepath):
    """
    Convert the audio file received from Gradio
    into text using Groq Whisper.
    """

    if not audio_filepath:
        raise ValueError("No patient voice was provided.")

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set.")

    client = Groq(api_key=api_key)

    print("\n🧠 Transcribing patient's voice with Groq Whisper...")

    with open(audio_filepath, "rb") as audio_file:

        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model=os.environ.get(
                "WHISPER_MODEL",
                "whisper-large-v3"
            )
        )

    patient_text = transcription.text

    print("\n========================================")
    print("PATIENT'S TRANSCRIPTION")
    print("========================================")
    print(patient_text)
    print("========================================")

    return patient_text


if __name__ == "__main__":
    print(
        "This file is designed to receive an audio file "
        "from Gradio."
    )
