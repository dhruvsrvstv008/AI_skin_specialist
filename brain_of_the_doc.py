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

    system_prompt = """You are a helpful AI skin care assistant. 
Generate a very BRIEF, CONCISE patient-facing skin consultation meant to be spoken aloud (1 minute max).
CRITICAL INSTRUCTION: You MUST NOT output any internal reasoning, chain of thought, or "Thinking Process". 
You MUST start your response directly with the Disclaimer. Do NOT use any <think> tags. Do NOT use ** for bolding anywhere.

REQUIRED RESPONSE STRUCTURE:
1. Disclaimer: Short sentence stating AI is not a doctor and cannot diagnose.
2. Observation: Briefly state what you see and what it may be.
3. Treatment: Briefly suggest specific ingredients or treatments.
4. Routine: 1-2 sentences on a basic skincare routine.
5. Warning: 1 sentence on what to avoid and when to see a dermatologist.

FORMATTING REQUIREMENTS:
- Do NOT use double asterisks (**) anywhere.
- Do NOT output Markdown bold formatting.
- Do NOT output internal reasoning, "Thinking Process", "Word count check", or any scratchpad.
- Your output must begin exactly with "1. Disclaimer" and contain ONLY the 5 required sections.
- Keep the entire response under 120 words. It will be converted to a short voice audio.
- Respond in the same language as the patient's question.
"""

    prompt = f"Patient question: {patient_text}\n\nStart your response immediately with '1. Disclaimer'."

    response = client.chat.completions.create(
        model=os.environ.get("GROQ_MODEL", "llama-3.2-11b-vision-preview"),
        max_completion_tokens=250,
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
    
    # Post-processing to remove any thinking process that might have leaked
    if "1. Disclaimer" in content:
        parts = content.split("1. Disclaimer")
        # Take everything after the first occurrence, and join in case there are multiple
        # We only want the disclaimer to appear ONCE at the very top.
        content = "1. Disclaimer" + "".join(parts[1:])

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
