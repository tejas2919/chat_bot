import streamlit as st
import speech_recognition as sr
import os
from dotenv import load_dotenv
import anthropic
import json
import time

# Load environment variables
load_dotenv()

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'is_recording' not in st.session_state:
    st.session_state.is_recording = False

def init_speech_recognition():
    try:
        recognizer = sr.Recognizer()
        # Adjust for ambient noise and sensitivity
        recognizer.dynamic_energy_threshold = True
        recognizer.energy_threshold = 4000  # Increase sensitivity
        recognizer.pause_threshold = 0.8    # Shorter pause detection
        return recognizer
    except Exception as e:
        st.error(f"Error initializing speech recognition: {str(e)}")
        return None

def record_audio():
    try:
        recognizer = init_speech_recognition()
        if not recognizer:
            return None

        # List available microphones
        mics = sr.Microphone.list_microphone_names()
        if not mics:
            st.error("No microphones found. Please connect a microphone and try again.")
            return None
        
        st.info("Available microphones: " + ", ".join(mics))
        
        with sr.Microphone() as source:
            # Clear any previous error messages
            if 'error' in st.session_state:
                del st.session_state.error
            
            # Visual feedback for recording
            st.session_state.is_recording = True
            placeholder = st.empty()
            placeholder.markdown("🎤 Adjusting for ambient noise... Please wait.")
            
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            placeholder.markdown("🎤 Listening... Speak now! (Recording will stop after silence)")
            try:
                # Add a progress bar for visual feedback
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.03)  # Total recording time feedback of 3 seconds
                    progress_bar.progress(i + 1)
                
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                placeholder.markdown("🔍 Processing your speech...")
                
                try:
                    text = recognizer.recognize_google(audio, language='en-US')
                    if text:
                        placeholder.markdown(f"✅ Recognized: '{text}'")
                        return text
                    else:
                        placeholder.markdown("❌ No speech detected. Please try again.")
                        return None
                except sr.UnknownValueError:
                    placeholder.markdown("❌ Could not understand audio. Please speak clearly and try again.")
                    return None
                except sr.RequestError as e:
                    placeholder.markdown(f"❌ Error with speech recognition service: {str(e)}")
                    return None
            except Exception as e:
                placeholder.markdown(f"❌ Error recording audio: {str(e)}")
                return None
            finally:
                st.session_state.is_recording = False
                if 'progress_bar' in locals():
                    progress_bar.empty()
    except Exception as e:
        st.error(f"Error setting up audio recording: {str(e)}")
        return None

def call_anthropic_api(prompt):
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        st.error("Please set your API key in the .env file")
        return None
    
    client = anthropic.Anthropic(api_key=api_key)
    
    try:
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text
    except Exception as e:
        st.error(f"Error calling API: {str(e)}")
        return None

def export_chat_history():
    chat_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
    return chat_history

# UI Setup
st.set_page_config(page_title="Max Chat Bot", page_icon="🤖")
st.title("🤖 Max Chat Bot")

# Sidebar
with st.sidebar:
    st.header("Options")
    
    # Voice input section with better feedback
    st.subheader("🎤 Voice Input")
    voice_col1, voice_col2 = st.columns([3, 1])
    with voice_col1:
        if st.button("Start Recording", disabled=st.session_state.is_recording):
            text = record_audio()
            if text:
                st.session_state.messages.append({"role": "user", "content": text})
                st.experimental_rerun()
    with voice_col2:
        if st.session_state.is_recording:
            st.markdown("🔴 REC")
    
    # Help section for voice input
    with st.expander("ℹ️ Voice Input Help"):
        st.markdown("""
        **Tips for better voice recognition:**
        - Speak clearly and at a normal pace
        - Use a good quality microphone
        - Minimize background noise
        - Keep a consistent distance from the microphone
        - Wait for the "Listening..." prompt before speaking
        """)
    
    # Export chat section
    st.subheader("📝 Export Chat")
    if st.button("Export Chat History"):
        chat_export = export_chat_history()
        st.download_button(
            label="Download Chat History",
            data=chat_export,
            file_name="chat_history.txt",
            mime="text/plain"
        )

# Main chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("What's on your mind?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = call_anthropic_api(prompt)
            if response:
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response}) 