import whisper
import streamlit as st
import speech_recognition as sr
import openai
import uuid
import pyttsx3
from langdetect import detect  # Import the language detection function

# Initialize Streamlit
st.title("ABU - THE BOT: Your Healthcare Assistant")

# Set your OpenAI API key
api_key = "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"
openai.api_key = api_key

# Load Whisper model
model = whisper.load_model("medium")

# Function to capture and transcribe audio
def record_and_transcribe_audio():
    # Record audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening... Speak something.")
        audio_data = r.listen(source)
        st.write("Recording complete!")

    # Transcribe audio using Whisper
    audio = whisper.audio.from_speech_recognition(audio_data)
    transcription = whisper.asr.transcribe(model, audio)

    return transcription

# Function to generate a response using GPT-3.5 Turbo
def generate_gpt3_response(text):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}],
        )
        response = completion.choices[0].message.content
        return response
    except Exception as e:
        return str(e)

# Function to speak text using text-to-speech
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to detect the language of a text
def detect_language(text):
    try:
        language = detect(text)
        return language
    except Exception as e:
        return "Unknown"

# Create a button to start the process
if st.button("Start Conversation"):
    # Record and transcribe audio
    transcription = record_and_transcribe_audio()

    if transcription:
        st.subheader("Transcription:")
        st.write(transcription)

        # Detect the language of the transcribed text
        detected_language = detect_language(transcription)
        st.subheader("Detected Language:")
        st.write(detected_language)

        # Send the transcribed text to GPT-3.5 Turbo for a response
        response = generate_gpt3_response(transcription)
        st.subheader("Response from ABU - THE BOT:")
        st.write(response)

        # Speak the response
        speak_text(response)
