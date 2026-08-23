import os
import platform
import subprocess
from pathlib import Path

from dotenv import load_dotenv
from deepgram import DeepgramClient


load_dotenv(Path(__file__).parent / ".env")


def text_to_speech(text, output_path=None):
    """
    Convert text into speech using Deepgram and save as an MP3 file.
    Returns the path to the saved file.
    """

    if not text:
        raise ValueError("Text cannot be empty.")

    api_key = os.environ.get("DEEPGRAM_API_KEY")
    if not api_key:
        raise ValueError("DEEPGRAM_API_KEY is not set.")

    deepgram = DeepgramClient(api_key=api_key)

    text = text[:2000]

    audio = deepgram.speak.v1.audio.generate(
        text=text,
        model="aura-2-thalia-en",
        encoding="mp3",
    )

    if output_path is None:
        import tempfile
        tmp = tempfile.NamedTemporaryFile(
            suffix=".mp3", delete=False
        )
        output_path = Path(tmp.name)
        tmp.close()

    output_path = Path(output_path)
    with output_path.open("wb") as file:
        for chunk in audio:
            file.write(chunk)

    print(f"Audio saved successfully: {output_path}")

    return output_path


def play_audio(audio_path):
    """Play the generated audio file according to the operating system."""

    system = platform.system()

    if system == "Darwin":
        subprocess.run(["afplay", str(audio_path)])
    elif system == "Windows":
        os.startfile(audio_path)
    else:
        subprocess.run(["xdg-open", str(audio_path)])


if __name__ == "__main__":
    text = (
        "Hi, my name is Whisperer. "
        "How can I help you today?"
    )
    audio_path = text_to_speech(text=text)
    play_audio(audio_path)
