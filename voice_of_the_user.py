import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


# ============================================================
# STEP 1: Load environment variables
# ============================================================

folder = Path(__file__).parent
env_path = folder / ".env"

load_dotenv(env_path)

groq_api_key = os.environ.get("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("Missing GROQ_API_KEY in .env")


# ============================================================
# STEP 2: Create Groq client
# ============================================================

client = Groq(api_key=groq_api_key)


# ============================================================
# STEP 3: Speech to Text function
# ============================================================

def speech_to_text(audio_filepath):
    """
    Convert the audio file received from Gradio
    into text using Groq Whisper.
    """

    if not audio_filepath:
        raise ValueError("No patient voice was provided.")

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


# ============================================================
# STEP 4: Test
# ============================================================

if __name__ == "__main__":

    print(
        "This file is designed to receive an audio file "
        "from Gradio."
    )



'''
import logging
import os

import speech_recognition as sr
from dotenv import load_dotenv
from groq import Groq


# ============================================================
# STEP 1: Load environment variables
# ============================================================

load_dotenv()

groq_api_key = os.environ.get("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("Missing GROQ_API_KEY in .env")


# ============================================================
# STEP 2: Create Groq client
# ============================================================

client = Groq(api_key=groq_api_key)


# ============================================================
# STEP 3: Record audio from microphone
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def record_audio(
    file_path,
    timeout=20,
    phrase_time_limit=10
):
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        logging.info("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(
            source,
            duration=1
        )

        logging.info("🎤 Start speaking now...")

        audio_data = recognizer.listen(
            source,
            timeout=timeout,
            phrase_time_limit=phrase_time_limit
        )

        logging.info("Recording complete.")

        # Save recording as WAV
        wav_data = audio_data.get_wav_data()

        with open(file_path, "wb") as audio_file:
            audio_file.write(wav_data)

        logging.info(f"Audio saved to {file_path}")


# ============================================================
# STEP 4: Record patient's voice
# ============================================================

audio_filepath = "patient_voice_test.wav"

record_audio(
    audio_filepath,
    timeout=20,
    phrase_time_limit=10
)


# ============================================================
# STEP 5: Convert speech to text using Groq Whisper
# ============================================================

print("\n🧠 Transcribing with Groq Whisper...")

with open(audio_filepath, "rb") as audio_file:

    transcription = client.audio.transcriptions.create(
        file=audio_file,
        model=os.environ.get(
            "WHISPER_MODEL",
            "whisper-large-v3"
        )
    )


# ============================================================
# STEP 6: Print transcription
# ============================================================

print("\n========================================")
print("PATIENT'S TRANSCRIPTION")
print("========================================")

print(transcription.text)

print("========================================")
'''