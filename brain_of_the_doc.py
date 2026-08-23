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

    system_prompt = """You are a helpful AI skin care assistant. 
Generate a clean, patient-facing skin consultation.
CRITICAL INSTRUCTION: You MUST NOT output any internal reasoning, chain of thought, or "Thinking Process". 
You MUST start your response directly with the Disclaimer. Do NOT use any <think> tags. Do NOT use ** for bolding anywhere.

REQUIRED RESPONSE STRUCTURE

1. Disclaimer
Start with a short disclaimer explaining that the AI is not a doctor and that image-based analysis cannot provide a definitive medical diagnosis.

2. What I Can See
Describe the visible skin concerns objectively. Use cautious language such as "This appearance may be consistent with...", "This looks like...", "The image shows...". Do not make a definitive diagnosis based only on an image.

3. What It May Be
Explain what the appearance could commonly be associated with. If the image appears consistent with acne, explain that clearly in simple language. Do not overstate severity unless the evidence supports it.

4. Treatment Plan
Provide a practical, step-by-step treatment routine that the user can follow or discuss with a dermatologist. Provide specific morning and night routines including Cleanser, Treatment, Moisturizer, and Sunscreen, explaining what each step does.

5. Important Things to Avoid
Clearly explain things to avoid (e.g., picking pimples, harsh scrubs, irritating products).

6. Expected Timeline
Give realistic expectations for when the user may notice improvements. Do not promise clear skin within a specific number of days.

7. When to See a Dermatologist
Explain when professional treatment is recommended (e.g., severe breakouts, painful lesions, scarring, no improvement from OTC treatments).

8. Personalized Product Review
If the user mentions specific products, evaluate them under KEEP, STOP, CHANGE, and ADD categories.

9. Final Summary
End with a short, practical summary of the Morning and Night routine, and one sentence on the importance of consistency.

FORMATTING REQUIREMENTS
- Do NOT use double asterisks (**) anywhere in the generated response.
- Do NOT output Markdown bold formatting.
- Do NOT output internal reasoning, "Thinking Process:", "1. Analyze the Request", or any scratchpad.
- Your output must begin exactly with "1. Disclaimer".
- Use clean headings, numbered steps, and bullet points.
- Use short paragraphs.
- Respond in the same language as the patient's question.

SAFETY REQUIREMENTS
- Do not claim that the AI can diagnose a medical condition from an image.
- Do not prescribe prescription medication.
- For over-the-counter treatments, provide general evidence-based guidance.
"""

    prompt = f"Patient question: {patient_text}"

    response = client.chat.completions.create(
        model=os.environ.get("GROQ_MODEL", "qwen/qwen3.6-27b"),
        max_completion_tokens=2000,
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
