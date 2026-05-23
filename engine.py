import sounddevice as sd
import numpy as np
import whisper
import warnings
import scipy.io.wavfile as wav

warnings.filterwarnings("ignore")

print("Loading Whisper model...")
whisper_model = whisper.load_model("base")

def record_audio(duration=4, fs=44100, filename="temp_audio.wav"):
    """Bypasses drivers to record directly from hardware buffer"""
    print("Listening (Raw Buffer)...")
    try:
        # Record raw data
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype=np.int16, device=9)
        sd.wait()
        # Save as standard wav
        wav.write(filename, fs, recording)
        print("Success! Audio saved.")
        return filename
    except Exception as e:
        print(f"Hardware Error: {e}")
        return None

def transcribe(audio_path):
    result = whisper_model.transcribe(audio_path, fp16=False)
    return result["text"].strip().lower()

def speak(text):
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    engine.say(text)
    engine.runAndWait()