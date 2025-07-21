import gradio as gr
import os
import sys

# Ajout du chemin parent pour importer app.utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.utils import transcribe_audio, analyze_sentiment


def process_audio(audio_path):
    if not audio_path or not os.path.exists(audio_path):
        return "", "⚠️ Aucun fichier audio reçu.", None

    # Transcription
    print(audio_path)
    transcription = transcribe_audio(audio_path)

    # Analyse du sentiment
    sentiment_result = analyze_sentiment(transcription)
    label = sentiment_result.get("label", "N/A")
    score = sentiment_result.get("score", 0)
    sentiment_display = f"{label.upper()} (score: {score:.2f})"

    return str(transcription), str(sentiment_display), audio_path


css = """
    .gr-button {
        background-color: blue !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: bold;
        font-size: 16px !important;
    }
    .gr-textbox textarea {
        font-size: 16px !important;
    }
    .gr-box {
        background-color: #f8f9fa !important;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    #header {
        text-align: center;
        font-weight: 800;
        color: #333;
    }
"""

with gr.Blocks(title="Détection Automatique de Sentiment Audio", css=css) as demo:
    gr.Markdown(
        """
        #  Détection Automatique de Sentiment Audio
        """,
        elem_id="header"
    )

    with gr.Tabs():
        with gr.Tab(" Importer un fichier audio"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("###  Fichier audio")
                    audio_input_upload = gr.Audio(
                        sources=["upload"], 
                        type="filepath", 
                        label="Charger uniquement les fichiers audio (.wav)"
                    )
                    btn_upload = gr.Button("Transcrire & Analyser")
                with gr.Column(scale=2):
                    gr.Markdown("###  Résultats")
                    with gr.Column():
                        audio_output_upload = gr.Audio(
                            label=" Audio importé", 
                            interactive=False,
                            #type="filepath"
                        )
                        transcribed_text_upload = gr.Textbox(
                            label=" Transcription", 
                            lines=4, 
                            interactive=False
                        )
                        sentiment_label_upload = gr.Textbox(
                            label="Détectection de sentiment", 
                            interactive=False
                        )

            btn_upload.click(
                fn=process_audio,
                inputs=audio_input_upload,
                outputs=[transcribed_text_upload, sentiment_label_upload, audio_output_upload]
            )


demo.launch(show_api=False, share=True)
