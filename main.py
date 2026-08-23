import os
from voice_of_the_user import speech_to_text
from brain_of_the_doc import brain_of_the_doctor
from voice_of_the_doctor import text_to_speech

import gradio as gr
import tempfile
import base64
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');

:root {
    --surface: #ffffff;
    --background: #f9f9ff;
    --surface-subtle: #f9fafb;
    --surface-blue: #f1f3ff;
    --ink: #141b2b;
    --muted: #434655;
    --primary: #1d4ed8;
    --primary-dark: #0037b0;
    --border: #e5e7eb;
    --outline: #c4c5d7;
    --success: #047857;
    --error: #b91c1c;
}

body, .gradio-container {
    background: var(--background) !important;
    color: var(--ink) !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
}

.gradio-container {
    max-width: 1440px !important;
    padding: 0 !important;
}

.topbar {
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 20px 32px 18px;
}

.topbar h1 { margin: 0; font-size: 30px; line-height: 1.2; font-weight: 700; }
.topbar p { margin: 6px 0 0; color: var(--muted); font-size: 16px; }

.dashboard {
    max-width: 1200px;
    margin: 0 auto;
    padding: 58px 24px 72px;
}

.section-title { gap: 12px; align-items: center; margin-bottom: 20px; }
.section-title h2 { margin: 0; font-size: 24px; line-height: 1.3; font-weight: 600; }
.section-icon { color: var(--primary); font-size: 28px; }

.panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 4px 12px rgba(20, 27, 43, 0.05);
}

.panel-label { color: var(--ink); font-size: 14px; font-weight: 600; margin: 0 0 10px; }
.media-field { margin-bottom: 18px; }
.media-field > label { color: var(--ink) !important; font-weight: 600 !important; }

.panel .file-preview, .panel .upload-container {
    border-color: var(--outline) !important;
    background: var(--surface-subtle) !important;
    border-radius: 8px !important;
}

.panel .wrap, .panel .block {
    border-color: var(--border) !important;
}

.analyze-button {
    background: var(--primary) !important;
    border: 0 !important;
    border-radius: 8px !important;
    color: white !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    min-height: 52px !important;
    margin-top: 6px;
}

.analyze-button:hover { background: var(--primary-dark) !important; }
.analyze-button:disabled { opacity: .65; }

.tip {
    background: var(--surface-blue);
    border: 1px solid #b7c4ff;
    border-radius: 8px;
    color: #001e5b;
    font-size: 14px;
    line-height: 1.5;
    margin-top: 20px;
    padding: 14px 16px;
}

.response-panel { min-height: 520px; }
.response-field { margin-bottom: 18px; }
.response-field textarea { background: var(--surface-subtle) !important; }
.response-field textarea, .response-field input { border-color: var(--border) !important; color: var(--ink) !important; }
.response-label { font-size: 14px; font-weight: 600; margin-bottom: 8px; }
.status { min-height: 28px; margin-top: 14px; font-size: 14px; }
.status.success { color: var(--success); }
.status.error { color: var(--error); }
.trust { border-top: 1px solid var(--border); color: #747686; font-size: 13px; justify-content: center; padding-top: 18px; margin-top: 18px; }

.footer {
    background: var(--surface-blue);
    border-top: 1px solid var(--border);
    color: var(--muted);
    padding: 28px 32px;
    font-size: 13px;
}
.footer strong { color: var(--ink); font-size: 15px; }

@media (max-width: 800px) {
    .topbar { padding: 18px 16px; }
    .topbar h1 { font-size: 25px; }
    .dashboard { padding: 36px 16px 48px; }
    .panel { padding: 18px; }
    .response-panel { min-height: 0; }
    .trust { justify-content: flex-start; }
    .footer { padding: 24px 16px; }
}
"""


# ============================================================
# MAIN PROCESSING FUNCTION
# ============================================================

def process_inputs(audio_filepath, image_filepath, video_filepath=None):

    # --------------------------------------------------------
    # STEP 1: Patient Voice → Text
    # --------------------------------------------------------

    patient_text = (
        speech_to_text(audio_filepath=audio_filepath)
        if audio_filepath
        else "No patient question was provided. Assess the skin image and give general skincare guidance."
    )


    # --------------------------------------------------------
    # STEP 2: Patient Text + Image → Doctor Response
    # --------------------------------------------------------

    doctor_text = brain_of_the_doctor(
        patient_text=patient_text,
        image_filepath=image_filepath
    )


    # --------------------------------------------------------
    # STEP 3: Doctor Response → Doctor Voice
    # --------------------------------------------------------

    doctor_audio = text_to_speech(
        text=doctor_text
    )


    # --------------------------------------------------------
    # STEP 4: Return results to Gradio
    # --------------------------------------------------------

    return (
        patient_text,
        doctor_text,
        str(doctor_audio)
    )


def run_analysis(audio_filepath, image_filepath):
    """Run the consultation and turn failures into useful UI feedback."""
    try:
        patient_text, doctor_text, doctor_audio = process_inputs(
            audio_filepath,
            image_filepath,
        )
        return patient_text, doctor_text, doctor_audio, "<span class='status success'>Analysis complete. Review the guidance below.</span>"
    except Exception as error:
        return "", "", None, f"<span class='status error'>Unable to complete analysis: {error}</span>"


# ============================================================
# STITCH-INSPIRED GRADIO UI
# ============================================================

with gr.Blocks(title="AI Skin Specialist") as iface:
    gr.HTML(
        """
        <header class="topbar">
            <h1>AI Skin Specialist</h1>
            <p>Voice and image based skin consultation assistant</p>
        </header>
        """
    )

    with gr.Column(elem_classes="dashboard"):
        with gr.Row(equal_height=False):
            with gr.Column(scale=1):
                gr.HTML('<div class="section-title"><span class="section-icon">✚</span><h2>Patient Input</h2></div>')
                with gr.Column(elem_classes="panel"):
                    gr.HTML('<p class="panel-label">Describe your skin concern</p>')
                    audio_input = gr.Audio(
                        sources=["microphone", "upload"],
                        type="filepath",
                        label="Patient voice",
                        elem_classes="media-field",
                    )
                    image_input = gr.Image(
                        type="filepath",
                        sources=["upload", "webcam"],
                        label="Skin image (required)",
                        elem_classes="media-field",
                    )
                    analyze_button = gr.Button("▣  Analyze Concern", elem_classes="analyze-button")
                gr.HTML('<div class="tip">ⓘ &nbsp; For better assessment, photograph the affected area under good lighting and include all visible symptoms.</div>')

            with gr.Column(scale=1):
                gr.HTML('<div class="section-title"><span class="section-icon">◈</span><h2>Doctor Response</h2></div>')
                with gr.Column(elem_classes="panel response-panel"):
                    transcript_output = gr.Textbox(
                        label="AI Transcript",
                        placeholder="Your voice transcription will appear here after analysis.",
                        lines=4,
                        interactive=False,
                        elem_classes="response-field",
                    )
                    response_output = gr.Textbox(
                        label="Medical Guidance",
                        placeholder="Your consultation guidance will appear here after analysis.",
                        lines=10,
                        interactive=False,
                        elem_classes="response-field",
                    )
                    audio_output = gr.Audio(label="Doctor's Voice", interactive=False, autoplay=True, elem_classes="response-field")
                    status_output = gr.HTML('<span class="status">Ready for analysis.</span>')
                gr.HTML('<div class="trust">♢ &nbsp; HIPAA Compliant Encryption &nbsp;&nbsp; | &nbsp;&nbsp; Privacy Guaranteed</div>')

        gr.HTML(
            """
            <footer class="footer">
                <strong>AI Skin Specialist</strong><br>
                For informational purposes only. AI guidance is not a medical diagnosis. Consult a licensed dermatologist for urgent or serious symptoms.
            </footer>
            """
        )

    analyze_button.click(
        fn=run_analysis,
        inputs=[audio_input, image_input],
        outputs=[transcript_output, response_output, audio_output, status_output],
        show_progress="full",
        api_name="run_analysis",
    )


# ============================================================
# FASTAPI REST API + GRADIO MOUNT
# ============================================================

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def root():
    return {"message": "AI Skin Specialist Backend is Running"}

@app.post('/api/analyze')
async def api_analyze(
    audio_input: UploadFile = File(None),
    image_input: UploadFile = File(None),
    video_input: UploadFile = File(None)
):
    """REST API endpoint for frontend"""
    try:
        if not image_input:
            return JSONResponse(status_code=400, content={'error': 'Image file is required'})

        # Create temporary directory for files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save image
            image_path = os.path.join(temp_dir, image_input.filename)
            with open(image_path, "wb") as f:
                f.write(await image_input.read())

            # Save audio if provided
            audio_path = None
            if audio_input:
                audio_path = os.path.join(temp_dir, audio_input.filename)
                with open(audio_path, "wb") as f:
                    f.write(await audio_input.read())

            # Save video if provided
            video_path = None
            if video_input:
                video_path = os.path.join(temp_dir, video_input.filename)
                with open(video_path, "wb") as f:
                    f.write(await video_input.read())

            # Call the analysis function and preserve failures as API errors.
            try:
                transcript, response_text, audio_output = process_inputs(
                    audio_path,
                    image_path,
                    video_path,
                )
            except Exception as error:
                return JSONResponse(status_code=500, content={'error': str(error)})

            # Read audio file if it was generated
            audio_data = None
            if audio_output and os.path.exists(str(audio_output)):
                try:
                    with open(str(audio_output), 'rb') as f:
                        audio_data = f"data:audio/wav;base64,{base64.b64encode(f.read()).decode()}"
                except:
                    pass

            return JSONResponse(status_code=200, content={
                'transcript': transcript,
                'response': response_text,
                'audio': audio_data
            })

    except Exception as e:
        print(f"Error in API: {str(e)}")
        return JSONResponse(status_code=500, content={'error': str(e)})


# Mount Gradio app onto FastAPI
app = gr.mount_gradio_app(app, iface, path="/ui")

# ============================================================
# LAUNCH APP
# ============================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)


'''from voice_of_the_user import speech_to_text
from brain_of_the_doc import brain_of_the_doctor
from voice_of_the_doctor import text_to_speech, play_audio


import gradio as gr



# Logic + UI
def process_inputs(audio_filepath, image_filepath, video_filepath):
    patient_text = transcribe_patient_voice(audio_filepath)

    doctor_text = brain_of_the_doctor(
        patient_text=patient_text,
        image_filepath=image_filepath,
        video_filepath=video_filepath,
    )

    doctor_audio = convert_text_to_doctor_audio(doctor_text)

    play_audio(doctor_audio)

    return patient_text, doctor_text, str(doctor_audio)




iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone", "upload"], type="filepath", label="Patient Voice"),
        gr.Image(type="filepath", label="Patient Image"),
        gr.Video(label="Patient Video"),
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio(label="Doctor's Voice"),
    ],
    title="AI Skin Specialist with Vision and Voice",
)

'''