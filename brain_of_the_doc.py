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


import io
from PIL import Image

def encode_file(filepath):
    try:
        img = Image.open(filepath)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        # Resize image to speed up API processing
        img.thumbnail((512, 512))
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        return base64.b64encode(buffer.getvalue()).decode("utf-8")
    except Exception:
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

    system_prompt = """You are a medical AI skin care assistant. 
You MUST output ONLY the final consultation text. Do NOT output any internal thoughts, image analysis, scratchpad, or drafting steps. 
If you output any thinking process, the system will crash.

REQUIRED RESPONSE STRUCTURE:
1. Disclaimer: State that AI is not a doctor and cannot diagnose.
2. Observation: Describe in detail what you see and what it may be.
3. Treatment: Suggest specific ingredients or treatments and explain why they help.
4. Routine: Detail a step-by-step basic skincare routine.
5. Warning: Explain what to avoid and when to see a dermatologist.

FORMATTING REQUIREMENTS:
- Do NOT use double asterisks (**) anywhere.
- Do NOT output Markdown bold formatting.
- Your output must begin exactly with "1. Disclaimer" and contain ONLY the 5 sections. Do not include introductory text.
- Keep the entire response around 250-300 words.
"""

    prompt = f"Patient question: {patient_text}\n\nOutput ONLY the final consultation. Start immediately with '1. Disclaimer' and nothing else."

    response = client.chat.completions.create(
        model=os.environ.get("GROQ_MODEL", "qwen/qwen3.6-27b"),
        max_completion_tokens=1000,
        messages=[
            {
                "role": "system",
                "content": system_prompt
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

    content = response.choices[0].message.content
    
    # Post-processing to clean up any leaked drafting text if the model disobeys
    if "*Draft:*" in content:
        content = content.split("*Draft:*")[-1].strip()
        # Ensure it starts with 1. Disclaimer if it got stripped
        if not content.startswith("1. Disclaimer") and "2. Observation" in content:
            content = "1. Disclaimer\n" + content
    elif "1. Disclaimer" in content:
        # Take the LAST occurrence of "1. Disclaimer" in case it leaked its prompt rules first
        parts = content.split("1. Disclaimer")
        content = "1. Disclaimer" + parts[-1]

    return content


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
