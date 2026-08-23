

import os
import platform
import subprocess
from pathlib import Path

from dotenv import load_dotenv
from deepgram import DeepgramClient


# ============================================================
# STEP 1: Load environment variables
# ============================================================

folder = Path(__file__).parent
env_path = folder / ".env"

load_dotenv(env_path)

api_key = os.environ.get("DEEPGRAM_API_KEY")

if not api_key:
    raise ValueError("Missing DEEPGRAM_API_KEY in .env")


# ============================================================
# STEP 2: Create Deepgram client
# ============================================================

deepgram = DeepgramClient(api_key=api_key)


# ============================================================
# STEP 3: Text to Speech function
# ============================================================

def text_to_speech(
    text,
    output_filename="test-output.mp3"
):
    """
    Convert text into speech using Deepgram
    and save the audio as an MP3 file.
    """

    if not text:
        raise ValueError("Text cannot be empty.")

    text = text[:2000]

    audio = deepgram.speak.v1.audio.generate(
        text=text,
        model="aura-2-thalia-en",
        encoding="mp3",
    )

    audio_path = folder / output_filename

    with audio_path.open("wb") as file:
        for chunk in audio:
            file.write(chunk)

    print(f"Audio saved successfully: {audio_path}")

    return audio_path


# ============================================================
# STEP 4: Play audio function
# ============================================================

def play_audio(audio_path):
    """
    Play the generated audio file
    according to the operating system.
    """

    system = platform.system()

    if system == "Darwin":
        # macOS
        subprocess.run(
            ["afplay", str(audio_path)]
        )

    elif system == "Windows":
        # Windows
        os.startfile(audio_path)

    else:
        # Linux
        subprocess.run(
            ["xdg-open", str(audio_path)]
        )


# ============================================================
# STEP 5: Test the functions
# ============================================================

if __name__ == "__main__":

    text = (
        "Hi, my name is Whisperer. "
        "How can I help you today?"
    )

    audio_path = text_to_speech(
        text=text,
        output_filename="test-output.mp3"
    )

    play_audio(audio_path)


'''
import os
from pathlib import Path

from dotenv import load_dotenv
from deepgram import DeepgramClient


# Step 1: Load environment variables

load_dotenv()

api_key = os.environ.get("DEEPGRAM_API_KEY")

if not api_key:
    raise ValueError("Missing DEEPGRAM_API_KEY in .env")


# Step 2: Create Deepgram client

deepgram = DeepgramClient(api_key=api_key)


# Step 3: Text to Speech

text = "Hi, my name is Whisperer. How can I help you today?"

audio = deepgram.speak.v1.audio.generate(
    text=text,
    model="aura-2-thalia-en",
    encoding="mp3",
)


# Step 4: Save audio

audio_file = "test-output.mp3"
audio_path = Path(__file__).with_name(audio_file)

with audio_path.open("wb") as file:
    for chunk in audio:
        file.write(chunk)


print(f"Audio saved successfully: {audio_path}")



# Step5: Play audio
import platform
import subprocess

if platform.system() == "Darwin":  # macOS
    subprocess.run(["afplay", str(audio_path)])
elif platform.system() == "Windows":
    os.startfile(audio_path)
else:  # Linux
    subprocess.run(["xdg-open", str(audio_path)])


'''