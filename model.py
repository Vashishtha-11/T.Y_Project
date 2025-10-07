import yt_dlp
import os
from pydub import AudioSegment
import speech_recognition as sr
from transformers import pipeline, BartTokenizer, BartForConditionalGeneration
import re
import streamlit as st
from googletrans import Translator

def safe_filename(name):
    return re.sub(r'[\\/*?:"<>|]', '_', name)

# Load the summarization model and tokenizer
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)
translator = Translator()

def download_audio(url, download_path="downloads"):
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',   # ✅ prefer audio-only
        'outtmpl': f'{download_path}/%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': False,        # show progress
        'no_warnings': True,   # suppress warnings
        'ignoreerrors': True,  # skip bad fragments if any
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        audio_file = ydl.prepare_filename(info_dict)
    return audio_file


def convert_to_wav(input_path, wav_path):
    audio = AudioSegment.from_file(input_path)
    audio.export(wav_path, format="wav")


def clean_text(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

# 🔹 Transcribe in chunks
def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_wav(audio_path)
    chunk_length_ms = 60000  # 1 min
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    full_transcript = ""
    for i, chunk in enumerate(chunks):
        chunk.export("temp_chunk.wav", format="wav")
        with sr.AudioFile("temp_chunk.wav") as source:
            audio_data = recognizer.record(source)
            try:
                transcript = recognizer.recognize_google(audio_data)
                full_transcript += transcript + " "
            except sr.UnknownValueError:
                print(f"Could not understand audio for chunk {i+1}")
            except sr.RequestError as e:
                print(f"Request error for chunk {i+1}; {e}")
    return full_transcript

def summarize_in_chunks(text, chunk_size=1024):
    text = clean_text(text)
    if len(text.split()) < 40:  # too short, skip summarizer
        return text
    
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    summaries = []
    for chunk in chunks:
        max_len = min(150, len(chunk)//2)  # prevent warning
        summary = summarizer(chunk, max_length=max_len, min_length=20, do_sample=False)
        summaries.append(summary[0]['summary_text'])
    return " ".join(summaries)

# 🔹 Translate
def translate_text(text, target_language):
    translation = translator.translate(text, dest=target_language)
    return translation.text

# 🔹 Streamlit App
def main():
    st.title("YouTube Audio Transcriber, Summarizer, and Translator")
    video_url = st.text_input("Enter the YouTube video URL")

    if video_url:
        st.write("Processing audio...")

        download_path = "downloads"
        os.makedirs(download_path, exist_ok=True)

        try:
            audio_file = download_audio(video_url, download_path)
            st.write(f"Downloaded audio file: {audio_file}")

            safe_name = safe_filename(os.path.splitext(os.path.basename(audio_file))[0])
            audio_file_wav = os.path.join(download_path, safe_name + ".wav")
            convert_to_wav(audio_file, audio_file_wav)

            transcript = transcribe_audio(audio_file_wav)
            st.subheader("Full Transcript:")
            st.write(transcript)

            summarized_transcript = summarize_in_chunks(transcript)
            st.subheader("Summarized Transcript:")
            st.write(summarized_transcript)

            # Translation
            languages = {'Spanish': 'es', 'French': 'fr', 'German': 'de', 'Chinese': 'zh-cn', 'Hindi': 'hi'}
            selected_language = st.selectbox("Select a language for translation", list(languages.keys()))

            if st.button("Translate Summary"):
                translated_text = translate_text(summarized_transcript, languages[selected_language])
                st.subheader(f"Translated Summary in {selected_language}:")
                st.write(translated_text)
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
