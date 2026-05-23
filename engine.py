import whisper
import warnings

# Ignore warnings for cleaner logs
warnings.filterwarnings("ignore")

# Load the model once
print("Loading Whisper model...")
whisper_model = whisper.load_model("base")

def transcribe(audio_path):
    """Transcribes the audio file saved by the browser."""
    try:
        # Whisper processes the file saved from your streamlit-mic-recorder
        result = whisper_model.transcribe(audio_path, fp16=False)
        return result["text"].strip().lower()
    except Exception as e:
        print(f"Transcription Error: {e}")
        return ""

# 'speak' is removed because cloud servers cannot play sound through your local speakers.
# You will use st.write() or st.success() in app.py to "show" the answer instead.