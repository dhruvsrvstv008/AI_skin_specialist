import base64
import mimetypes
import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


load_dotenv(Path(__file__).parent / ".env")


def get_media_type(filepath, fallback="image/png"):
    media_type, _ = mimetypes.guess_type(filepath)
    return media_type or fallback


def encode_file(filepath):
    with open(filepath, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


def brain_of_the_doctor(patient_text, image_filepath=None):

    if not image_filepath:
        raise ValueError("Image file is required.")

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set.")

    client = Groq(api_key=api_key)

    image_data = encode_file(image_filepath)

    media_type = get_media_type(image_filepath, "image/png")

    prompt = (
        "You are a helpful AI skin care assistant. "
        "Analyze the provided skin image and the patient's question. "
        "Give general skincare information and possible observations, "
        "but do not claim to provide a medical diagnosis. "
        "Be clear, concise, and helpful. "
        "Respond in the same language as the patient's question. "
        "Do not use markdown, asterisks, or unnecessary special characters. "
        f"Patient question: {patient_text}"
    )

    response = client.chat.completions.create(
        model=os.environ.get(
            "GROQ_MODEL",
            "qwen/qwen3.6-27b"
        ),
        max_completion_tokens=1000,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful AI skin care assistant. "
                    "Provide general information and safety-focused "
                    "guidance, not a medical diagnosis."
                )
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": (
                                f"data:{media_type};base64,"
                                f"{image_data}"
                            )
                        }
                    }
                ]
            }
        ]
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    folder = os.path.dirname(__file__)
    image_path = os.path.join(folder, "test-image.png")
    patient_text = (
        "What do you see in this image? "
        "Please give me general skincare advice."
    )
    result = brain_of_the_doctor(
        patient_text=patient_text,
        image_filepath=image_path
    )
    print("\nDoctor's Response:")
    print(result)
