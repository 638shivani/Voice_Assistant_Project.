import streamlit as st
import joblib
from engine import transcribe
from actions import execute_command

# 1. Load your models
@st.cache_resource
def load_ml_models():
    vec = joblib.load('vectorizer.pkl')
    classifier = joblib.load('intent_model.pkl')
    return vec, classifier

vectorizer, clf = load_ml_models()

# 2. UI Layout
st.title("🎙️ AI Web Assistant")

# 3. Built-in Audio Input
audio_value = st.audio_input("Record a voice command")

# 4. Processing Logic
if audio_value:
    with st.status("Processing...", expanded=True) as status:
        st.write("Saving audio...")
        
        # Save the audio data directly from the buffer
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_value.read())
        
        st.write("Transcribing...")
        # engine.py will now handle the file directly
        user_text = transcribe("temp_audio.wav")
        st.info(f"You said: {user_text}")
        
        if user_text:
            st.write("Analyzing intent...")
            text_vec = vectorizer.transform([user_text])
            intent = clf.predict(text_vec)[0]
            
            response = execute_command(intent, user_text)
            st.success(f"Assistant says: {response}")
        else:
            st.warning("Could not understand audio. Please try again.")
        
        status.update(label="Task Complete!", state="complete", expanded=False)
