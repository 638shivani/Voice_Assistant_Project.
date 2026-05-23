import streamlit as st
import joblib
from streamlit_mic_recorder import mic_recorder
from engine import transcribe
from actions import execute_command
import streamlit.components.v1 as components

# 1. Load your models
@st.cache_resource
def load_ml_models():
    vec = joblib.load('vectorizer.pkl')
    classifier = joblib.load('intent_model.pkl')
    return vec, classifier

vectorizer, clf = load_ml_models()

# 2. UI Layout
st.set_page_config(page_title="AI Web Assistant", layout="centered")
st.title("🎙️ AI Web Assistant")
st.write("Click 'Start Recording' and speak your command.")

# 3. Audio Recording
audio = mic_recorder(
    start_prompt="Start Recording",
    stop_prompt="Stop Recording",
    just_once=False,
    use_container_width=True
)

# 4. Processing Logic
if audio:
    with st.status("Processing your request...", expanded=True) as status:
        st.write("Saving audio...")
        with open("temp_audio.wav", "wb") as f:
            f.write(audio["bytes"])
        
        st.write("Transcribing...")
        user_text = transcribe("temp_audio.wav")
        st.info(f"You said: {user_text}")
        
        st.write("Analyzing intent...")
        text_vec = vectorizer.transform([user_text])
        intent = clf.predict(text_vec)[0]
        st.write(f"Detected Intent: {intent}")
        
        # Capture the result from actions.py
        response = execute_command(intent, user_text)
        
        # Display the result on the website
        st.success(f"Assistant says: {response}")
        
        # Web-based speaking (using browser synthesis instead of local drivers)
        js_code = f"""
        <script>
            var msg = new SpeechSynthesisUtterance('{response}');
            window.speechSynthesis.speak(msg);
        </script>
        """
        components.html(js_code, height=0)
        
        status.update(label="Task Complete!", state="complete", expanded=False)
