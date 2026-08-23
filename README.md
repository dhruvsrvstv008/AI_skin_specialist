# AI Skin Specialist

A voice and image based skin consultation assistant powered by Groq (Whisper + vision LLM) and Deepgram TTS, built with Gradio.

**Live demo:** https://ai-skin-specialist-he3a.onrender.com

---

## What it does

1. **Voice input** — Record or upload a voice clip describing your skin concern.
2. **Image input** — Upload or webcam-capture a photo of the affected area.
3. **AI analysis** — Groq Whisper transcribes the voice; a Qwen vision model analyses the image alongside your question.
4. **Voice response** — Deepgram converts the doctor's text response to spoken audio.

The app provides general skincare information only. It is not a medical diagnosis tool.

---

## Stack

| Layer | Technology |
|---|---|
| UI | Gradio 6.25 |
| Speech to text | Groq Whisper (`whisper-large-v3`) |
| Vision LLM | Groq (`qwen/qwen3.6-27b`) |
| Text to speech | Deepgram Aura 2 (`aura-2-thalia-en`) |
| Runtime | Python 3.11, uv |
| Hosting | Render (free tier, Singapore) |

---

## Local development

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- A `GROQ_API_KEY` from [console.groq.com](https://console.groq.com)
- A `DEEPGRAM_API_KEY` from [console.deepgram.com](https://console.deepgram.com)

### Setup

```bash
git clone https://github.com/dhruvsrvstv008/AI_skin_specialist.git
cd AI_skin_specialist
cp .env.example .env   # then fill in your keys
uv sync --frozen
uv run --no-sync python main.py
```

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_key_here
DEEPGRAM_API_KEY=your_deepgram_key_here
```

The app starts at http://localhost:7860 by default. Set the `PORT` environment variable to use a different port.

### Optional overrides

| Variable | Default | Description |
|---|---|---|
| `GROQ_MODEL` | `qwen/qwen3.6-27b` | Groq vision model ID |
| `WHISPER_MODEL` | `whisper-large-v3` | Groq Whisper model ID |
| `PORT` | `7860` | Server port |

---

## Render deployment

### Build command
```
uv sync --frozen && uv cache prune --ci
```

### Start command
```
uv run --no-sync python main.py
```

### Required environment variables
Set these in the Render dashboard under **Environment**:
- `GROQ_API_KEY`
- `DEEPGRAM_API_KEY`
- `PYTHONUNBUFFERED=1`

---

## Project structure

```
main.py                  # Gradio UI and request orchestration
voice_of_the_user.py     # Groq Whisper speech-to-text
brain_of_the_doc.py      # Groq vision LLM
voice_of_the_doctor.py   # Deepgram text-to-speech
pyproject.toml           # Dependencies
uv.lock                  # Pinned dependency versions
```

---

## Disclaimer

This tool provides general skincare information for educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Consult a licensed dermatologist for any skin concerns.
